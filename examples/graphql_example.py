import asyncio
from trajectory_trace_client import GraphQLClient, basic_auth

client = GraphQLClient(
    url="https://city.app.sdk-cloud.de/api/graphql",
    auth=basic_auth("user@example.com", "password"),
)

# --- Query: fetch traffic participants ---
result = client.query("""
  query entities {
    entities(
        source: 1
        after: "2025-03-24T16:57:12.000Z"
        before: "2025-03-24T16:57:15.000Z"
    ) {
        nodes {
        id
        knownAs
        time
        timeEnd
        count
        class {
            name
        }
        measurements {
            time
            coordinateLongLat
        }
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
    measurements(source: 1, intervalMs: 1000) {
        trackingId
        time
        sensorName
        velocityMs
        data
        lat
        long
        class {
        id
        name
        }
    }
  }
""", on_measurement))
