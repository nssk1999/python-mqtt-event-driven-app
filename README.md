# MQTT Event-Driven Architecture Demo

A comprehensive demonstration of event-driven architecture using Python, MQTT, and modern web technologies. This project showcases how to build a real-time IoT monitoring system with MQTT messaging, Python backend services, and a responsive web dashboard.

## 🏗️ Architecture Overview

This project demonstrates a complete event-driven system with the following components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MQTT Broker  │    │  Python Apps    │    │  Web Dashboard  │
│   (Mosquitto)  │◄──►│  (Publisher &   │◄──►│  (Flask + WS)   │
│                 │    │   Subscriber)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Key Components:

1. **MQTT Broker (Mosquitto)**: Central message broker handling pub/sub communication
2. **Sensor Publisher**: Simulates IoT sensors publishing data to MQTT topics
3. **Message Subscriber**: Processes incoming MQTT messages with event handlers
4. **Web Application**: Real-time dashboard with WebSocket support
5. **Event Handlers**: Demonstrates event-driven message processing

## 🚀 Features

- **Real-time Data Streaming**: Live sensor data updates via MQTT and WebSockets
- **Event-Driven Processing**: Asynchronous message handling with custom event handlers
- **Modern Web UI**: Responsive dashboard built with Tailwind CSS and JavaScript
- **Command Control**: Send commands to IoT devices via MQTT
- **Message History**: Track all MQTT messages with timestamps
- **Alert System**: Automatic alerts for sensor thresholds and device status
- **Scalable Architecture**: Easy to extend with additional sensors and devices

## 📋 Prerequisites

- Python 3.8+
- macOS (for Homebrew installation)
- Git

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd python-mqtt
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and Start MQTT Broker (Mosquitto)

```bash
# Install Mosquitto
brew install mosquitto

# Start Mosquitto service
brew services start mosquitto

# Verify it's running
brew services list | grep mosquitto
```

### 5. Configure Environment

Copy and modify the configuration file:

```bash
cp config.env.example config.env
# Edit config.env with your preferred settings
```

## 🎯 Usage

### Starting the System

The system consists of three main components that can be run independently:

#### 1. Start the Web Application

```bash
# Terminal 1
source venv/bin/activate
python web_app.py
```

The web dashboard will be available at: http://localhost:5000

#### 2. Start the MQTT Publisher (Simulates IoT Sensors)

```bash
# Terminal 2
source venv/bin/activate
python mqtt_publisher.py
```

This will start publishing simulated sensor data every 5 seconds.

#### 3. Start the MQTT Subscriber (Optional - for debugging)

```bash
# Terminal 3
source venv/bin/activate
python mqtt_subscriber.py
```

This will show all incoming MQTT messages in the terminal.

### Running All Components

You can run all components simultaneously using the provided scripts:

```bash
# Start everything (requires multiple terminals)
./start_system.sh

# Or run components individually as shown above
```

## 📊 MQTT Topics

The system uses the following MQTT topics:

- **`sensor/data`**: IoT sensor readings (temperature, humidity, pressure, light)
- **`device/status`**: Device status information (battery, signal, uptime)
- **`device/commands`**: Commands sent to devices (restart, calibrate, update)

### Topic Structure

```
sensor/data
├── timestamp: Unix timestamp
├── device_id: Device identifier
├── location: Sensor location
└── sensors: Object containing sensor values
    ├── temperature: °C
    ├── humidity: %
    ├── pressure: hPa
    └── light: lux

device/status
├── timestamp: Unix timestamp
├── device_id: Device identifier
├── status: Online/Offline
├── battery: Battery percentage
├── signal_strength: Signal strength in dBm
└── uptime: Device uptime in seconds

device/commands
├── timestamp: Unix timestamp
├── command: Command type
├── target_device: Target device ID
└── parameters: Command parameters (JSON)
```

## 🔧 Configuration

### Environment Variables

Edit `config.env` to customize the system:

```env
# MQTT Broker Configuration
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1883
MQTT_BROKER_USERNAME=
MQTT_BROKER_PASSWORD=

# Web Application Configuration
FLASK_SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# MQTT Topics
MQTT_TOPIC_SENSOR_DATA=sensor/data
MQTT_TOPIC_DEVICE_STATUS=device/status
MQTT_TOPIC_COMMANDS=device/commands
```

### MQTT Broker Configuration

Mosquitto configuration file location: `/opt/homebrew/etc/mosquitto/mosquitto.conf`

Common configurations:
- Enable WebSocket support for browser clients
- Configure authentication and TLS
- Set up persistent storage
- Configure logging levels

## 🎨 Web Dashboard Features

### Real-time Monitoring
- Live sensor data visualization
- Device status indicators
- Connection status monitoring
- Message count tracking

### Command Control
- Send device commands via MQTT
- Pre-configured command templates
- Custom command parameters
- Command execution feedback

### Data Visualization
- Responsive grid layout
- Color-coded sensor values
- Interactive charts (future enhancement)
- Historical data display

## 🔍 Troubleshooting

### Common Issues

1. **MQTT Connection Failed**
   - Verify Mosquitto is running: `brew services list | grep mosquitto`
   - Check port 1883 is not blocked
   - Verify network connectivity

2. **Web Dashboard Not Loading**
   - Check Flask app is running on correct port
   - Verify WebSocket connection in browser console
   - Check for JavaScript errors

3. **No Data Appearing**
   - Ensure MQTT publisher is running
   - Check MQTT topics match configuration
   - Verify message format is correct

### Debug Mode

Enable debug logging by setting `FLASK_DEBUG=True` in `config.env` and check terminal output for detailed information.

## 🚀 Extending the System

### Adding New Sensors

1. Modify `mqtt_publisher.py` to include new sensor types
2. Update the web dashboard to display new data
3. Add appropriate units and thresholds

### Custom Event Handlers

1. Extend `mqtt_client.py` with new message handlers
2. Register handlers for new topics
3. Implement business logic for message processing

### Additional MQTT Topics

1. Define new topics in `config.env`
2. Create publishers and subscribers for new topics
3. Update web dashboard to handle new message types

## 📚 Learning Resources

- [MQTT Protocol Specification](https://mqtt.org/specification)
- [Mosquitto Documentation](https://mosquitto.org/documentation/)
- [Paho MQTT Python Client](https://pypi.org/project/paho-mqtt/)
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [Event-Driven Architecture Patterns](https://martinfowler.com/articles/201701-event-driven.html)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Mosquitto team for the excellent MQTT broker
- Paho MQTT team for the Python client library
- Flask and SocketIO communities
- Tailwind CSS for the beautiful UI framework

---

**Happy MQTT-ing! 🚀**
