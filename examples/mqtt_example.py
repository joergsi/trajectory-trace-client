import yaml
from trajectory_trace_client import MQTTClient

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
            "custom_int": 1,
            "custom_char": "a"
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
