import paho.mqtt.client as mqtt
import json
import time
import logging
from typing import Callable, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

class MQTTClient:
    """
    MQTT Client class for handling MQTT communications
    """
    
    def __init__(self, client_id: str = None):
        self.client_id = client_id or f"python_mqtt_client_{int(time.time())}"
        # Force MQTT v3.1.1 for better compatibility
        self.client = mqtt.Client(client_id=self.client_id, protocol=mqtt.MQTTv311)
        self.connected = False
        self.message_handlers: Dict[str, Callable] = {}
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Set up callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        self.client.on_publish = self._on_publish
        self.client.on_subscribe = self._on_subscribe
        
        # Get configuration from environment
        self.broker_host = os.getenv('MQTT_BROKER_HOST', 'localhost')
        self.broker_port = int(os.getenv('MQTT_BROKER_PORT', 1883))
        self.username = os.getenv('MQTT_BROKER_USERNAME')
        self.password = os.getenv('MQTT_BROKER_PASSWORD')
        
        # Set authentication if provided
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)
    
    def _on_connect(self, client, userdata, flags, rc):
        """Callback when connected to MQTT broker"""
        if rc == 0:
            self.connected = True
            self.logger.info(f"Connected to MQTT broker at {self.broker_host}:{self.broker_port}")
        else:
            error_messages = {
                1: "Connection refused - incorrect protocol version",
                2: "Connection refused - invalid client identifier",
                3: "Connection refused - server unavailable",
                4: "Connection refused - bad username or password",
                5: "Connection refused - not authorized"
            }
            error_msg = error_messages.get(rc, f"Unknown error code: {rc}")
            self.logger.error(f"Failed to connect to MQTT broker: {error_msg} (code: {rc})")
            self.connected = False
    
    def _on_disconnect(self, client, userdata, rc):
        """Callback when disconnected from MQTT broker"""
        self.connected = False
        if rc == 0:
            self.logger.info("Disconnected from MQTT broker (clean disconnect)")
        else:
            self.logger.warning(f"Disconnected from MQTT broker with code: {rc}")
            # Don't log every disconnect to reduce spam
    
    def _on_message(self, client, userdata, msg):
        """Callback when message is received"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            
            self.logger.info(f"Received message on topic '{topic}': {payload}")
            
            # Call registered handler if exists
            if topic in self.message_handlers:
                self.message_handlers[topic](topic, payload)
            else:
                # Default handler for unhandled topics
                self.logger.info(f"No handler registered for topic: {topic}")
                
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
    
    def _on_publish(self, client, userdata, mid):
        """Callback when message is published"""
        self.logger.info(f"Message published with ID: {mid}")
    
    def _on_subscribe(self, client, userdata, mid, granted_qos):
        """Callback when subscribed to topic"""
        self.logger.info(f"Subscribed to topic with ID: {mid}, QoS: {granted_qos}")
    
    def connect(self):
        """Connect to MQTT broker"""
        try:
            # Set clean session to False for persistent connections
            self.client._clean_session = False
            # Set keep alive to 60 seconds
            self.client.connect(self.broker_host, self.broker_port, keepalive=60)
            self.client.loop_start()
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MQTT broker"""
        try:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False
            self.logger.info("Disconnected from MQTT broker")
        except Exception as e:
            self.logger.error(f"Error disconnecting: {e}")
    
    def subscribe(self, topic: str, qos: int = 0):
        """Subscribe to a topic"""
        try:
            result = self.client.subscribe(topic, qos)
            self.logger.info(f"Subscribed to topic: {topic}")
            return result
        except Exception as e:
            self.logger.error(f"Failed to subscribe to {topic}: {e}")
            return None
    
    def publish(self, topic: str, message: Any, qos: int = 0, retain: bool = False):
        """Publish a message to a topic"""
        try:
            if isinstance(message, (dict, list)):
                message = json.dumps(message)
            elif not isinstance(message, str):
                message = str(message)
            
            result = self.client.publish(topic, message, qos, retain)
            self.logger.info(f"Published message to topic '{topic}': {message}")
            return result
        except Exception as e:
            self.logger.error(f"Failed to publish to {topic}: {e}")
            return None
    
    def register_handler(self, topic: str, handler: Callable):
        """Register a message handler for a specific topic"""
        self.message_handlers[topic] = handler
        self.logger.info(f"Registered handler for topic: {topic}")
    
    def is_connected(self) -> bool:
        """Check if client is connected"""
        return self.connected
    
    def get_client_info(self) -> Dict[str, Any]:
        """Get client information"""
        return {
            'client_id': self.client_id,
            'connected': self.connected,
            'broker_host': self.broker_host,
            'broker_port': self.broker_port,
            'subscribed_topics': list(self.message_handlers.keys())
        }
