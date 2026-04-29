# trajectory-trace-client
Python client for [Trajectory Trace](https://city.app.sdk-cloud.de): 
- Publish trajectory, traffic light, sensor or event data via MQTT
- Query historical data via GraphQL
- Subscribe to live data via GraphQL

## Installation
```bash
pip install git+https://techhub-by-efs.ghe.com/EFS/FO00047-trajectory-trace-client.git
```

## Usage
### Publish data (MQTT)
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

See `examples/config.yaml` for all configuration options and the expected data format.

### Query live/historical data (GraphQL)
```python
from trajectory_trace_client import GraphQLClient, basic_auth

client = GraphQLClient(
    url="https://city.app.sdk-cloud.de/api/graphql",
    auth=basic_auth("user@example.com", "password"),
)

# One-shot query
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

See `examples/graphql_example.py` for a full example.

### Credentials
```python
from trajectory_trace_client import basic_auth

auth = basic_auth("user@example.com", "password")
```


