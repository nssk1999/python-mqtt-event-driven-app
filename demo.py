#!/usr/bin/env python3
"""
MQTT Event-Driven Architecture Demo
Interactive demonstration of the MQTT system
"""

import time
import json
import threading
from mqtt_client import MQTTClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

class MQTTDemo:
    """Interactive MQTT demonstration"""
    
    def __init__(self):
        self.mqtt_client = MQTTClient("demo_client")
        self.running = False
        self.message_count = 0
        
        # Get topics from environment
        self.sensor_topic = os.getenv('MQTT_TOPIC_SENSOR_DATA', 'sensor/data')
        self.status_topic = os.getenv('MQTT_TOPIC_DEVICE_STATUS', 'device/status')
        self.commands_topic = os.getenv('MQTT_TOPIC_COMMANDS', 'device/commands')
        
        # Register message handlers
        self.mqtt_client.register_handler(self.sensor_topic, self._handle_sensor_data)
        self.mqtt_client.register_handler(self.status_topic, self._handle_device_status)
        self.mqtt_client.register_handler(self.commands_topic, self._handle_commands)
    
    def _handle_sensor_data(self, topic: str, payload: str):
        """Handle incoming sensor data"""
        try:
            data = json.loads(payload)
            self.message_count += 1
            
            print(f"\n📊 [Message #{self.message_count}] Sensor Data Received:")
            print(f"   Device: {data.get('device_id', 'Unknown')}")
            print(f"   Location: {data.get('location', 'Unknown')}")
            
            sensors = data.get('sensors', {})
            for sensor_name, value in sensors.items():
                unit = self._get_sensor_unit(sensor_name)
                print(f"   {sensor_name.capitalize()}: {value} {unit}")
                
        except Exception as e:
            print(f"Error processing sensor data: {e}")
    
    def _handle_device_status(self, topic: str, payload: str):
        """Handle incoming device status"""
        try:
            data = json.loads(payload)
            self.message_count += 1
            
            print(f"\n📱 [Message #{self.message_count}] Device Status Received:")
            print(f"   Device: {data.get('device_id', 'Unknown')}")
            print(f"   Status: {data.get('status', 'Unknown')}")
            print(f"   Battery: {data.get('battery', 0)}%")
            print(f"   Signal: {data.get('signal_strength', 0)} dBm")
            print(f"   Uptime: {data.get('uptime', 0)} seconds")
            
        except Exception as e:
            print(f"Error processing device status: {e}")
    
    def _handle_commands(self, topic: str, payload: str):
        """Handle incoming commands"""
        try:
            data = json.loads(payload)
            self.message_count += 1
            
            print(f"\n🎯 [Message #{self.message_count}] Command Received:")
            print(f"   Command: {data.get('command', 'Unknown')}")
            print(f"   Target: {data.get('target_device', 'Unknown')}")
            print(f"   Parameters: {data.get('parameters', {})}")
            
        except Exception as e:
            print(f"Error processing command: {e}")
    
    def _get_sensor_unit(self, sensor_name: str) -> str:
        """Get sensor unit"""
        units = {
            'temperature': '°C',
            'humidity': '%',
            'pressure': 'hPa',
            'light': 'lux'
        }
        return units.get(sensor_name, '')
    
    def start(self):
        """Start the demo"""
        print("🚀 MQTT Event-Driven Architecture Demo")
        print("=" * 50)
        
        # Connect to MQTT broker
        print("Connecting to MQTT broker...")
        if not self.mqtt_client.connect():
            print("❌ Failed to connect to MQTT broker")
            return False
        
        # Subscribe to topics
        print("Subscribing to MQTT topics...")
        self.mqtt_client.subscribe(self.sensor_topic)
        self.mqtt_client.subscribe(self.status_topic)
        self.mqtt_client.subscribe(self.commands_topic)
        
        self.running = True
        
        print(f"✅ Connected to MQTT broker at {self.mqtt_client.broker_host}:{self.mqtt_client.broker_port}")
        print(f"📡 Subscribed to topics:")
        print(f"   - {self.sensor_topic}")
        print(f"   - {self.status_topic}")
        print(f"   - {self.commands_topic}")
        
        print("\n🎯 Demo Commands:")
        print("   'send' - Send a test command")
        print("   'publish' - Publish test sensor data")
        print("   'status' - Show connection status")
        print("   'quit' - Exit demo")
        print("\nWaiting for messages... (Messages will appear automatically)")
        
        try:
            while self.running:
                command = input("\n> ").strip().lower()
                
                if command == 'quit':
                    break
                elif command == 'send':
                    self._send_test_command()
                elif command == 'publish':
                    self._publish_test_data()
                elif command == 'status':
                    self._show_status()
                elif command == 'help':
                    self._show_help()
                else:
                    print("Unknown command. Type 'help' for available commands.")
                    
        except KeyboardInterrupt:
            print("\nReceived interrupt signal...")
        finally:
            self.stop()
    
    def _send_test_command(self):
        """Send a test command"""
        command_data = {
            'command': 'test',
            'target_device': 'demo_device',
            'parameters': {
                'test_id': int(time.time()),
                'message': 'Hello from demo!'
            },
            'timestamp': int(time.time())
        }
        
        print(f"📤 Sending test command to {self.commands_topic}...")
        result = self.mqtt_client.publish(self.commands_topic, command_data)
        
        if result:
            print("✅ Test command sent successfully")
        else:
            print("❌ Failed to send test command")
    
    def _publish_test_data(self):
        """Publish test sensor data"""
        sensor_data = {
            'timestamp': int(time.time()),
            'device_id': 'demo_sensor',
            'location': 'demo_room',
            'sensors': {
                'temperature': round(20 + (time.time() % 10), 1),
                'humidity': round(50 + (time.time() % 20), 1),
                'pressure': round(1013 + (time.time() % 10), 1),
                'light': round(500 + (time.time() % 200), 1)
            }
        }
        
        print(f"📤 Publishing test sensor data to {self.sensor_topic}...")
        result = self.mqtt_client.publish(self.sensor_topic, sensor_data)
        
        if result:
            print("✅ Test sensor data published successfully")
        else:
            print("❌ Failed to publish test sensor data")
    
    def _show_status(self):
        """Show current status"""
        print(f"\n📊 Current Status:")
        print(f"   MQTT Connected: {'✅ Yes' if self.mqtt_client.is_connected() else '❌ No'}")
        print(f"   Messages Received: {self.message_count}")
        print(f"   Broker: {self.mqtt_client.broker_host}:{self.mqtt_client.broker_port}")
        print(f"   Client ID: {self.mqtt_client.client_id}")
    
    def _show_help(self):
        """Show help information"""
        print("\n🎯 Available Commands:")
        print("   'send'     - Send a test command to the commands topic")
        print("   'publish'  - Publish test sensor data")
        print("   'status'   - Show current connection and message status")
        print("   'help'     - Show this help message")
        print("   'quit'     - Exit the demo")
        print("\n📡 The demo will automatically display incoming MQTT messages")
        print("   from the subscribed topics.")
    
    def stop(self):
        """Stop the demo"""
        self.running = False
        if self.mqtt_client:
            self.mqtt_client.disconnect()
        print("\n👋 Demo stopped. Goodbye!")

def main():
    """Main function"""
    demo = MQTTDemo()
    demo.start()

if __name__ == "__main__":
    main()
