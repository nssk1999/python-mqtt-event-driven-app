#!/usr/bin/env python3
"""
Web Application - Flask app with WebSocket support for real-time MQTT data visualization
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json
import threading
import time
import os
from dotenv import load_dotenv
from mqtt_client import MQTTClient

# Load environment variables
load_dotenv('config.env')

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')

# Initialize SocketIO with cross-platform async mode
try:
    import eventlet  # type: ignore  # noqa: F401
    _async_mode = 'eventlet'
except Exception:
    _async_mode = 'threading'

socketio = SocketIO(app, cors_allowed_origins="*", async_mode=_async_mode)

# Global variables
mqtt_client = None
latest_sensor_data = {}
latest_device_status = {}
message_history = []
max_history = 100

class WebAppMQTTClient:
    """MQTT Client wrapper for the web application"""
    
    def __init__(self):
        self.mqtt_client = MQTTClient("web_app_client")
        self.sensor_topic = os.getenv('MQTT_TOPIC_SENSOR_DATA', 'sensor/data')
        self.status_topic = os.getenv('MQTT_TOPIC_DEVICE_STATUS', 'device/status')
        self.commands_topic = os.getenv('MQTT_TOPIC_COMMANDS', 'device/commands')
        self._connection_attempts = 0
        self._max_connection_attempts = 3
        
        # Register message handlers
        self.mqtt_client.register_handler(self.sensor_topic, self._handle_sensor_data)
        self.mqtt_client.register_handler(self.status_topic, self._handle_device_status)
    
    def _handle_sensor_data(self, topic: str, payload: str):
        """Handle incoming sensor data and emit to WebSocket clients"""
        try:
            data = json.loads(payload)
            global latest_sensor_data, message_history
            
            latest_sensor_data = data
            message_history.append({
                'type': 'sensor_data',
                'timestamp': time.time(),
                'data': data
            })
            
            # Keep only recent messages
            if len(message_history) > max_history:
                message_history.pop(0)
            
            # Emit to all connected WebSocket clients
            socketio.emit('sensor_data', data)
            
        except Exception as e:
            print(f"Error handling sensor data: {e}")
    
    def _handle_device_status(self, topic: str, payload: str):
        """Handle incoming device status and emit to WebSocket clients"""
        try:
            data = json.loads(payload)
            global latest_device_status, message_history
            
            latest_device_status = data
            message_history.append({
                'type': 'device_status',
                'timestamp': time.time(),
                'data': data
            })
            
            # Keep only recent messages
            if len(message_history) > max_history:
                message_history.pop(0)
            
            # Emit to all connected WebSocket clients
            socketio.emit('device_status', data)
            
        except Exception as e:
            print(f"Error handling device status: {e}")
    
    def connect(self):
        """Connect to MQTT broker"""
        if self._connection_attempts >= self._max_connection_attempts:
            print(f"Max connection attempts ({self._max_connection_attempts}) reached")
            return False
            
        try:
            if self.mqtt_client.connect():
                self._connection_attempts = 0  # Reset on successful connection
                self.mqtt_client.subscribe(self.sensor_topic)
                self.mqtt_client.subscribe(self.status_topic)
                print(f"Successfully connected and subscribed to topics")
                return True
            else:
                self._connection_attempts += 1
                print(f"Connection attempt {self._connection_attempts} failed")
                return False
        except Exception as e:
            self._connection_attempts += 1
            print(f"Connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MQTT broker"""
        if self.mqtt_client:
            self.mqtt_client.disconnect()
    
    def publish_command(self, command_data):
        """Publish a command to the commands topic"""
        return self.mqtt_client.publish(self.commands_topic, command_data)
    
    def is_connected(self):
        """Check if MQTT client is connected"""
        try:
            return self.mqtt_client.is_connected()
        except Exception as e:
            print(f"Error checking connection status: {e}")
            return False
    
    def get_connection_info(self):
        """Get detailed connection information"""
        try:
            return {
                'connected': self.mqtt_client.is_connected(),
                'connection_attempts': self._connection_attempts,
                'max_attempts': self._max_connection_attempts,
                'client_id': self.mqtt_client.client_id
            }
        except Exception as e:
            return {'error': str(e)}

# Initialize MQTT client
def init_mqtt():
    """Initialize MQTT client in a separate thread"""
    global mqtt_client
    mqtt_client = WebAppMQTTClient()
    
    # Single connection attempt with better error handling
    try:
        if mqtt_client.connect():
            print("Web app MQTT client connected successfully")
        else:
            print("Failed to connect MQTT client")
    except Exception as e:
        print(f"Error connecting MQTT client: {e}")
    
    # Keep the connection alive
    while True:
        try:
            if mqtt_client and mqtt_client.is_connected():
                time.sleep(5)  # Check connection every 5 seconds
            else:
                print("MQTT client disconnected, attempting to reconnect...")
                if mqtt_client.connect():
                    print("Reconnected successfully")
                time.sleep(10)  # Wait longer before retry
        except Exception as e:
            print(f"Error in MQTT connection loop: {e}")
            time.sleep(10)

# Initialize MQTT client in main thread only
mqtt_client = WebAppMQTTClient()
if mqtt_client.connect():
    print("Main thread MQTT client connected successfully")
else:
    print("Failed to connect main thread MQTT client")

# Don't start additional MQTT threads to avoid conflicts
# mqtt_thread = threading.Thread(target=init_mqtt, daemon=True)
# mqtt_thread.start()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """API endpoint for current status"""
    try:
        connection_info = {}
        if mqtt_client:
            connection_info = mqtt_client.get_connection_info()
        
        return jsonify({
            'mqtt_connected': connection_info.get('connected', False),
            'connection_details': connection_info,
            'latest_sensor_data': latest_sensor_data,
            'latest_device_status': latest_device_status,
            'message_count': len(message_history)
        })
    except Exception as e:
        print(f"Error in status API: {e}")
        return jsonify({
            'mqtt_connected': False,
            'error': str(e),
            'message_count': len(message_history)
        }), 500

@app.route('/api/history')
def api_history():
    """API endpoint for message history"""
    return jsonify(message_history)

@app.route('/api/health')
def api_health():
    """API endpoint for connection health check"""
    try:
        if mqtt_client:
            connection_info = mqtt_client.get_connection_info()
            return jsonify({
                'status': 'healthy' if connection_info.get('connected') else 'unhealthy',
                'mqtt_connection': connection_info,
                'timestamp': int(time.time())
            })
        else:
            return jsonify({'status': 'unhealthy', 'error': 'MQTT client not initialized'}), 503
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/api/send_command', methods=['POST'])
def api_send_command():
    """API endpoint for sending commands"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
            
        command = data.get('command')
        target_device = data.get('target_device', 'sensor_node_001')
        parameters = data.get('parameters', {})
        
        if not command:
            return jsonify({'error': 'Command is required'}), 400
        
        command_data = {
            'command': command,
            'target_device': target_device,
            'parameters': parameters,
            'timestamp': int(time.time())
        }
        
        print(f"Received command request: {command_data}")
        print(f"MQTT client object: {mqtt_client}")
        
        if not mqtt_client:
            return jsonify({'error': 'MQTT client not initialized'}), 503
        
        print(f"MQTT client connected status: {mqtt_client.is_connected()}")
        if not mqtt_client.is_connected():
            return jsonify({'error': 'MQTT client not connected'}), 503
        
        result = mqtt_client.publish_command(command_data)
        if result:
            print(f"Command published successfully: {command_data}")
            return jsonify({'success': True, 'message': 'Command sent successfully'})
        else:
            print(f"Failed to publish command: {command_data}")
            return jsonify({'error': 'Failed to send command'}), 500
            
    except Exception as e:
        print(f"Error in send_command API: {e}")
        return jsonify({'error': str(e)}), 500

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket client connection"""
    print(f"Client connected: {request.sid}")
    
    # Send current data to newly connected client
    if latest_sensor_data:
        emit('sensor_data', latest_sensor_data)
    if latest_device_status:
        emit('device_status', latest_device_status)

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket client disconnection"""
    print(f"Client disconnected: {request.sid}")

@socketio.on('request_data')
def handle_data_request():
    """Handle data request from WebSocket client"""
    emit('sensor_data', latest_sensor_data)
    emit('device_status', latest_device_status)

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    print(f"Starting web application on {host}:{port}")
    print(f"Debug mode: {debug}")
    print(f"SocketIO async_mode: {_async_mode}")

    try:
        socketio.run(app, host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\nShutting down web application...")
        if mqtt_client:
            mqtt_client.disconnect()
