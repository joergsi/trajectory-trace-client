# trajectory-trace-client
Python client for [Trajectory Trace](https://city.app.sdk-cloud.de): 
- Publish trajectory, traffic light, sensor or event data via MQTT
- Query historical data via GraphQL
- Subscribe to live data via GraphQL

## Installation
```bash
pip install git+https://github.com/joergsi/trajectory-trace-client.git

# Without git (e.g. Docker, CI)
pip install "trajectory-trace-client @ https://github.com/joergsi/trajectory-trace-client/archive/refs/heads/main.zip"

# Or pin to a specific release tag, e.g. 0.1.0
pip install "trajectory-trace-client @ https://github.com/joergsi/trajectory-trace-client/archive/refs/tags/v0.1.0.zip"

# Or add to requirements.txt
trajectory-trace-client @ https://github.com/joergsi/trajectory-trace-client/archive/refs/tags/v0.1.0.zip"
```

## Publish data (MQTT)
### Information
- [Documentation for publishing](https://city.app.sdk-cloud.de/docs/user/guide/new_source/)
- [JSON Schema](https://city.app.sdk-cloud.de/api/schema/mqtt-measurements.json)
- [Protobuf Schema](https://city.app.sdk-cloud.de/api/schema/mqtt-measurements.proto)

### Short example
```python
import yaml
from trajectory_trace_client import MQTTClient

with open("config.yaml") as f:
    config = yaml.safe_load(f)

client = MQTTClient(config)
client.publish({
    "measurements": [{
        "tracking_id": 1,
        "time": "2024-10-22T10:25:26+02:00",
        "lat": 48.7751,
        "long": 11.4253,
        "class_id": 2,
    }]
})
client.close()
```

### Full example
- See `examples/config.yaml` for all configuration options and the expected data format.
- See `examples/mqtt_example.py` for a full example.


## Query live/historical data (GraphQL)
### Information
- [GraphQL Overview](https://city.app.sdk-cloud.de/docs/user/GraphQL/overview/)
- [GraphiQL IDE](https://city.app.sdk-cloud.de/docs/user/GraphQL/ide/)

### Short example
```python
from trajectory_trace_client import GraphQLClient, basic_auth

# Connect to client
client = GraphQLClient(
    url="https://city.app.sdk-cloud.de/api/graphql",
    auth=basic_auth("user@example.com", "password"),
)

# Add credentials (optional), to access non public data
auth = basic_auth("user@example.com", "password")

# Query historical data
result = client.query("query { sensors(source: 1) { totalCount } }")

# Live subscription
import asyncio

async def on_data(data):
    print(data)

asyncio.run(client.subscribe(
    "subscription { measurements(source: 1, intervalMs: 100) { trackingId lat long time } }",
    on_data,
))
```

### Full example
See `examples/graphql_example.py` for a full example.



