#!/usr/bin/env python3
"""
MQTT Subscriber - Receives and processes messages from MQTT topics
"""

import json
import time
import signal
import sys
from mqtt_client import MQTTClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

class MessageSubscriber:
    """
    Subscribes to MQTT topics and processes incoming messages
    """
    
    def __init__(self):
        self.mqtt_client = MQTTClient("message_subscriber")
        self.running = False
        
        # Get topics from environment
        self.sensor_topic = os.getenv('MQTT_TOPIC_SENSOR_DATA', 'sensor/data')
        self.status_topic = os.getenv('MQTT_TOPIC_DEVICE_STATUS', 'device/status')
        self.commands_topic = os.getenv('MQTT_TOPIC_COMMANDS', 'device/commands')
        
        # Message counters
        self.message_count = 0
        self.sensor_messages = 0
        self.status_messages = 0
        self.command_messages = 0
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Register message handlers
        self._register_handlers()
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\nReceived signal {signum}, shutting down gracefully...")
        self.stop()
        sys.exit(0)
    
    def _register_handlers(self):
        """Register message handlers for different topics"""
        self.mqtt_client.register_handler(self.sensor_topic, self._handle_sensor_data)
        self.mqtt_client.register_handler(self.status_topic, self._handle_device_status)
        self.mqtt_client.register_handler(self.commands_topic, self._handle_commands)
    
    def _handle_sensor_data(self, topic: str, payload: str):
        """Handle incoming sensor data messages"""
        try:
            data = json.loads(payload)
            self.sensor_messages += 1
            self.message_count += 1
            
            print(f"\n📊 Sensor Data Received (Message #{self.sensor_messages}):")
            print(f"   Device: {data.get('device_id', 'Unknown')}")
            print(f"   Location: {data.get('location', 'Unknown')}")
            print(f"   Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data.get('timestamp', 0)))}")
            
            sensors = data.get('sensors', {})
            for sensor_name, value in sensors.items():
                unit = self._get_sensor_unit(sensor_name)
                print(f"   {sensor_name.capitalize()}: {value} {unit}")
            
            # Process sensor data (example: check for alerts)
            self._check_sensor_alerts(data)
            
        except json.JSONDecodeError as e:
            print(f"Error parsing sensor data: {e}")
        except Exception as e:
            print(f"Error processing sensor data: {e}")
    
    def _handle_device_status(self, topic: str, payload: str):
        """Handle incoming device status messages"""
        try:
            data = json.loads(payload)
            self.status_messages += 1
            self.message_count += 1
            
            print(f"\n📱 Device Status Received (Message #{self.status_messages}):")
            print(f"   Device: {data.get('device_id', 'Unknown')}")
            print(f"   Status: {data.get('status', 'Unknown')}")
            print(f"   Battery: {data.get('battery', 0)}%")
            print(f"   Signal: {data.get('signal_strength', 0)} dBm")
            print(f"   Uptime: {data.get('uptime', 0)} seconds")
            
            # Process device status (example: check battery level)
            self._check_device_alerts(data)
            
        except json.JSONDecodeError as e:
            print(f"Error parsing device status: {e}")
        except Exception as e:
            print(f"Error processing device status: {e}")
    
    def _handle_commands(self, topic: str, payload: str):
        """Handle incoming command messages"""
        try:
            data = json.loads(payload)
            self.command_messages += 1
            self.message_count += 1
            
            print(f"\n🎯 Command Received (Message #{self.command_messages}):")
            print(f"   Command: {data.get('command', 'Unknown')}")
            print(f"   Target: {data.get('target_device', 'Unknown')}")
            print(f"   Parameters: {data.get('parameters', {})}")
            
            # Process commands (example: execute actions)
            self._execute_command(data)
            
        except json.JSONDecodeError as e:
            print(f"Error parsing command: {e}")
        except Exception as e:
            print(f"Error processing command: {e}")
    
    def _get_sensor_unit(self, sensor_name: str) -> str:
        """Get the appropriate unit for a sensor"""
        units = {
            'temperature': '°C',
            'humidity': '%',
            'pressure': 'hPa',
            'light': 'lux'
        }
        return units.get(sensor_name, '')
    
    def _check_sensor_alerts(self, data: dict):
        """Check sensor data for alert conditions"""
        sensors = data.get('sensors', {})
        
        # Temperature alert
        if 'temperature' in sensors:
            temp = sensors['temperature']
            if temp > 30:
                print(f"   ⚠️  HIGH TEMPERATURE ALERT: {temp}°C")
            elif temp < 20:
                print(f"   ⚠️  LOW TEMPERATURE ALERT: {temp}°C")
        
        # Humidity alert
        if 'humidity' in sensors:
            humidity = sensors['humidity']
            if humidity > 75:
                print(f"   ⚠️  HIGH HUMIDITY ALERT: {humidity}%")
            elif humidity < 35:
                print(f"   ⚠️  LOW HUMIDITY ALERT: {humidity}%")
    
    def _check_device_alerts(self, data: dict):
        """Check device status for alert conditions"""
        battery = data.get('battery', 100)
        if battery < 20:
            print(f"   🔋 LOW BATTERY ALERT: {battery}%")
        
        signal = data.get('signal_strength', -30)
        if signal < -50:
            print(f"   📶 WEAK SIGNAL ALERT: {signal} dBm")
    
    def _execute_command(self, data: dict):
        """Execute received commands"""
        command = data.get('command', '').lower()
        target = data.get('target_device', '')
        params = data.get('parameters', {})
        
        print(f"   🚀 Executing command: {command}")
        
        if command == 'restart':
            print(f"   📱 Restarting device: {target}")
        elif command == 'calibrate':
            print(f"   🔧 Calibrating sensors on device: {target}")
        elif command == 'update':
            print(f"   🔄 Updating device: {target} with parameters: {params}")
        else:
            print(f"   ❓ Unknown command: {command}")
    
    def start(self):
        """Start the subscriber"""
        print("Starting MQTT Message Subscriber...")
        
        # Connect to MQTT broker
        if not self.mqtt_client.connect():
            print("Failed to connect to MQTT broker")
            return False
        
        # Subscribe to topics
        self.mqtt_client.subscribe(self.sensor_topic)
        self.mqtt_client.subscribe(self.status_topic)
        self.mqtt_client.subscribe(self.commands_topic)
        
        self.running = True
        
        print(f"Connected to MQTT broker at {self.mqtt_client.broker_host}:{self.mqtt_client.broker_port}")
        print(f"Subscribed to topics:")
        print(f"  - {self.sensor_topic}")
        print(f"  - {self.status_topic}")
        print(f"  - {self.commands_topic}")
        print("Waiting for messages... (Press Ctrl+C to stop)")
        
        try:
            while self.running:
                if self.mqtt_client.is_connected():
                    time.sleep(1)
                else:
                    print("MQTT client disconnected, attempting to reconnect...")
                    time.sleep(5)
                    
        except KeyboardInterrupt:
            print("\nStopping subscriber...")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the subscriber"""
        self.running = False
        if self.mqtt_client:
            self.mqtt_client.disconnect()
        
        print(f"\n📊 Message Summary:")
        print(f"   Total messages: {self.message_count}")
        print(f"   Sensor data: {self.sensor_messages}")
        print(f"   Device status: {self.status_messages}")
        print(f"   Commands: {self.command_messages}")
        print("Subscriber stopped")

def main():
    """Main function"""
    subscriber = MessageSubscriber()
    subscriber.start()

if __name__ == "__main__":
    main()
