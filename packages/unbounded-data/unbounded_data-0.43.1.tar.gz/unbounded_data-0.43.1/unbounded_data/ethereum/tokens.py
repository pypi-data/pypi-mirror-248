import pandas as pd
from gql.dsl import DSLQuery, DSLSchema, DSLVariableDefinitions, dsl_gql
from unbounded_data.ethereum.utilities import (
    sort_columns_lexi,
    convert_multiple_columns_to_float,
    handle_null_column,
)
from unbounded_data.ethereum.client import (
    Client,
    Fields,
    Conversion,
)


TOKEN_INFO_QUERY_FIELDS = Fields(
    _all={
        "type",
        "address",
        "symbol",
        "name",
        "decimals",
        "block_number",
        "supply",
        "veracity",
        "price",
    },
    default={
        "type",
        "address",
        "symbol",
        "name",
        "decimals",
        "block_number",
        "supply",
        "veracity",
        "price",
    },
    indexed={
        "type",
        "address",
        "symbol",
        "name",
        "decimals",
        "block_number",
        "supply",
        "veracity",
        "price",
    },
)

TOKEN_CONTRACT_COLUMNS_RENAME_MAP = {
    "account.address": "address",
    "totalSupply.blockNumber": "block_number",
    "totalSupply.supply": "supply",
}

TOKEN_CONTRACT_CONVERTIBLE_COLUMNS = ["supply", "price"]


async def token_info_by_address(
    client: Client,
    address: str,
    token_contract_fields: set = TOKEN_INFO_QUERY_FIELDS.default,
    denomination: str = None,
):
    """description: used to query a token contract info using its address

    arguments:  client - client for a specific GraphQL endpoint
                address - Ethereum address to get the token info for
                token_contract_fields - desired GraphQL query token contract fields set
                denomination - price denomination

    returns:     token info df  (if no contract with this address, exception is thrown)

    exceptions:  throws an exception if:
                - Ethereum address is not defined
                - GraphQL client is not defined
                - Token contract is not found
                - Address does not belong to a contract
    """

    if not client:
        raise ValueError("The gql client must be defined")
    if not address:
        raise ValueError("Address must be defined")
    if not denomination:
        denomination = "USD"
    if not client.is_connected_to_endpoint():
        await client.connect_to_endpoint()

    query = create_token_info_by_address_query(client, token_contract_fields)
    token_contract_dict = await client.do_query(
        query, {"address": address, "denomination": denomination}
    )

    token_contract_df = pd.json_normalize(
        token_contract_dict["account"]["tokenContract"]
    )

    if "totalSupply" in token_contract_df.columns:
        token_contract_df = populate_total_supply_subfields(
            token_contract_df, token_contract_fields
        )

    token_contract_df = token_contract_df.rename(
        columns=TOKEN_CONTRACT_COLUMNS_RENAME_MAP
    )

    if client.conversion_type in [Conversion.CONVERT, Conversion.CONVERT_DROP_ORIGINAL]:
        token_contract_df = convert_token_contract_columns(
            token_contract_df, client.conversion_type
        )

    token_contract_df = create_scaled_columns(token_contract_df)

    return sort_columns_lexi(token_contract_df)


def create_token_info_by_address_query(client: Client, fields_set: set):
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
        "type": dsl.TokenContract.type,
        "address": dsl.TokenContract.account.select(dsl.Account.address),
        "symbol": dsl.TokenContract.symbol,
        "name": dsl.TokenContract.name,
        "decimals": dsl.TokenContract.decimals,
        "block_number": dsl.TokenContract.totalSupply.select(
            dsl.TokenTotalSupply.blockNumber
        ),
        "supply": dsl.TokenContract.totalSupply.select(dsl.TokenTotalSupply.supply),
        "veracity": dsl.TokenContract.veracity,
    }

    if "price" in fields_set:
        fields_map["price"] = dsl.ERC20TokenTransfer.price(
            denomination=variables.denomination
        )

    for field in fields_set:
        if field not in fields_map:
            raise ValueError(f"field '{field}' does not exist in the schema")
        dsl_fields_set.append(fields_map[field])

    selected_fields = dsl.Query.account(address=variables.address).select(
        dsl.Account.tokenContract.select(*dsl_fields_set)
    )

    dsl_query = DSLQuery(selected_fields)
    dsl_query.variable_definitions = variables
    return dsl_gql(dsl_query)


async def token_info_by_symbol(
    client: Client,
    symbol: str,
    token_contract_fields: set = TOKEN_INFO_QUERY_FIELDS.default,
    denomination: str = None,
):
    """description: used to query a token contract info using token symbol (only vetted)

    arguments:  client - client for a specific GraphQL endpoint
                symbol - token symbol
                token_contract_fields - desired GraphQL query token contract fields set
                denomination - price denomination

    returns:    token info df

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

    query = create_token_info_by_symbol_query(client, token_contract_fields)

    token_contract_dict = await client.do_query(
        query,
        {
            "symbol": symbol,
            "filter": {"veracity": "Vetted"},
            "denomination": denomination,
        },
    )

    token_contract_df = pd.json_normalize(
        token_contract_dict["tokenContractsBySymbol"]["nodes"]
    )

    if "totalSupply" in token_contract_df.columns:
        token_contract_df = populate_total_supply_subfields(
            token_contract_df, token_contract_fields
        )

    token_contract_df = token_contract_df.rename(
        columns=TOKEN_CONTRACT_COLUMNS_RENAME_MAP
    )

    if client.conversion_type in [Conversion.CONVERT, Conversion.CONVERT_DROP_ORIGINAL]:
        token_contract_df = convert_token_contract_columns(
            token_contract_df, client.conversion_type
        )

    token_contract_df = create_scaled_columns(token_contract_df)

    return sort_columns_lexi(token_contract_df)


def create_token_info_by_symbol_query(client: Client, fields_set: set):
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
        "type": dsl.TokenContract.type,
        "address": dsl.TokenContract.account.select(dsl.Account.address),
        "symbol": dsl.TokenContract.symbol,
        "name": dsl.TokenContract.name,
        "decimals": dsl.TokenContract.decimals,
        "block_number": dsl.TokenContract.totalSupply.select(
            dsl.TokenTotalSupply.blockNumber
        ),
        "supply": dsl.TokenContract.totalSupply.select(dsl.TokenTotalSupply.supply),
        "veracity": dsl.TokenContract.veracity,
    }

    if "price" in fields_set:
        fields_map["price"] = dsl.TokenContract.price(
            denomination=variables.denomination
        )

    for field in fields_set:
        if field not in fields_map:
            raise ValueError(f"field '{field}' does not exist in the schema")
        dsl_fields_set.append(fields_map[field])

    selected_fields = dsl.Query.tokenContractsBySymbol(
        symbol=variables.symbol, filter=variables.filter
    ).select(dsl.TokenContractConnection.nodes.select(*dsl_fields_set))

    dsl_query = DSLQuery(selected_fields)
    dsl_query.variable_definitions = variables
    return dsl_gql(dsl_query)


def populate_total_supply_subfields(token_contract_df, token_contract_fields):
    """
    used in the case when totalSupply column is null and subfields are required in the
    output. Checks which subfields are required and either populates NaNs with default
    value or in the case when subfield column is not in the data frame, creates the
    column and populates it with the default value.
    """

    if "block_number" in token_contract_fields:
        token_contract_df = handle_null_column(
            token_contract_df, "totalSupply.blockNumber", 0
        )
    if "supply" in token_contract_fields:
        token_contract_df = handle_null_column(
            token_contract_df, "totalSupply.supply", "0"
        )
    token_contract_df = token_contract_df.drop("totalSupply", axis=1)
    return token_contract_df


def convert_token_contract_columns(token_contract_df, conversion_type):
    """
    used to convert numeric string columns to float type. If conversion type
    is CONVERT_DROP_ORIGINAL, additionally drop original columns
    """

    return convert_multiple_columns_to_float(
        token_contract_df,
        TOKEN_CONTRACT_CONVERTIBLE_COLUMNS,
        conversion_type == Conversion.CONVERT_DROP_ORIGINAL,
    )


def create_scaled_columns(token_contract_df):
    """
    used to scale columns of token contract dataframe according to the
    number of decimals
    """
    if "decimals" in token_contract_df:
        decimals = (
            pd.to_numeric(token_contract_df["decimals"], errors="coerce")
            .fillna(0)
            .astype(int)
        )
        if "supply" in token_contract_df:
            token_contract_df["supply_scaled"] = token_contract_df["supply"].astype(
                "float"
            ) / 10 ** (decimals)
        if "price" in token_contract_df:
            token_contract_df["price_scaled"] = token_contract_df["price"].astype(
                "float"
            ) / 10 ** (decimals)

    return token_contract_df
