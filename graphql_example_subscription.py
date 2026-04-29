import asyncio, json
from gql import Client, gql
from gql.transport.websockets import WebsocketsTransport

# For access to non public sources you can generate the Basic Auth Header with 
# Username and Password here https://www.debugbear.com/basic-auth-header-generator
# For acces to public sources, just leave it as it is

# basic_auth = "Basic yourBase64encodedusernameandpassword"
basic_auth = "Basic YWRtaW5AYWRtaW4ubG9jYWw6dGVzdDEyMw=="       # for local

# Websockets transport
transport = WebsocketsTransport(
    # url = "wss://disrupt.sdk.efs.ai/api/graphql/ws", 
    url = "ws://localhost:8080/api/graphql/ws",                 # for local
		subprotocols = ["graphql-ws"],
    headers = {"Authorization": basic_auth}
	)

# Query
body = """
  subscription subscription{
    measurements(source:1 intervalMs:100) {
      trackingId
      long
      lat
      time
    }
  }
"""

async def subscribe():
    async with Client(transport=transport) as session:
        async for result in session.subscribe(gql(body)):
            print("New Data Received:", result)
            #with open('subscription.json', 'w') as f:
            #    json.dump(result, f, indent=4)

# Run the subscription
asyncio.run(subscribe())
