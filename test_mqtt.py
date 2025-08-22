#!/usr/bin/env python3
"""
MQTT Connection Test Script
Tests basic MQTT connectivity and functionality
"""

import time
import json
from mqtt_client import MQTTClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

def test_mqtt_connection():
    """Test basic MQTT connectivity"""
    print("🧪 Testing MQTT Connection...")
    print("=" * 40)
    
    # Create MQTT client
    client = MQTTClient("test_client")
    
    # Test connection
    print(f"Connecting to {client.broker_host}:{client.broker_port}...")
    
    if client.connect():
        print("✅ Successfully connected to MQTT broker")
        
        # Test publishing
        test_topic = "test/connection"
        test_message = {
            "test": True,
            "timestamp": int(time.time()),
            "message": "Hello MQTT!"
        }
        
        print(f"📤 Publishing test message to {test_topic}...")
        result = client.publish(test_topic, test_message)
        
        if result:
            print("✅ Test message published successfully")
        else:
            print("❌ Failed to publish test message")
        
        # Test subscribing
        print(f"📥 Subscribing to {test_topic}...")
        client.subscribe(test_topic)
        
        # Wait a bit for any messages
        print("⏳ Waiting for messages (5 seconds)...")
        time.sleep(5)
        
        # Disconnect
        client.disconnect()
        print("✅ Disconnected from MQTT broker")
        
    else:
        print("❌ Failed to connect to MQTT broker")
        print("Please check:")
        print("  1. Mosquitto is running: brew services list | grep mosquitto")
        print("  2. Port 1883 is not blocked")
        print("  3. Network connectivity")
        return False
    
    return True

def test_environment_config():
    """Test environment configuration"""
    print("\n🔧 Testing Environment Configuration...")
    print("=" * 40)
    
    required_vars = [
        'MQTT_BROKER_HOST',
        'MQTT_BROKER_PORT',
        'MQTT_TOPIC_SENSOR_DATA',
        'MQTT_TOPIC_DEVICE_STATUS',
        'MQTT_TOPIC_COMMANDS'
    ]
    
    all_good = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")
            all_good = False
    
    return all_good

def test_python_dependencies():
    """Test Python dependencies"""
    print("\n🐍 Testing Python Dependencies...")
    print("=" * 40)
    
    dependencies = [
        ('paho.mqtt.client', 'paho.mqtt.client'),
        ('flask', 'flask'),
        ('flask_socketio', 'flask_socketio'),
        ('dotenv', 'dotenv')
    ]
    
    all_good = True
    for dep_name, import_name in dependencies:
        try:
            __import__(import_name)
            print(f"✅ {dep_name}: Available")
        except ImportError:
            print(f"❌ {dep_name}: Not available")
            all_good = False
    
    return all_good

def main():
    """Main test function"""
    print("🚀 MQTT Event-Driven Architecture - System Test")
    print("=" * 50)
    
    # Test dependencies
    deps_ok = test_python_dependencies()
    
    # Test environment
    env_ok = test_environment_config()
    
    # Test MQTT connection
    mqtt_ok = test_mqtt_connection()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 40)
    print(f"Python Dependencies: {'✅ PASS' if deps_ok else '❌ FAIL'}")
    print(f"Environment Config:  {'✅ PASS' if env_ok else '❌ FAIL'}")
    print(f"MQTT Connection:     {'✅ PASS' if mqtt_ok else '❌ FAIL'}")
    
    if all([deps_ok, env_ok, mqtt_ok]):
        print("\n🎉 All tests passed! System is ready to run.")
        print("\nNext steps:")
        print("1. Run: python web_app.py")
        print("2. Run: python mqtt_publisher.py")
        print("3. Open: http://localhost:5000")
        print("\nOr use: ./start_system.sh")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before running the system.")
        print("\nCommon solutions:")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Start Mosquitto: brew services start mosquitto")
        print("- Check config.env file")

if __name__ == "__main__":
    main()
