import pandas as pd
from gql.dsl import DSLQuery, DSLSchema, DSLVariableDefinitions, dsl_gql
from unbounded_data.ethereum.tokens import (
    TOKEN_INFO_QUERY_FIELDS,
    token_info_by_address,
    token_info_by_symbol,
)
from unbounded_data.ethereum.utilities import (
    sort_columns_lexi,
    convert_multiple_columns_to_float,
)
from unbounded_data.ethereum.client import (
    Client,
    RangeFilter,
    TokenTransferFilter,
    Fields,
    Conversion,
)

TOKEN_TRANSFERS_QUERY_FIELDS = Fields(
    _all={
        "tx_id",
        "block_number",
        "tx_index",
        "log_index",
        "token_address",
        "from",
        "to",
        "amount",
        "price",
    },
    default={
        "tx_id",
        "block_number",
        "tx_index",
        "log_index",
        "token_address",
        "from",
        "to",
        "amount",
        "price",
    },
    indexed={
        "tx_id",
        "block_number",
        "tx_index",
        "log_index",
        "token_address",
        "from",
        "to",
        "amount",
        "price",
    },
)

TRANSFERS_COLUMNS_RENAME_MAP = {
    "transaction.id": "tx_id",
    "transaction.block.number": "block_number",
    "transaction.txIndex": "tx_index",
    "from.address": "from",
    "to.address": "to",
    "token.account.address": "token_address",
    "token.decimals": "decimals",
    "logIndex": "log_index",
}

TOKEN_TRANSFERS_CONVERTIBLE_COLUMNS = ["price", "amount"]


async def token_transfers_by_address(
    client: Client,
    address: str,
    token_filter: TokenTransferFilter = None,
    range_filter: RangeFilter = None,
    token_contract_fields: set = TOKEN_INFO_QUERY_FIELDS.default,
    token_transfers_fields: set = TOKEN_TRANSFERS_QUERY_FIELDS.default,
    denomination: str = None,
    limit: int = None,
    order_descending: bool = False,
):
    """description: used to query a token contract info and token transfers that
                are associated with the Ethereum contract address

    arguments:  client - client for a specific GraphQL endpoint
                address - Ethereum address to get the token info for
                token_contract_fields - desired GraphQL query token contract fields set
                token_transfers_fields - desired GraphQL query token transfers fields set
                denomination - price denomination
                limit - sets the limit on number of records to be returned
                order_descending - determines the order in which pagination
                                      will be happening

    returns:     a tuple containing two dataframes:
                - token contract df  (if no contract with this address, exception is thrown)
                - token transfers df (if no transfers, None is returned)

    exceptions:  throws an exception if:
                - Ethereum address is not defined
                - GraphQL client is not defined
                - Token contract is not found
                - Address does not belong to a contract
    """

    if not client:
        raise ValueError("The gql client must be defined")
    if not address:
        raise ValueError("Address or symbol must be defined")
    if not denomination:
        denomination = "USD"
    if not client.is_connected_to_endpoint():
        await client.connect_to_endpoint()

    if "amount" in token_transfers_fields:
        token_contract_fields.add("decimals")

    token_info_df = await token_info_by_address(
        client, address, token_contract_fields, denomination
    )

    dsl_fields, variables = select_token_transfers_fields(
        client, token_transfers_fields
    )
    token_transfers_query = create_token_transfers_by_address_query(
        client, dsl_fields, variables
    )
    variables = {
        "address": address,
        "denomination": denomination,
        "rangeFilter": range_filter.to_dict() if range_filter else {},
        "tokenFilter": token_filter.to_dict() if token_filter else {},
    }

    result_df = await client.do_queries(
        token_transfers_query,
        variables,
        "account.tokenContract.erc20TokenTransfers.pageInfo",
        limit,
        order_descending,
    )

    if result_df.empty:
        return (token_info_df, None)

    token_transfers_df = result_df.rename(columns=TRANSFERS_COLUMNS_RENAME_MAP)

    token_transfers_df = create_scaled_columns(token_transfers_df)

    if "token_address" in token_transfers_df:
        token_transfers_df = convert_token_address_to_category(token_transfers_df)

    if client.conversion_type in [Conversion.CONVERT, Conversion.CONVERT_DROP_ORIGINAL]:
        token_transfers_df = convert_token_transfers_columns_to_float(
            token_transfers_df, client.conversion_type
        )

    token_transfers_df = sort_columns_lexi(token_transfers_df)

    return (token_info_df, token_transfers_df)


def select_token_transfers_fields(client: Client, fields_set: set):
    """
    description:    this function allows to select dsl fields based on the provided
                    set of string field names.

    arguments:      schema - GraphQLSchema that is to be used to select fields from
                    fields_set - set of string names of fields to be selected

    returns:        dsl_fields_set - set of selected dsl fields
                    variables - dsl variable definitions used with the fields
    """

    dsl = DSLSchema(client.get_gql_schema())
    variables = DSLVariableDefinitions()
    dsl_fields_set = []
    fields_map = {
        "tx_id": dsl.ERC20TokenTransfer.transaction.select(dsl.Transaction.id),
        "block_number": dsl.ERC20TokenTransfer.transaction.select(
            dsl.Transaction.block.select(dsl.Block.number)
        ),
        "tx_index": dsl.ERC20TokenTransfer.transaction.select(dsl.Transaction.txIndex),
        "log_index": dsl.ERC20TokenTransfer.logIndex,
        "token_address": dsl.ERC20TokenTransfer.token.select(
            dsl.TokenContract.account.select(dsl.Account.address),
        ),
        "from": getattr(dsl.ERC20TokenTransfer, "from").select(dsl.Account.address),
        "to": dsl.ERC20TokenTransfer.to.select(dsl.Account.address),
        "amount": dsl.ERC20TokenTransfer.amount,
    }

    if any(item in ["amount", "price"] for item in fields_set):
        dsl_fields_set.append(
            dsl.ERC20TokenTransfer.token.select(dsl.TokenContract.decimals)
        )

    if "price" in fields_set:
        fields_map["price"] = dsl.ERC20TokenTransfer.price(
            denomination=variables.denomination
        )

    for field in fields_set:
        if field not in fields_map:
            raise ValueError(f"field '{field}' does not exist in the schema")
        dsl_fields_set.append(fields_map[field])

    return (dsl_fields_set, variables)


def create_token_transfers_by_address_query(
    client: Client, dsl_fields: list, variables: DSLVariableDefinitions
):
    """
     description:   used to create a GraphQL query based on dsl fields and variables

    arguments:      schema - GraphQLSchema that is to be used to select fields from
                    dsl_fields - list of dsl fields for the query
                    variables - dsl variables for the query

    returns:        constructed graphql query
    """
    dsl = DSLSchema(client.get_gql_schema())

    page_info_fields = [
        dsl.PageInfo.hasPreviousPage,
        dsl.PageInfo.startCursor,
        dsl.PageInfo.endCursor,
        dsl.PageInfo.hasNextPage,
    ]

    selected_fields = dsl.Query.account(address=variables.address).select(
        dsl.Account.tokenContract.select(
            dsl.TokenContract.erc20TokenTransfers(
                first=variables.first,
                after=variables.after,
                before=variables.before,
                last=variables.last,
                rangeFilter=variables.rangeFilter,
                filter=variables.tokenFilter,
            ).select(
                dsl.ERC20TokenTransferConnection.nodes.select(*dsl_fields),
                dsl.ERC20TokenTransferConnection.pageInfo.select(*page_info_fields),
            )
        )
    )

    dsl_query = DSLQuery(selected_fields)
    dsl_query.variable_definitions = variables
    return dsl_gql(dsl_query)


async def token_transfers_by_symbol(
    client: Client,
    symbol: str,
    token_filter: TokenTransferFilter = None,
    range_filter: RangeFilter = None,
    token_contract_fields: set = TOKEN_INFO_QUERY_FIELDS.default,
    token_transfers_fields: set = TOKEN_TRANSFERS_QUERY_FIELDS.default,
    denomination: str = None,
    limit: int = None,
    order_descending: bool = False,
):
    """description: used to query a token contract info and token transfers that
                are associated with a token symbol (only vetted)

    arguments:  client - client for a specific GraphQL endpoint
                symbol - token symbol
                token_contract_fields - desired GraphQL query token contract fields set
                token_transfers_fields - desired GraphQL query token transfers fields set
                denomination - price denomination
                limit - sets the limit on number of records to be returned
                order_descending - determines the order in which pagination
                                      will be happening

    returns:     a tuple containing two dataframes:
                - token contract df
                - token transfers df (if no transfers, None is returned)

    exceptions:  throws an exception if:
                - Ethereum address is not defined
                - GraphQL client is not defined
                - Token contract is not found
    """
    if not client:
        raise ValueError("The gql client must be defined")
    if not symbol:
        raise ValueError("Symbol must be defined")
    if not denomination:
        denomination = "USD"
    if not client.is_connected_to_endpoint():
        await client.connect_to_endpoint()

    token_info_df = await token_info_by_symbol(
        client, symbol, token_contract_fields, denomination
    )

    dsl_fields, variables = select_token_transfers_fields(
        client, token_transfers_fields
    )
    token_transfers_query = create_token_transfers_by_symbol_query(
        client, dsl_fields, variables
    )
    variables = {
        "symbol": symbol,
        "filter": {"veracity": "Vetted"},
        "denomination": denomination,
        "rangeFilter": range_filter.to_dict() if range_filter else {},
        "tokenFilter": token_filter.to_dict() if token_filter else {},
    }
    result_df = await client.do_queries(
        token_transfers_query,
        variables,
        "tokenContractsBySymbol.nodes[0].erc20TokenTransfers.pageInfo",
        limit,
        order_descending,
    )

    if result_df.empty:
        return (token_info_df, None)

    token_transfers_df = result_df.rename(columns=TRANSFERS_COLUMNS_RENAME_MAP)

    if "decimals" in token_transfers_df:
        token_transfers_df = create_scaled_columns(token_transfers_df)

    if "token_address" in token_transfers_df:
        token_transfers_df = convert_token_address_to_category(token_transfers_df)

    if client.conversion_type in [Conversion.CONVERT, Conversion.CONVERT_DROP_ORIGINAL]:
        token_transfers_df = convert_token_transfers_columns_to_float(
            token_transfers_df, client.conversion_type
        )

    token_transfers_df = sort_columns_lexi(token_transfers_df)

    return (token_info_df, token_transfers_df)


def create_token_transfers_by_symbol_query(
    client: Client, dsl_fields: set, variables: DSLVariableDefinitions
):
    """
     description:   used to create a GraphQL query based on the set of field names

    arguments:      schema - GraphQLSchema that is to be used to select fields from
                    fields_set - set of string field names to be used in the query

    returns:        constructed graphql query
    """

    dsl = DSLSchema(client.get_gql_schema())

    page_info_fields = [
        dsl.PageInfo.hasPreviousPage,
        dsl.PageInfo.startCursor,
        dsl.PageInfo.endCursor,
        dsl.PageInfo.hasNextPage,
    ]

    selected_fields = dsl.Query.tokenContractsBySymbol(
        symbol=variables.symbol, filter=variables.filter
    ).select(
        dsl.TokenContractConnection.nodes.select(
            dsl.TokenContract.erc20TokenTransfers(
                first=variables.first,
                after=variables.after,
                before=variables.before,
                last=variables.last,
                rangeFilter=variables.rangeFilter,
                filter=variables.tokenFilter,
            ).select(
                dsl.ERC20TokenTransferConnection.nodes.select(*dsl_fields),
                dsl.ERC20TokenTransferConnection.pageInfo.select(*page_info_fields),
            )
        )
    )

    dsl_query = DSLQuery(selected_fields)
    dsl_query.variable_definitions = variables
    return dsl_gql(dsl_query)


async def account_token_transfers(
    client: Client,
    address: str,
    token_filter: TokenTransferFilter = None,
    range_filter: RangeFilter = None,
    token_contract_fields: set = TOKEN_INFO_QUERY_FIELDS.default,
    token_transfers_fields: set = TOKEN_TRANSFERS_QUERY_FIELDS.default,
    denomination: str = None,
    limit: int = None,
    order_descending: bool = False,
):
    """description: used to query account's token transfers

    arguments:  client - client for a specific GraphQL endpoint
                address - Ethereum address
                token_contract_fields - desired GraphQL query fields for token info
                transfers_fields - desired GraphQL query fields for account
                denomination - price denomination
                limit - sets the limit on number of records to be returned
                order_descending - determines the order in which pagination
                                      will be happening

    returns:     a tuple containing two dataframes:
                - token info df  (if no account found, empty df is returned)
                - account token transfers df (if none, None is returned)

    exceptions:  throws an exception if:
                - Ethereum address is not defined
                - GraphQL client is not defined
    """

    if not address:
        raise ValueError("The address must be defined")
    if not client:
        raise ValueError("The gql client must be defined")
    if not denomination:
        denomination = "USD"
    if not client.is_connected_to_endpoint():
        await client.connect_to_endpoint()

    dsl_fields, variables = select_token_transfers_fields(
        client, token_transfers_fields
    )
    token_transfers_query = create_account_token_transfers_query(
        client, dsl_fields, variables
    )
    variables = {
        "address": address,
        "denomination": denomination,
        "rangeFilter": range_filter.to_dict() if range_filter else {},
        "filter": token_filter.to_dict() if token_filter else {},
    }
    result_df = await client.do_queries(
        token_transfers_query,
        variables,
        "account.erc20TokenTransfers.pageInfo",
        limit,
        order_descending,
    )
    token_info_df = pd.DataFrame(columns=list(TOKEN_INFO_QUERY_FIELDS.default))

    if result_df.empty:
        return (token_info_df, pd.DataFrame(columns=list(token_transfers_fields)))

    token_transfers_df = result_df.rename(columns=TRANSFERS_COLUMNS_RENAME_MAP)

    if "decimals" in token_transfers_df:
        token_transfers_df = create_scaled_columns(token_transfers_df)

    if "token_address" in token_transfers_df:
        token_transfers_df = convert_token_address_to_category(token_transfers_df)
        if "amount" in token_transfers_fields:
            token_contract_fields.add("decimals")
        contract_addresses = token_transfers_df[
            "token_address"
        ].cat.categories.values.tolist()
        token_info_list = []

        for contract_addr in contract_addresses:
            data_frame = await token_info_by_address(
                client, contract_addr, token_contract_fields
            )
            token_info_list.append(data_frame)

        token_info_df = pd.concat(token_info_list)

    if client.conversion_type in [Conversion.CONVERT, Conversion.CONVERT_DROP_ORIGINAL]:
        token_transfers_df = convert_token_transfers_columns_to_float(
            token_transfers_df, client.conversion_type
        )

    token_transfers_df = sort_columns_lexi(token_transfers_df)

    return (token_info_df, token_transfers_df)


def create_account_token_transfers_query(
    client: Client, dsl_fields: set, variables: DSLVariableDefinitions
):
    """
     description:   used to create a GraphQL query based on the set of field names

    arguments:      schema - GraphQLSchema that is to be used to select fields from
                    fields_set - set of string field names to be used in the query

    returns:        constructed graphql query
    """

    dsl = DSLSchema(client.get_gql_schema())

    page_info_fields = [
        dsl.PageInfo.hasPreviousPage,
        dsl.PageInfo.startCursor,
        dsl.PageInfo.endCursor,
        dsl.PageInfo.hasNextPage,
    ]

    selected_fields = dsl.Query.account(address=variables.address).select(
        dsl.Account.erc20TokenTransfers(
            first=variables.first,
            after=variables.after,
            before=variables.before,
            last=variables.last,
            rangeFilter=variables.rangeFilter,
            filter=variables.filter,
        ).select(
            dsl.ERC20TokenTransferConnection.nodes.select(*dsl_fields),
            dsl.ERC20TokenTransferConnection.pageInfo.select(*page_info_fields),
        )
    )

    dsl_query = DSLQuery(selected_fields)
    dsl_query.variable_definitions = variables
    return dsl_gql(dsl_query)


def create_scaled_columns(transfers_df):
    """
    used to scale columns of token transfers dataframe according to the
    number of decimals
    """
    if "decimals" in transfers_df:
        decimals = (
            pd.to_numeric(transfers_df["decimals"], errors="coerce")
            .fillna(0)
            .astype(int)
        )
        if "amount" in transfers_df:
            transfers_df["amount_scaled"] = transfers_df["amount"].astype(
                "float"
            ) / 10 ** (decimals)
        if "price" in transfers_df:
            transfers_df["price_scaled"] = transfers_df["price"].astype(
                "float"
            ) / 10 ** (decimals)

    return transfers_df


def convert_token_address_to_category(transfers_df):
    """
    used to convert a token address field of token transfers dataframe to
    a category type
    """
    transfers_df["token_address"] = transfers_df["token_address"].astype("category")
    return transfers_df


def convert_token_transfers_columns_to_float(token_transfers_df, conversion_type):
    """
    used to convert numeric string columns to float type. If conversion type
    is CONVERT_DROP_ORIGINAL, additionally drop original columns
    """
    return convert_multiple_columns_to_float(
        token_transfers_df,
        TOKEN_TRANSFERS_CONVERTIBLE_COLUMNS,
        conversion_type == Conversion.CONVERT_DROP_ORIGINAL,
    )
