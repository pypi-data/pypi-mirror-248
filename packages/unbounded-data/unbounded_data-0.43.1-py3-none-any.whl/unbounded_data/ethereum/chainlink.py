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

CHAINLINK_PROXY_ANSWERS_QUERY_FIELDS = Fields(
    _all={
        "block_number",
        "timestamp",
        "tx_index",
        "tx_id",
        "log_index",
        "updated_at",
        "round_id",
        "value",
    },
    default={
        "block_number",
        "timestamp",
        "tx_index",
        "tx_id",
        "log_index",
        "updated_at",
        "round_id",
        "value",
    },
    indexed={
        "block_number",
        "timestamp",
        "tx_index",
        "tx_id",
        "log_index",
        "updated_at",
        "round_id",
        "value",
    },
)

CHAINLINK_PROXY_INFO_QUERY_FIELDS = Fields(
    _all={
        "pair",
        "account_address",
        "asset_name",
        "deviation_threshold",
        "heartbeat",
        "decimals",
        "feed_category",
        "feed_type",
    },
    default={
        "pair",
        "account_address",
        "asset_name",
        "deviation_threshold",
        "heartbeat",
        "decimals",
        "feed_category",
        "feed_type",
    },
    indexed={
        "pair",
        "account_address",
        "asset_name",
        "deviation_threshold",
        "heartbeat",
        "decimals",
        "feed_category",
        "feed_type",
    },
)

CHAINLINK_ANSWERS_CONVERTIBLE_COLUMNS = ["round_id", "value"]


async def chainlink_answers_by_pair(
    client: Client,
    pair: str,
    range_filter: RangeFilter = None,
    proxies_fields: set = CHAINLINK_PROXY_INFO_QUERY_FIELDS.default,
    answers_fields: set = CHAINLINK_PROXY_ANSWERS_QUERY_FIELDS.default,
    limit: int = None,
    order_descending: bool = False,
):
    """description: used to query a chainlink proxy using a symbol pair with
                associated answers
    arguments:  client - client for a specific GraphQL endpoint
                pair - pair symbol of chainlink proxy
                proxies_fields - desired GraphQL query proxies fields set
                answers_fields - desired GraphQL query answers fields set
                limit - sets the limit on number of records to be returned
                order_descending - determines the order in which pagination
                                      will be happening

    returns:     a tuple containing two dataframes:
                - proxy info df  (if no info, None is returned)
                - proxy answers df (if no answers, None is returned)

    exceptions:  throws an exception if:
                - GraphQL client is not defined
                - pair is not defined
                - pair symbol corresponds to multiple pairs
    """

    if not client:
        raise ValueError("The gql client must be defined")
    if not pair:
        raise ValueError("Pair symbol must be defined")
    if not client.is_connected_to_endpoint():
        await client.connect_to_endpoint()

    proxy_info_df = await chainlink_proxies_by_pair(client, pair, proxies_fields)

    if proxy_info_df is None:
        return (None, None)

    if len(proxy_info_df.index) > 1:
        raise ValueError(
            "Provided `pair` corresponds to multiple pairs symbols. Make sure it corresponds to only one pair symbol"
        )

    query = create_chainlink_proxy_answers_query(client, answers_fields)
    variables = {
        "filter": {"ticker": pair},
        "rangeFilter": range_filter.to_dict() if range_filter else {},
    }
    result_df = await client.do_queries(
        query,
        variables,
        "chainlinkProxies.nodes[0].answers.pageInfo",
        limit,
        order_descending,
    )

    if result_df.empty:
        return (proxy_info_df, None)

    proxy_answers_df = result_df.rename(
        columns={
            "transaction.block.number": "block_number",
            "transaction.block.timestamp": "timestamp",
            "transaction.id": "tx_id",
            "transaction.txIndex": "tx_index",
            "logIndex": "log_index",
            "updatedAt": "updated_at",
            "roundID": "round_id",
        }
    )

    if client.conversion_type in [Conversion.CONVERT, Conversion.CONVERT_DROP_ORIGINAL]:
        proxy_answers_df = convert_chainlink_answers_columns_to_float(
            proxy_answers_df, client.conversion_type
        )

    proxy_answers_df = convert_multiple_columns_to_timestamp(
        proxy_answers_df, ["timestamp", "updated_at"]
    )

    proxy_answers_df = create_scaled_columns(proxy_answers_df, proxy_info_df)

    return (proxy_info_df, sort_columns_lexi(proxy_answers_df))


async def chainlink_proxies_by_pair(
    client: Client,
    pair_matcher: str,
    proxies_fields: set = CHAINLINK_PROXY_INFO_QUERY_FIELDS.default,
    limit: int = None,
    order_descending: bool = False,
):
    """description: used to query a chainlink proxies using a symbol pair matcher
    arguments:  client - client for a specific GraphQL endpoint
                pair_matcher - a string that is used to match chainlink proxies
                proxies_fields - desired GraphQL query fields set
                limit - sets the limit on number of records to be returned
                order_descending - determines the order in which pagination
                                      will be happening

    returns:    chainlink proxies info df  (if no proxies matched, None is returned)

    exceptions: throws an exception if:
                - GraphQL client is not defined
    """

    if not client:
        raise ValueError("The gql client must be defined")
    if not client.is_connected_to_endpoint():
        await client.connect_to_endpoint()

    query = create_chainlink_proxies_query(client, proxies_fields)
    result_df = await client.do_queries(
        query,
        {"filter": {"ticker": pair_matcher}},
        "chainlinkProxies.pageInfo",
        limit,
        order_descending,
    )

    if result_df.empty:
        return None

    result_df = sort_columns_lexi(
        result_df.rename(
            columns={
                "account.address": "account_address",
                "assetName": "asset_name",
                "deviationThreshold": "deviation_threshold",
                "feedCategory": "feed_category",
                "feedType": "feed_type",
            }
        )
    )
    return result_df


def create_chainlink_proxy_answers_query(client: Client, fields_set: set):
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
        "block_number": dsl.ChainlinkAnswer.transaction.select(
            dsl.Transaction.block.select(dsl.Block.number)
        ),
        "timestamp": dsl.ChainlinkAnswer.transaction.select(
            dsl.Transaction.block.select(dsl.Block.timestamp)
        ),
        "tx_index": dsl.ChainlinkAnswer.transaction.select(dsl.Transaction.txIndex),
        "tx_id": dsl.ChainlinkAnswer.transaction.select(dsl.Transaction.id),
        "log_index": dsl.ChainlinkAnswer.logIndex,
        "updated_at": dsl.ChainlinkAnswer.updatedAt,
        "round_id": dsl.ChainlinkAnswer.roundID,
        "value": dsl.ChainlinkAnswer.value,
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

    selected_fields = dsl.Query.chainlinkProxies(filter=variables.filter).select(
        dsl.ChainlinkProxyConnection.nodes.select(
            dsl.ChainlinkProxy.answers(
                first=variables.first,
                after=variables.after,
                before=variables.before,
                last=variables.last,
                rangeFilter=variables.rangeFilter,
            ).select(
                dsl.ChainlinkAnswerConnection.nodes.select(*dsl_fields_set),
                dsl.ChainlinkAnswerConnection.pageInfo.select(*page_info_fields),
            )
        )
    )

    dsl_query = DSLQuery(selected_fields)
    dsl_query.variable_definitions = variables
    return dsl_gql(dsl_query)


def create_chainlink_proxies_query(client: Client, fields_set: set):
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
        "pair": dsl.ChainlinkProxy.pair,
        "account_address": dsl.ChainlinkProxy.account.select(dsl.Account.address),
        "asset_name": dsl.ChainlinkProxy.assetName,
        "deviation_threshold": dsl.ChainlinkProxy.deviationThreshold,
        "heartbeat": dsl.ChainlinkProxy.heartbeat,
        "decimals": dsl.ChainlinkProxy.decimals,
        "feed_category": dsl.ChainlinkProxy.feedCategory,
        "feed_type": dsl.ChainlinkProxy.feedType,
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

    selected_fields = dsl.Query.chainlinkProxies(
        first=variables.first,
        after=variables.after,
        before=variables.before,
        last=variables.last,
        filter=variables.filter,
    ).select(
        dsl.ChainlinkProxyConnection.nodes.select(*dsl_fields_set),
        dsl.ChainlinkProxyConnection.pageInfo.select(*page_info_fields),
    )
    dsl_query = DSLQuery(selected_fields)
    dsl_query.variable_definitions = variables
    return dsl_gql(dsl_query)


def convert_chainlink_answers_columns_to_float(chainlink_answers_df, conversion_type):
    """
    used to convert numeric string columns to float type. If conversion type
    is CONVERT_DROP_ORIGINAL, additionally drop original columns
    """
    return convert_multiple_columns_to_float(
        chainlink_answers_df,
        CHAINLINK_ANSWERS_CONVERTIBLE_COLUMNS,
        conversion_type == Conversion.CONVERT_DROP_ORIGINAL,
    )


def create_scaled_columns(proxy_answers_df, proxy_info_df):
    """
    used to scale columns of chainlink answers dataframe according to the
    number of decimals
    """
    if "decimals" in proxy_info_df:
        decimals = proxy_info_df["decimals"].fillna(0).loc[0]
        if "value" in proxy_answers_df:
            proxy_answers_df["value_scaled"] = proxy_answers_df["value"].astype(
                "float"
            ) / 10 ** (decimals)

    return proxy_answers_df
