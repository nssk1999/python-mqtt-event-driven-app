# API Reference

This document describes the public APIs, classes, functions, endpoints, WebSocket events, and frontend components in this repository. It also includes runnable examples.

## Python Modules

### mqtt_client.MQTTClient

Constructor:
- `MQTTClient(client_id: str | None = None)`

Properties:
- `client_id: str` (readonly)
- `broker_host: str` (from `MQTT_BROKER_HOST`, default `localhost`)
- `broker_port: int` (from `MQTT_BROKER_PORT`, default `1883`)
- `connected: bool` (connection state)

Public Methods:
- `connect() -> bool`: Connects to the MQTT broker and starts the network loop. Returns True on success.
- `disconnect() -> None`: Stops loop and disconnects.
- `subscribe(topic: str, qos: int = 0)` -> Any: Subscribes to a topic (returns Paho result tuple).
- `publish(topic: str, message: Any, qos: int = 0, retain: bool = False)` -> Any: Publishes JSON-serializable payloads or strings.
- `register_handler(topic: str, handler: Callable[[str, str], None]) -> None`: Registers a callback per-topic.
- `is_connected() -> bool`: Returns current connection status.
- `get_client_info() -> Dict[str, Any]`: Returns diagnostic info.

Usage Example:
```python
from mqtt_client import MQTTClient

client = MQTTClient("example_client")
if client.connect():
    client.subscribe("sensor/data")
    client.publish("device/commands", {"command": "restart", "target_device": "sensor_node_001"})
```

### mqtt_publisher.SensorDataPublisher

Purpose: Simulates sensors and periodically publishes messages.

Public Methods:
- `start() -> bool | None`: Connects and begins publishing loop.
- `stop() -> None`: Gracefully stops and disconnects.

CLI:
```bash
python mqtt_publisher.py
```

### mqtt_subscriber.MessageSubscriber

Purpose: Subscribes to topics and prints processed messages and simple alerts.

Public Methods:
- `start() -> bool | None`
- `stop() -> None`

CLI:
```bash
python mqtt_subscriber.py
```

### demo.MQTTDemo

Purpose: Interactive CLI to test publishing, sending commands, and viewing messages.

CLI:
```bash
python demo.py
```

## Web Application

Module: `web_app.py` (Flask + Socket.IO)

Environment variables:
- `FLASK_HOST` (default `0.0.0.0`)
- `FLASK_PORT` (default `5000`)
- `FLASK_DEBUG` (default `True`)
- MQTT topics and broker config from `config.env`.

### REST Endpoints

- `GET /` -> HTML dashboard.
- `GET /api/status`
  - Returns: `{ mqtt_connected: bool, connection_details: object, latest_sensor_data: object, latest_device_status: object, message_count: number }`

- `GET /api/history`
  - Returns message history array: `[ { type: 'sensor_data' | 'device_status', timestamp: number, data: object }, ... ]`

- `GET /api/health`
  - Returns: `{ status: 'healthy'|'unhealthy', mqtt_connection: object, timestamp: number }`

- `POST /api/send_command`
  - Body (JSON): `{ command: string, target_device?: string, parameters?: object }`
  - Returns: `{ success: true }` or `{ error: string }`

Example (curl):
```bash
curl -X POST http://localhost:5000/api/send_command \
  -H "Content-Type: application/json" \
  -d '{"command":"restart","target_device":"sensor_node_001","parameters":{"force":true}}'
```

### WebSocket Events (Socket.IO)

Emitted by server:
- `sensor_data` (payload: latest sensor object)
- `device_status` (payload: latest device status object)

Emitted by client (from dashboard):
- `sensor_data_received` (ack that UI received data)
- `device_status_received` (ack that UI received status)

### Frontend Components (static/js/app.js)

Class: `MQTTDashboard`
- Manages Socket.IO connection
- Fetches initial `/api/status`
- Renders sensor/device cards and message history
- Sends commands via `/api/send_command`

Key methods:
- `initializeSocket()`
- `requestInitialData()`
- `handleSensorData(data)` / `handleDeviceStatus(data)`
- `sendCommand()`
- `addToMessageHistory(type, data)`

## Configuration

File: `config.env`
- `MQTT_BROKER_HOST=localhost`
- `MQTT_BROKER_PORT=1883`
- `MQTT_BROKER_USERNAME=`
- `MQTT_BROKER_PASSWORD=`
- `FLASK_SECRET_KEY=...`
- `FLASK_DEBUG=True`
- `FLASK_HOST=0.0.0.0`
- `FLASK_PORT=5000`
- `MQTT_TOPIC_SENSOR_DATA=sensor/data`
- `MQTT_TOPIC_DEVICE_STATUS=device/status`
- `MQTT_TOPIC_COMMANDS=device/commands`

## Cross-Platform Notes

- On Windows, use PowerShell: `venv\Scripts\Activate.ps1` and `python`.
- Socket.IO async mode auto-selects `eventlet` when available, else falls back to `threading` for Windows compatibility.
- Mosquitto install differs by OS; see README for instructions.

