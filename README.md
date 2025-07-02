# Entity Broadcaster

A Home Assistant custom integration that broadcasts entity state changes over UDP to the local network, allowing external applications to receive real-time updates. Works together with my other custom integration for Home Assistant called Entity Receiver.

## Features

- **Real-time Broadcasting**: Automatically broadcasts entity state changes when they occur
- **Multi-entity Support**: Select multiple entities to broadcast simultaneously
- **Configurable UDP Port**: Choose any available UDP port (1024-65535)
- **Network Broadcasting**: Sends UDP broadcasts to the entire local network
- **JSON Format**: Structured data format for easy parsing by external applications
- **Options Flow**: Modify entity selection and UDP port after initial setup

## Installation

1. Copy this folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Go to Configuration → Integrations
4. Click "+ ADD INTEGRATION"
5. Search for "Entity Broadcaster"
6. Follow the configuration steps

## Configuration

### Step 1: Name Your Broadcaster
Enter a unique name for this broadcaster instance (useful if you want multiple broadcasters).

### Step 2: Select Entities
Choose one or more entities whose state changes you want to broadcast. The interface shows:
- Entity ID
- Friendly name (if available)
- Only enabled entities are shown

### Step 3: Configure Network
Set the UDP port for broadcasting (default: 8888). The integration will verify the port is available.

## Broadcast Message Format

Each broadcast message is a JSON object with the following structure:

```json
{
  "broadcaster_name": "Entity Broadcaster",
  "entity_id": "sensor.temperature",
  "state": "23.5",
  "attributes": {
    "unit_of_measurement": "°C",
    "friendly_name": "Living Room Temperature",
    "device_class": "temperature"
  },
  "timestamp": 1672531200.123
}
```

### Fields Description:
- `broadcaster_name`: Name of the broadcaster instance
- `entity_id`: Home Assistant entity identifier
- `state`: Current state value
- `attributes`: All entity attributes (friendly_name, unit_of_measurement, etc.)
- `timestamp`: Unix timestamp when the broadcast was sent

## Receiving Broadcasts

### Example Python Client

Use the included `example_client.py` to test receiving broadcasts:

```bash
python example_client.py [port]
```

### Custom Implementation

Create a UDP socket to listen for broadcasts:

```python
import socket
import json

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 8888))  # Use your configured port

while True:
    data, addr = sock.recvfrom(4096)
    message = json.loads(data.decode('utf-8'))
    
    print(f"Entity {message['entity_id']} changed to {message['state']}")
```

## Use Cases

- **Home Automation Dashboards**: External displays showing real-time sensor data
- **Mobile Applications**: React to state changes without polling Home Assistant
- **IoT Devices**: Microcontrollers that respond to Home Assistant entity changes
- **Logging Systems**: External databases recording state change history
- **Integration Testing**: Monitor entity changes during development

## Network Considerations

- Broadcasts are sent to the entire local network subnet
- Ensure your firewall allows UDP traffic on the configured port
- The integration also sends to localhost (127.0.0.1) for local testing
- Consider network bandwidth if broadcasting many frequently-changing entities

## Troubleshooting

### Port in Use Error
If you get a "port in use" error:
1. Try a different port number
2. Check if another application is using the port
3. Restart Home Assistant and try again

### No Broadcasts Received
1. Verify the UDP port is correct
2. Check firewall settings
3. Ensure client is on the same network
4. Test with the example client first

### Performance Issues
If experiencing performance problems:
1. Reduce the number of broadcasted entities
2. Avoid high-frequency changing entities (like timestamp sensors)
3. Monitor Home Assistant logs for errors

## Development

The integration consists of:
- `config_flow.py`: Configuration interface
- `broadcaster.py`: Core broadcasting functionality
- `__init__.py`: Integration setup and lifecycle
- `const.py`: Constants and configuration keys

## License

This project is licensed under the Apache License 2.0.
