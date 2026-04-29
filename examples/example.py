"""
Basic usage example for disrupt-mqtt-client.

This example shows how to:
1. Load configuration from a YAML file
2. Create an MQTT client
3. Publish a single message
4. Close the connection properly
"""

import yaml
from disrupt_mqtt import MQTTClient

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Create MQTT client
mqtt_client = MQTTClient(config)

# Prepare data to publish (measurements format)
data = {
    "measurements": [{
        "tracking_id": 1001,
        "time": "2024-12-18T10:30:45.123000+01:00",
        "lat": 48.7758,
        "long": 11.4297,
        "class_id": 2,  # Car
        "heading": 90.0,
        "velocity_ms": 13.9,  # ~50 km/h
        "data": {
            "source": "example"
        }
    }]
}

# Publish the data
print("Publishing data to MQTT broker...")
success = mqtt_client.publish(data)

if success:
    print("✓ Data published successfully!")
else:
    print("✗ Failed to publish data")

# Close connection
mqtt_client.close()
print("Connection closed")
