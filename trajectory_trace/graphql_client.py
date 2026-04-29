import requests
import asyncio
from gql import Client, gql
from gql.transport.websockets import WebsocketsTransport


class GraphQLClient:

    def __init__(self, url, auth=None):
        self.url = url
        self.ws_url = url.replace("https://", "wss://").replace("http://", "ws://") + "/ws"
        self.headers = {"Authorization": auth} if auth else {}

    def query(self, body, variables=None):
        payload = {"query": body}
        if variables:
            payload["variables"] = variables
        resp = requests.post(self.url, json=payload, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    async def subscribe(self, body, callback):
        transport = WebsocketsTransport(
            url=self.ws_url,
            subprotocols=["graphql-ws"],
            headers=self.headers,
        )
        async with Client(transport=transport) as session:
            async for result in session.subscribe(gql(body)):
                await callback(result)
