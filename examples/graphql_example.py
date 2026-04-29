import asyncio
from trajectory_trace import GraphQLClient

client = GraphQLClient(
    url="https://city.app.sdk-cloud.de/api/graphql",
    auth="Basic <your-base64-credentials>",
)

# --- Query: fetch sensors ---
result = client.query("""
  query {
    sensors(source: 1) {
      totalCount
      nodes {
        id
        time
        knownAs
        class { name }
      }
    }
  }
""")
print(result)


# --- Subscription: live measurements ---
async def on_measurement(data):
    print(data)

asyncio.run(client.subscribe("""
  subscription {
    measurements(source: 1, intervalMs: 100) {
      trackingId
      lat
      long
      time
    }
  }
""", on_measurement))
