# Project Structure

This document provides an overview of the project structure and explains the purpose of each file and directory.

## 📁 Directory Structure

```
python-mqtt/
├── venv/                          # Python virtual environment
├── templates/                     # Flask HTML templates
│   └── index.html                # Main web dashboard template
├── static/                        # Static web assets
│   ├── css/
│   │   └── style.css             # Custom CSS styles
│   └── js/
│       └── app.js                # Frontend JavaScript application
├── mqtt_client.py                 # Core MQTT client class
├── mqtt_publisher.py             # MQTT publisher (simulates IoT sensors)
├── mqtt_subscriber.py            # MQTT subscriber (processes messages)
├── web_app.py                    # Flask web application with WebSocket support
├── test_mqtt.py                  # MQTT connection test script
├── demo.py                       # Interactive demo script
├── start_system.sh               # System startup script
├── requirements.txt               # Python dependencies
├── config.env                    # Environment configuration
├── README.md                     # Project documentation
└── PROJECT_STRUCTURE.md          # This file
```

## 🔧 Core Components

### MQTT Infrastructure

- **`mqtt_client.py`**: Core MQTT client implementation
  - Handles connections, publishing, subscribing
  - Implements event-driven message handling
  - Provides connection management and error handling

- **`mqtt_publisher.py`**: Simulates IoT sensor data
  - Generates realistic sensor readings (temperature, humidity, pressure, light)
  - Publishes data to MQTT topics at regular intervals
  - Demonstrates event-driven data generation

- **`mqtt_subscriber.py`**: Processes incoming MQTT messages
  - Subscribes to multiple topics
  - Implements custom event handlers for different message types
  - Shows real-time message processing

### Web Application

- **`web_app.py`**: Flask web server with WebSocket support
  - RESTful API endpoints for data access
  - WebSocket integration for real-time updates
  - MQTT client integration for web dashboard

- **`templates/index.html`**: Main web dashboard
  - Responsive design with Tailwind CSS
  - Real-time data visualization
  - Command control interface

- **`static/css/style.css`**: Custom styling
  - Enhanced visual appearance
  - Responsive design improvements
  - Custom animations and transitions

- **`static/js/app.js`**: Frontend application logic
  - WebSocket connection management
  - Real-time data updates
  - User interaction handling

### Configuration & Setup

- **`config.env`**: Environment configuration
  - MQTT broker settings
  - Web application configuration
  - Topic definitions

- **`requirements.txt`**: Python dependencies
  - All required packages with versions
  - Ensures consistent environment setup

## 🚀 Utility Scripts

### Testing & Development

- **`test_mqtt.py`**: System testing script
  - Tests MQTT connectivity
  - Verifies environment configuration
  - Checks Python dependencies

- **`demo.py`**: Interactive demonstration
  - Command-line interface for testing
  - Manual message publishing/subscribing
  - System status monitoring

### System Management

- **`start_system.sh`**: Automated startup script
  - Launches all system components
  - Opens separate terminal windows
  - Provides startup status information

## 📊 MQTT Topics

The system uses three main MQTT topics for communication:

1. **`sensor/data`**: IoT sensor readings
2. **`device/status`**: Device status information  
3. **`device/commands`**: Device control commands

## 🔄 Data Flow

```
IoT Sensors → MQTT Publisher → MQTT Broker → MQTT Subscriber
                ↓                    ↓              ↓
            Web App ←────────── WebSocket ←────── Browser
```

## 🎯 Key Features

### Event-Driven Architecture
- Asynchronous message processing
- Custom event handlers for different message types
- Scalable topic-based communication

### Real-Time Updates
- WebSocket integration for live data
- Automatic UI updates
- Message history tracking

### Command & Control
- Device command interface
- Pre-configured command templates
- Real-time command execution

### Monitoring & Debugging
- Connection status indicators
- Message counters
- Comprehensive logging

## 🛠️ Development Workflow

1. **Setup**: Install dependencies and configure environment
2. **Testing**: Run `test_mqtt.py` to verify system readiness
3. **Development**: Use `demo.py` for interactive testing
4. **Production**: Use `start_system.sh` for full system launch

## 🔍 File Dependencies

### Core Dependencies
- `mqtt_client.py` ← Used by all other Python files
- `config.env` ← Configuration for all components
- `requirements.txt` ← Dependencies for all Python files

### Web Application Dependencies
- `web_app.py` ← Depends on `mqtt_client.py`
- `templates/index.html` ← Depends on `static/js/app.js`
- `static/js/app.js` ← Depends on Flask API endpoints

### MQTT Components Dependencies
- `mqtt_publisher.py` ← Depends on `mqtt_client.py`
- `mqtt_subscriber.py` ← Depends on `mqtt_client.py`
- `demo.py` ← Depends on `mqtt_client.py`

## 📝 File Purposes Summary

| File | Purpose | Dependencies |
|------|---------|--------------|
| `mqtt_client.py` | Core MQTT functionality | `paho-mqtt`, `python-dotenv` |
| `mqtt_publisher.py` | Simulate IoT sensors | `mqtt_client.py` |
| `mqtt_subscriber.py` | Process MQTT messages | `mqtt_client.py` |
| `web_app.py` | Web dashboard server | `mqtt_client.py`, `flask`, `flask-socketio` |
| `index.html` | Web dashboard UI | `app.js`, `style.css` |
| `app.js` | Frontend logic | WebSocket API |
| `style.css` | Custom styling | None |
| `test_mqtt.py` | System testing | `mqtt_client.py` |
| `demo.py` | Interactive demo | `mqtt_client.py` |
| `start_system.sh` | System startup | All Python files |
| `config.env` | Configuration | Used by all Python files |
| `requirements.txt` | Dependencies | Python package manager |

## 🚀 Getting Started

1. **Clone and setup**: Follow README.md installation instructions
2. **Test system**: Run `python test_mqtt.py`
3. **Try demo**: Run `python demo.py`
4. **Launch full system**: Run `./start_system.sh`
5. **Access dashboard**: Open http://localhost:5000 in browser

## 🔧 Customization

- **Add new sensors**: Modify `mqtt_publisher.py`
- **New message types**: Update topic handlers in `mqtt_client.py`
- **UI changes**: Edit `templates/index.html` and `static/` files
- **Configuration**: Modify `config.env` for different settings
