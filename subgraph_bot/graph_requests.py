import requests

URL = 'https://api.thegraph.com/index-node/graphql'


def query(subgraph, method):
    data = { "query": f"{{{method}(subgraphName: \"{subgraph}\") {{ chains {{ latestBlock {{ hash number }} }} }} }}"}
    response = requests.post(URL, json=data)

    response_data = response.json()
    if "errors" in response_data:
        raise Exception(response_data["errors"][0]["message"])
    status_data = response_data["data"][method]

    if status_data is None:
        return None

    latest_block = status_data["chains"][0]["latestBlock"]
    if latest_block:
        block_num = int(latest_block["number"])
    else:
        block_num = 0
    return block_num


def query_current(subgraph):
    return query(subgraph, "indexingStatusForCurrentVersion")


def query_pending(subgraph):
    return query(subgraph, "indexingStatusForPendingVersion")


def query_latest_block_num():
    return query_current("uniswap/uniswap-v2")
