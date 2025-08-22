#!/usr/bin/env python3
"""
MQTT Publisher - Simulates IoT sensor data and publishes to MQTT topics
"""

import time
import random
import json
import signal
import sys
from mqtt_client import MQTTClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

class SensorDataPublisher:
    """
    Simulates IoT sensors and publishes data to MQTT topics
    """
    
    def __init__(self):
        self.mqtt_client = MQTTClient("sensor_publisher")
        self.running = False
        
        # Get topics from environment
        self.sensor_topic = os.getenv('MQTT_TOPIC_SENSOR_DATA', 'sensor/data')
        self.status_topic = os.getenv('MQTT_TOPIC_DEVICE_STATUS', 'device/status')
        
        # Sensor simulation parameters
        self.sensors = {
            'temperature': {'min': 18.0, 'max': 32.0, 'current': 25.0},
            'humidity': {'min': 30.0, 'max': 80.0, 'current': 55.0},
            'pressure': {'min': 1000.0, 'max': 1020.0, 'current': 1013.0},
            'light': {'min': 0.0, 'max': 1000.0, 'current': 500.0}
        }
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\nReceived signal {signum}, shutting down gracefully...")
        self.stop()
        sys.exit(0)
    
    def _generate_sensor_data(self):
        """Generate realistic sensor data with gradual changes"""
        data = {}
        timestamp = int(time.time())
        
        for sensor_name, sensor_config in self.sensors.items():
            # Add some randomness and gradual drift
            drift = random.uniform(-0.5, 0.5)
            sensor_config['current'] += drift
            
            # Keep within bounds
            sensor_config['current'] = max(sensor_config['min'], 
                                        min(sensor_config['max'], 
                                            sensor_config['current']))
            
            # Add some noise
            noise = random.uniform(-0.1, 0.1)
            value = sensor_config['current'] + noise
            
            data[sensor_name] = round(value, 2)
        
        return {
            'timestamp': timestamp,
            'device_id': 'sensor_node_001',
            'location': 'room_101',
            'sensors': data
        }
    
    def _generate_device_status(self):
        """Generate device status information"""
        return {
            'timestamp': int(time.time()),
            'device_id': 'sensor_node_001',
            'status': 'online',
            'battery': random.randint(80, 100),
            'signal_strength': random.randint(-60, -30),
            'uptime': int(time.time()) - self.start_time
        }
    
    def start(self):
        """Start the publisher"""
        print("Starting MQTT Sensor Data Publisher...")
        
        # Connect to MQTT broker
        if not self.mqtt_client.connect():
            print("Failed to connect to MQTT broker")
            return False
        
        self.running = True
        self.start_time = time.time()
        
        print(f"Connected to MQTT broker at {self.mqtt_client.broker_host}:{self.mqtt_client.broker_port}")
        print(f"Publishing sensor data to topic: {self.sensor_topic}")
        print(f"Publishing device status to topic: {self.status_topic}")
        print("Press Ctrl+C to stop...")
        
        try:
            while self.running:
                if self.mqtt_client.is_connected():
                    # Generate and publish sensor data
                    sensor_data = self._generate_sensor_data()
                    self.mqtt_client.publish(self.sensor_topic, sensor_data)
                    
                    # Generate and publish device status (less frequently)
                    if int(time.time()) % 30 == 0:  # Every 30 seconds
                        status_data = self._generate_device_status()
                        self.mqtt_client.publish(self.status_topic, status_data)
                    
                    # Wait before next publication
                    time.sleep(5)  # Publish every 5 seconds
                else:
                    print("MQTT client disconnected, attempting to reconnect...")
                    time.sleep(5)
                    
        except KeyboardInterrupt:
            print("\nStopping publisher...")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the publisher"""
        self.running = False
        if self.mqtt_client:
            self.mqtt_client.disconnect()
        print("Publisher stopped")

def main():
    """Main function"""
    publisher = SensorDataPublisher()
    publisher.start()

if __name__ == "__main__":
    main()
