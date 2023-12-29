import pandas as pd
from gql.dsl import DSLQuery, DSLSchema, DSLVariableDefinitions, dsl_gql
from unbounded_data.ethereum.utilities import (
    sort_columns_lexi,
    convert_multiple_columns_to_float,
    handle_null_column,
)
from unbounded_data.ethereum.client import (
    Client,
    RangeFilter,
)
from unbounded_data.ethereum.client import Fields, Conversion


TRANSACTIONS_QUERY_FIELDS = Fields(
    _all={
        "tx_id",
        "block_number",
        "block_hash",
        "from",
        "hash",
        "status",
        "to",
        "tx_index",
        "value",
        "gas_price",
        "gas_limit",
        "nonce",
        "price",
    },
    default={"tx_id", "block_number", "from", "to", "status", "value"},
    indexed={
        "tx_id",
        "block_number",
        "block_hash",
        "from",
        "hash",
        "status",
        "to",
        "tx_index",
        "value",
    },
)

TRANSACTIONS_CONVERTIBLE_COLUMNS = ["price", "value"]


async def transactions_by_address(
    client: Client,
    address: str,
    range_filter: RangeFilter = None,
    transactions_fields: set = TRANSACTIONS_QUERY_FIELDS.default,
    denomination: str = None,
    limit: int = None,
    order_descending: bool = False,
):
    """description: used to query account information and transactions associated with it

    arguments:  client - client for a specific GraphQL endpoint
                address - Ethereum address to get the token info for
                range_filter - a filter for blocks range
                transactions_fields - desired GraphQL query fields set
                denomination - price denomination
                limit - sets the limit on number of records to be returned
                order_descending - determines the order in which pagination
                                      will be happening

    returns:     a tuple containing two dataframes:
                - account information df  (if no account found, exception is thrown)
                - account transactions df (if no transactions, None is returned)

    exceptions:  throws an exception if:
                - Ethereum address is not defined
                - GraphQL client is not defined
                - account is not found
    """

    if not address:
        raise ValueError("The address must be defined")
    if not client:
        raise ValueError("The gql client must be defined")
    if not denomination:
        denomination = "USD"
    if not client.is_connected_to_endpoint():
        await client.connect_to_endpoint()

    account_info_df = await account_info(client, address)

    transactions_query = create_transactions_by_address_query(
        client, transactions_fields
    )
    variables = {
        "address": address,
        "denomination": denomination,
        "rangeFilter": range_filter.to_dict() if range_filter else {},
    }
    transactions_by_address_df = await client.do_queries(
        transactions_query,
        variables,
        "account.transactions.pageInfo",
        limit,
        order_descending,
    )
    if transactions_by_address_df.empty:
        return (account_info_df, None)

    if "to" in transactions_by_address_df.columns:
        transactions_by_address_df = handle_null_column(
            transactions_by_address_df, "to.address", ""
        )
        transactions_by_address_df = transactions_by_address_df.drop("to", axis=1)

    transactions_by_address_df = transactions_by_address_df.rename(
        columns={
            "id": "tx_id",
            "block.number": "block_number",
            "block.hash": "block_hash",
            "from.address": "from",
            "to.address": "to",
            "txIndex": "tx_index",
            "gasPrice": "gas_price",
            "gasLimit": "gas_limit",
        }
    )

    if client.conversion_type in [Conversion.CONVERT, Conversion.CONVERT_DROP_ORIGINAL]:
        transactions_by_address_df = convert_transactions_columns_to_float(
            transactions_by_address_df, client.conversion_type
        )

    return (account_info_df, sort_columns_lexi(transactions_by_address_df))


async def account_info(client: Client, address: str):
    """
     description:   used to query account info

    arguments:      address - Ethereum address of an account

    returns:        dataframe with account info
    """
    if not address:
        raise ValueError("The address must be defined")
    if not client:
        raise ValueError("The gql client must be defined")
    if not client.is_connected_to_endpoint():
        await client.connect_to_endpoint()

    account_info_query = create_account_info_query(client)
    account_info_dict = await client.do_query(
        account_info_query, variables={"address": address}
    )
    account_info_df = sort_columns_lexi(
        pd.json_normalize(account_info_dict).rename(
            columns={
                "account.type": "account_type",
                "account.address": "account_address",
                "account.balance": "account_balance",
            }
        )
    )
    return account_info_df


def create_account_info_query(client: Client):
    """
    description:   used to create a GraphQL query
    returns:        constructed graphql query
    """

    dsl_schema = DSLSchema(client.get_gql_schema())
    variables = DSLVariableDefinitions()
    dsl_query = DSLQuery(
        dsl_schema.Query.account(address=variables.address).select(
            dsl_schema.Account.address,
            dsl_schema.Account.type,
            dsl_schema.Account.balance,
        )
    )
    dsl_query.variable_definitions = variables

    return dsl_gql(dsl_query)


def create_transactions_by_address_query(client: Client, fields_set: set):
    """
     description:   used to create a GraphQL query based on the set of field names

    arguments:      schema - GraphQLSchema that is to be used to select fields from
                    fields_set - set of string field names to be used in the query

    returns:        constructed graphql query
    """

    dsl = DSLSchema(client.get_gql_schema())
    variables = DSLVariableDefinitions()
    dsl_fields_set = []
    fields_map = {
        "tx_id": dsl.Transaction.id,
        "block_number": dsl.Transaction.block.select(dsl.Block.number),
        "block_hash": dsl.Transaction.block.select(dsl.Block.hash),
        "from": getattr(dsl.Transaction, "from").select(dsl.Account.address),
        "hash": dsl.Transaction.hash,
        "status": dsl.Transaction.status,
        "to": dsl.Transaction.to.select(dsl.Account.address),
        "tx_index": dsl.Transaction.txIndex,
        "value": dsl.Transaction.value,
        "gas_limit": dsl.Transaction.gasLimit,
        "gas_price": dsl.Transaction.gasPrice,
        "nonce": dsl.Transaction.nonce,
    }

    if "price" in fields_set:
        fields_map["price"] = dsl.Transaction.price(denomination=variables.denomination)

    for field in fields_set:
        if field not in fields_map:
            raise ValueError(f"field '{field}' does not exist in the schema")
        dsl_fields_set.append(fields_map[field])

    page_info_fields = [
        dsl.PageInfo.hasPreviousPage,
        dsl.PageInfo.startCursor,
        dsl.PageInfo.endCursor,
        dsl.PageInfo.hasNextPage,
    ]

    selected_fields = dsl.Query.account(address=variables.address).select(
        dsl.Account.transactions(
            first=variables.first,
            after=variables.after,
            before=variables.before,
            last=variables.last,
            rangeFilter=variables.rangeFilter,
        ).select(
            dsl.TransactionConnection.nodes.select(*dsl_fields_set),
            dsl.TransactionConnection.pageInfo.select(*page_info_fields),
        )
    )

    dsl_query = DSLQuery(selected_fields)
    dsl_query.variable_definitions = variables
    return dsl_gql(dsl_query)


def convert_transactions_columns_to_float(transactions_df, conversion_type):
    """
    used to convert numeric string columns to float type. If conversion type
    is CONVERT_DROP_ORIGINAL, additionally drop original columns
    """
    return convert_multiple_columns_to_float(
        transactions_df,
        TRANSACTIONS_CONVERTIBLE_COLUMNS,
        conversion_type == Conversion.CONVERT_DROP_ORIGINAL,
    )
