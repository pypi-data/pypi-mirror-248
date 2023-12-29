import time
import random
import logging
from enum import Enum
import pandas as pd
from benedict import benedict
from graphql import DocumentNode
from gql import gql
from gql import Client as gqlClient
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import (
    TransportQueryError,
    TransportAlreadyConnected,
    TransportClosed,
    TransportServerError,
    TransportProtocolError,
)

MAINNET_ENDPOINT_URL = "https://uwalletd.attestedinfo.com/graphql"
GOERLI_ENDPOINT_URL = "https://uwalletd.goerli.attestedinfo.com/graphql"


class RangeFilter:
    """
    Class used to store range filter attributes:
    - start block
    - end block
    - start time
    - end time
    """

    def __init__(
        self,
        start_block: int = None,
        end_block: int = None,
        start_time: int = None,
        end_time: int = None,
    ):
        self.start_block = start_block
        self.end_block = end_block
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {
            "startBlock": self.start_block,
            "endBlock": self.end_block,
            "startTime": self.start_time,
            "endTime": self.end_time,
        }


class TokenTransferFilter:
    """
    Class used to store token transfer filter attributes:
    - from
    - to
    - token
    """

    def __init__(
        self, from_addr: str = None, to_addr: str = None, token_addr: str = None
    ):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.token_addr = token_addr

    def to_dict(self):
        return {
            "from": self.from_addr,
            "to": self.to_addr,
            "token": self.token_addr,
        }


class Fields:
    """
    Class used to store sets of fields for each query type.
    There are three main sets for each query:
    - all
    - default
    - indexed
    """

    def __init__(self, _all: set, default: set, indexed: set):
        self.all = _all
        self.default = default
        self.indexed = indexed


class Conversion(Enum):
    """
    Class is used to Enumerate conversion types for data frames. When
    converted, a new column will be created with the name *original*_float.
    There are three conversion types:
     CONVERT - convert numeric string columns to float
     NOT_CONVERT - do not convert numeric string columns to float
     CONVERT_DROP_ORIGINAL - convert and drop the original column
    """

    CONVERT = 1
    NOT_CONVERT = 2
    CONVERT_DROP_ORIGINAL = 3


class Client:
    """
    This class is a wrapper around a GraphQL client with
    some additional parameters and methods. It is used to
    execute a single or multiple queries against a GQL endpoint
    """

    def __init__(
        self,
        timeout: int = 30,
        retries: int = 5,
        page_size: int = 1000,
        endpoint_url: str = MAINNET_ENDPOINT_URL,
        conversion_type: str = "convert",
    ):
        self.timeout = timeout
        self.retries = retries
        self.page_size = page_size
        self.endpoint_url = endpoint_url
        self.__gql_client = None
        self.conversion_type = self.__to_conversion_enum(conversion_type)

    def __to_conversion_enum(self, conversion_type):
        """
        description:    used to convert string conversion type into Conversion
                        enum
        exceptions:     throws an exception if provided string conversion type
                        does not match any of the possible Conversion enum types
        """
        if conversion_type == "convert":
            return Conversion.CONVERT
        if conversion_type == "convert_drop_original":
            return Conversion.CONVERT_DROP_ORIGINAL
        if conversion_type == "not_convert":
            return Conversion.NOT_CONVERT
        raise ValueError("Incorrect conversion type provided")

    async def connect_to_endpoint(self):
        """
        description:    used to create a GraphQL client instance and create a
                        connection with the endpoint
        exceptions:     throws an exception if provided endpointURL is invalid
                        or endpoint is not active.
        """
        transport = AIOHTTPTransport(url=self.endpoint_url, timeout=self.timeout)
        client = gqlClient(
            transport=transport, fetch_schema_from_transport=True, execute_timeout=None
        )
        query = gql(
            """
        {
            __schema {
                queryType {
                    name
                }
            }
        }
        """
        )

        self.__gql_client = client
        await self.do_query(query, {})

    def is_connected_to_endpoint(self):
        """
        used to check if a connection to an endpoint was established
        """
        return self.__gql_client is not None

    def get_gql_schema(self):
        """
        used to get a GraphQL schema from the GQL Client instance.
        Note: if a connection to the endpoint was not established (the
        GQL Client instance was not created) this function will throw
        an error
        """
        return self.__gql_client.schema

    async def do_query(self, query: DocumentNode, variables: dict):
        """
        description:    the function is used to perform the actual query
        arguments:      query - the GraphQL query with optional arguments
                        variables - variables to the GraphQL query
        returns:        the query response in a dictionary format
        """
        if not self.__gql_client:
            await self.connect_to_endpoint()

        backoff_in_seconds = 1
        retry_count = 0
        while True:
            try:
                return await self.__gql_client.execute_async(
                    query, variable_values=variables
                )
            except TransportQueryError as query_error:
                logging.warning(" Transport Query Error occurred: %s", str(query_error))
                logging.warning(" Error Query variables: %s", str(variables))
                raise query_error
            except (
                TransportAlreadyConnected,
                TransportClosed,
                TransportServerError,
                TransportProtocolError,
            ) as transport_error:
                logging.warning(" Transport error occurred: %s", str(transport_error))
                if retry_count == self.retries:
                    raise transport_error
                logging.warning(" Retrying ...")
                sleep = backoff_in_seconds * 2**retry_count + random.uniform(0, 1)
                time.sleep(sleep)
                retry_count += 1

    async def do_queries(
        self,
        query: DocumentNode,
        variables: dict,
        page_info_path: str,
        limit: int = None,
        paginating_backwards: bool = False,
    ):
        """description: the function that performs queries in a loop to get all
                    of the pages from the GraphQL endpoint. Stores each page as
                    a dataframe. After all dataframes are collected, they are
                    concatenated into a single one.

        arguments:  client - GraphQL client for querying a specific endpoint
                    query - the GraphQL query with optional arguments
                    predicates - pagination filters (first, last, before, after etc.)
                    variables - optional variables to the GraphQL query
                    page_info_path - the keypath to the pageInfo key in the dictionary
                    that GraphQL library outputs after the query
                    limit - sets the limit on number of records to be returned
                    paginating_backwards - determines the order in which pagination
                                      will be happening

        returns:    a dataframe containing all of the pages from each query
        """
        df_list = []
        another_page_exists = True
        after_cursor = None
        before_cursor = None
        records_num = 0

        while another_page_exists:
            page_size = self.page_size

            if limit is not None:
                records_offset = limit - records_num
                if records_offset == 0:
                    break
                page_size = min(page_size, records_offset)
                records_num += page_size

            if paginating_backwards:
                variables["last"] = page_size
                variables["before"] = before_cursor
            else:
                variables["first"] = page_size
                variables["after"] = after_cursor

            result_dict = await self.do_query(query, variables)
            result_benedict = benedict(result_dict)
            data_frame = pd.json_normalize(
                result_benedict[page_info_path.replace("pageInfo", "nodes")]
            )
            page_info = result_benedict[page_info_path]

            if paginating_backwards:
                before_cursor = page_info["startCursor"]
                another_page_exists = page_info["hasPreviousPage"]
                df_list.append(data_frame.iloc[::-1])
            else:
                after_cursor = page_info["endCursor"]
                another_page_exists = page_info["hasNextPage"]
                df_list.append(data_frame)

        result_df = pd.concat(df_list, ignore_index=True)
        return result_df
