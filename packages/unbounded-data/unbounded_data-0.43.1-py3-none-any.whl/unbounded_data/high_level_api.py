from typing import Union, Optional
import os
import asyncio
import re
import csv
import json
import threading
from io import StringIO, BytesIO

import pandas as pd

from .datasets import Client, Dataset


def _refresh_client(client: Optional[Client] = None) -> Client:
    """
    description:    creates or reuses a global Client object. can use user-provided object instead.

    arguments:      client - user-provided Client to use.

    returns:        Client structure.
    """

    if client is not None:
        return client

    return Client()


def _desynchronize_async_helper(to_return: any, sync: bool = True) -> Union[asyncio.Future, any]:
    """
    description:    returns a value that was generated synchronously in a Future.

    arguments:      to_return - input value.
                    sync - whether to return the value directly or wrap it in a complete Future.

    returns:        Future or return value
    """

    if sync:
        return to_return

    future = asyncio.Future()
    future.set_result(to_return)
    return future


def _synchronize_async_helper(to_await: asyncio.Future, sync: bool = True) -> Union[asyncio.Future, any]:
    """
    description:    runs asynchronous queries synchronously.

    arguments:      to_await - input future.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.

    returns:        to_await (if not sync) or return value of to_await (if sync).
    """

    if not sync:
        return to_await

    async_response = []
    async_exception = []

    async def run_and_capture_result():
        try:
            response = await to_await
            async_response.append(response)
        except Exception as exc:
            async_exception.append(exc)

    def thread_func():
        if os.name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.new_event_loop()
        coroutine = run_and_capture_result()
        loop.run_until_complete(coroutine)

    thread = threading.Thread(target=thread_func)
    thread.start()
    thread.join()

    if async_exception:
        raise async_exception[0]

    return async_response[0]


def _guess_mime_type(check_bytes: bytes) -> str:
    """
    description:    guesses MIME type. raises with a nice error if magic is not installed.

    arguments:      check_bytes - byte array to autodetect.

    returns:        MIME type.
    """

    try:
        # pylint: disable-next=import-outside-toplevel
        import magic

        return magic.from_buffer(check_bytes, mime=True)
    except ImportError as exc:
        raise ImportError('Python-Magic is required to detect MIME type automatically') from exc


def _get_dataset_from_arg(dataset_name_or_id: Union[Dataset, str], client: Client) -> Optional[Dataset]:
    """
    description:    returns dataset by either it's direct value, UUID, or name. guesses parameter type.

    arguments:      dataset_name_or_id - value to guess.

    returns:        Dataset instance, if found.
    """

    if isinstance(dataset_name_or_id, Dataset):
        dataset = _desynchronize_async_helper(dataset_name_or_id, sync=False)
    elif re.match(r'^[A-Fa-f0-9]{8}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{12}$', dataset_name_or_id):
        dataset = client.get_dataset(uuid=dataset_name_or_id)
    else:
        dataset = client.get_dataset(name=dataset_name_or_id)
    return dataset


def read_file(dataset_name_or_id: Union[Dataset, str],
              file_name: str,
              sync: bool = True,
              client: Optional[Client] = None) -> Union[asyncio.Future[bytes], bytes]:
    """
    description:    reads file from dataset as bytes.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to read.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.

    returns:        file content.
    """

    async def read_file_func():
        real_client = _refresh_client(client=client)
        try:
            dataset = await _get_dataset_from_arg(dataset_name_or_id, client=real_client)
            dataset_version = await dataset.latest()
            buf = await dataset_version.get_file(file_name).raw()
            buf.seek(0)
            return buf.read()
        finally:
            await real_client.close_session()

    return _synchronize_async_helper(read_file_func(), sync=sync)


def write_file(dataset_name_or_id: Union[Dataset, str],
               file_name: str,
               content: Union[str, bytes],
               mime_type: Optional[str] = None,
               sync: bool = True,
               client: Optional[Client] = None) -> Optional[asyncio.Future]:
    """
    description:    writes bytes to a dataset as file.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to write.
                    content - bytes or string.
                    mime_type - MIME type. preferred. will try to guess with 'magic' module if this is not specified.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.

    returns:        future or nothing.
    """

    if mime_type is None:
        mime_type = _guess_mime_type(mime_type)

    if not isinstance(content, bytes):
        content = content.encode('utf-8')

    buf = BytesIO()
    buf.write(content)
    buf.seek(0)

    async def write_file_func():
        real_client = _refresh_client(client=client)
        try:
            dataset = await _get_dataset_from_arg(dataset_name_or_id, client=real_client)
            await dataset.create_raw_file(buf, file_name, mime_type)
        finally:
            await real_client.close_session()

    return _synchronize_async_helper(write_file_func(), sync=sync)


def read_json(dataset_name_or_id: Union[Dataset, str],
              file_name: str,
              sync: bool = True,
              client: Optional[Client] = None) -> Union[Union[dict, list, str, bool, int, float, None],
                                                        asyncio.Future[dict, list, str, bool, int, float, None]]:
    """
    description:    reads file from dataset as JSON.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to read.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.

    returns:        parsed JSON object.
    """

    return _desynchronize_async_helper(json.loads(read_file(dataset_name_or_id, file_name, sync=True, client=client)), sync=sync)


def write_json(dataset_name_or_id: Union[Dataset, str],
               file_name: str,
               content: any,
               sync: bool = True,
               client: Optional[Client] = None) -> Optional[asyncio.Future]:
    """
    description:    writes JSON-serializable object to a dataset as file.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to write.
                    content - any value serializable with `json.dumps()`.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.

    returns:        future or nothing.
    """

    bytes_content = json.dumps(content).encode('utf-8')
    return write_file(dataset_name_or_id, file_name, bytes_content, mime_type='application/json', sync=sync, client=client)


def read_csv(dataset_name_or_id: Union[Dataset, str],
             file_name: str,
             sync: bool = True,
             client: Optional[Client] = None,
             sep: str = ',') -> Union[asyncio.Future[pd.DataFrame], pd.DataFrame]:
    """
    description:    reads CSV file from dataset as DataFrame.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to read.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.
                    sep - column separator, defaults to comma (,).

    returns:        DataFrame.
    """

    async def read_file_func():
        real_client = _refresh_client(client=client)
        try:
            dataset = await _get_dataset_from_arg(dataset_name_or_id, client=real_client)
            dataset_version = await dataset.latest()
            buf = await dataset_version.get_file(file_name).raw()
            buf.seek(0)
            return buf.read()
        finally:
            await real_client.close_session()

    as_bytes = _synchronize_async_helper(read_file_func(), sync=True)
    buf = StringIO()
    buf.write(as_bytes.decode('utf-8', errors='surrogateescape'))
    buf.seek(0)
    return _desynchronize_async_helper(pd.read_csv(buf, engine='python', sep=sep), sync=sync)


def read_tsv(dataset_name_or_id: Union[Dataset, str],
             file_name: str,
             sync: bool = True,
             client: Optional[Client] = None) -> Union[asyncio.Future[pd.DataFrame], pd.DataFrame]:
    """
    description:    reads TSV file from dataset as DataFrame.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to read.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.

    returns:        DataFrame.
    """

    return read_csv(dataset_name_or_id, file_name, sync=sync, client=client, sep='\t')


def write_csv(dataset_name_or_id: Union[Dataset, str],
              file_name: str,
              content: Union[pd.DataFrame, list[list]],
              sync: bool = True,
              client: Optional[Client] = None,
              sep: str = ',') -> Optional[asyncio.Future]:
    """
    description:    writes Python-style CSV or Pandas DataFrame to a dataset as CSV file.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to write.
                    content - list of lists of str or a DataFrame.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.
                    sep - column separator, defaults to comma (,).

    returns:        future or nothing.
    """

    mime_type = 'text/csv'
    if sep == '\t':
        mime_type = 'text/tab-separated-values'

    buf = StringIO()
    if isinstance(content, list):
        writer = csv.writer(buf)
        writer.writerows(content)
    else:
        content.to_csv(buf, index=False, sep=sep)
    buf.seek(0)
    bytes_content = buf.read().encode('utf-8', errors='surrogateescape')
    return write_file(dataset_name_or_id, file_name, bytes_content, mime_type=mime_type, sync=sync, client=client)


def write_tsv(dataset_name_or_id: Union[Dataset, str],
              file_name: str,
              content: Union[pd.DataFrame, list[list]],
              sync: bool = True,
              client: Optional[Client] = None) -> Optional[asyncio.Future]:
    """
    description:    writes Python-style CSV or Pandas DataFrame to a dataset as TSV file.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to write.
                    content - list of lists of str or a DataFrame.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.

    returns:        future or nothing.
    """

    return write_csv(dataset_name_or_id, file_name, content, sync=sync, client=client, sep='\t')


def read_parquet(dataset_name_or_id: Union[Dataset, str],
                 file_name: str,
                 sync: bool = True,
                 client: Optional[Client] = None) -> Union[asyncio.Future[pd.DataFrame], pd.DataFrame]:
    """
    description:    reads Parquet file from dataset as DataFrame.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to read.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.

    returns:        DataFrame.
    """

    async def read_file_func():
        real_client = _refresh_client(client=client)
        try:
            dataset = await _get_dataset_from_arg(dataset_name_or_id, client=real_client)
            dataset_version = await dataset.latest()
            buf = await dataset_version.get_file(file_name).raw()
            buf.seek(0)
            return buf
        finally:
            await real_client.close_session()

    return _desynchronize_async_helper(pd.read_parquet(_synchronize_async_helper(read_file_func(), sync=True)), sync=sync)


def write_parquet(dataset_name_or_id: Union[Dataset, str],
                  file_name: str,
                  content: Union[list[list], pd.DataFrame],
                  sync: bool = True,
                  client: Optional[Client] = None) -> Optional[asyncio.Future]:
    """
    description:    writes Python-style CSV or Pandas DataFrame to a dataset as Parquet file.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to write.
                    content - list of lists of str or a DataFrame.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.

    returns:        future or nothing.
    """

    if isinstance(content, list):
        content = pd.DataFrame(content[1:], columns=content[0])
    buf = BytesIO()
    content.to_parquet(buf, index=False)
    buf.seek(0)
    content_bytes = buf.read()
    return write_file(dataset_name_or_id, file_name, content_bytes, mime_type='application/vnd.apache.parquet', sync=sync, client=client)


__all__ = ['read_file', 'write_file',
           'read_csv', 'write_csv',
           'read_tsv', 'write_tsv',
           'read_json', 'write_json',
           'read_parquet', 'write_parquet']
