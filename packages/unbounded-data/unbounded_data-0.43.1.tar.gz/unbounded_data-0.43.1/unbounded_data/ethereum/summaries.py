from gql.dsl import DSLQuery, DSLSchema, DSLVariableDefinitions, dsl_gql
from unbounded_data.ethereum.utilities import (
    sort_columns_lexi,
    convert_multiple_columns_to_float,
    convert_multiple_columns_to_timestamp,
)
from unbounded_data.ethereum.client import (
    Client,
    RangeFilter,
    Fields,
    Conversion,
)

BLOCK_SUMMARIES_QUERY_FIELDS = Fields(
    _all={
        "id",
        "block_number",
        "block_hash",
        "block_time",
        "txes",
        "successful_txes",
        "transfer_txes",
        "empty_data_txes",
        "total_eth_value",
        "total_gas_fee",
        "total_gas_price",
        "total_gas_used",
        "gas_limit",
        "difficulty",
        "base_fee",
        "block_rewards",
        "swap_txes",
    },
    default={
        "id",
        "block_number",
        "block_hash",
        "block_time",
        "txes",
        "successful_txes",
        "transfer_txes",
        "empty_data_txes",
        "total_eth_value",
        "total_gas_fee",
        "total_gas_price",
        "total_gas_used",
        "gas_limit",
        "difficulty",
        "base_fee",
        "block_rewards",
        "swap_txes",
    },
    indexed={
        "id",
        "block_number",
        "block_hash",
        "block_time",
        "txes",
        "successful_txes",
        "transfer_txes",
        "empty_data_txes",
        "total_eth_value",
        "total_gas_fee",
        "total_gas_price",
        "total_gas_used",
        "gas_limit",
        "difficulty",
        "base_fee",
        "block_rewards",
        "swap_txes",
    },
)

BLOCK_SUMMARIES_CONVERTIBLE_COLUMNS = [
    "total_eth_value",
    "total_gas_fee",
    "total_gas_price",
    "difficulty",
    "base_fee",
    "block_rewards",
]


async def block_summaries(
    client: Client,
    range_filter: RangeFilter = None,
    block_summaries_fields: set = BLOCK_SUMMARIES_QUERY_FIELDS.default,
    limit: int = None,
    order_descending: bool = False,
):
    """description: used to query block summaries with the use of pagination

    arguments:   client - client for a specific GraphQL endpoint
                 predicates - Pagination object that contains predicates (first, after,
                 last, before) and iteration direction
                 block_summaries_fields - desired GraphQL query fields set
                 limit - sets the limit on number of records to be returned
                 order_descending - determines the order in which pagination will be
                                        happening

    returns:     a dataframe containing block summary

    exceptions:  throws an exception if:
                - GraphQL client is not defined
    """

    if not client:
        raise ValueError("The gql client must be defined")
    if not client.is_connected_to_endpoint():
        await client.connect_to_endpoint()

    query = create_block_summaries_query(client, block_summaries_fields)
    variables = {"rangeFilter": range_filter.to_dict() if range_filter else {}}
    result_df = await client.do_queries(
        query, variables, "blockSummaries.pageInfo", limit, order_descending
    )

    if result_df.empty:
        return None

    block_summaries_df = result_df.rename(
        columns={
            "blockNumber": "block_number",
            "blockHash": "block_hash",
            "blockTime": "block_time",
            "successfulTxes": "successful_txes",
            "transferTxes": "transfer_txes",
            "emptyDataTxes": "empty_data_txes",
            "totalEthValue": "total_eth_value",
            "totalGasFee": "total_gas_fee",
            "totalGasPrice": "total_gas_price",
            "totalGasUsed": "total_gas_used",
            "gasLimit": "gas_limit",
            "baseFee": "base_fee",
            "blockRewards": "block_rewards",
            "swapTxes": "swap_txes",
        }
    )

    if client.conversion_type in [Conversion.CONVERT, Conversion.CONVERT_DROP_ORIGINAL]:
        block_summaries_df = convert_block_summaries_columns(
            block_summaries_df, client.conversion_type
        )

    block_summaries_df = convert_multiple_columns_to_timestamp(
        block_summaries_df, ["block_time"]
    )

    return sort_columns_lexi(block_summaries_df)


def create_block_summaries_query(client: Client, fields_set: set):
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
        "id": dsl.BlockSummary.id,
        "block_number": dsl.BlockSummary.blockNumber,
        "block_hash": dsl.BlockSummary.blockHash,
        "block_time": dsl.BlockSummary.blockTime,
        "txes": dsl.BlockSummary.txes,
        "successful_txes": dsl.BlockSummary.successfulTxes,
        "transfer_txes": dsl.BlockSummary.transferTxes,
        "empty_data_txes": dsl.BlockSummary.emptyDataTxes,
        "total_eth_value": dsl.BlockSummary.totalEthValue,
        "total_gas_fee": dsl.BlockSummary.totalGasFee,
        "total_gas_price": dsl.BlockSummary.totalGasPrice,
        "total_gas_used": dsl.BlockSummary.totalGasUsed,
        "gas_limit": dsl.BlockSummary.gasLimit,
        "difficulty": dsl.BlockSummary.difficulty,
        "base_fee": dsl.BlockSummary.baseFee,
        "block_rewards": dsl.BlockSummary.blockRewards,
        "swap_txes": dsl.BlockSummary.swapTxes,
    }

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

    selected_fields = dsl.Query.blockSummaries(
        first=variables.first,
        after=variables.after,
        last=variables.last,
        before=variables.before,
        rangeFilter=variables.rangeFilter,
    ).select(
        dsl.BlockSummaryConnection.nodes.select(*dsl_fields_set),
        dsl.BlockSummaryConnection.pageInfo.select(*page_info_fields),
    )

    dsl_query = DSLQuery(selected_fields)
    dsl_query.variable_definitions = variables
    return dsl_gql(dsl_query)


def convert_block_summaries_columns(block_summaries_df, conversion_type):
    """
    used to convert numeric string columns to float type. If conversion type
    is CONVERT_DROP_ORIGINAL, additionally drop original column
    """
    return convert_multiple_columns_to_float(
        block_summaries_df,
        BLOCK_SUMMARIES_CONVERTIBLE_COLUMNS,
        conversion_type == Conversion.CONVERT_DROP_ORIGINAL,
    )


async def get_latest_indexed_block_height(client: Client):
    """description: used to query the latests indexed block height

    arguments:   client - client for a specific GraphQL endpoint

    returns:     the height

    exceptions:  throws an exception if:
                - GraphQL client is not defined
    """
    if not client:
        raise ValueError("The gql client must be defined")
    if not client.is_connected_to_endpoint():
        await client.connect_to_endpoint()

    query = create_block_summaries_query(client, {"block_number"})
    variables = {"last": 1, "rangeFilter": {}}
    result_df = await client.do_query(query, variables)
    return result_df["blockSummaries"]["nodes"][0]["blockNumber"]
