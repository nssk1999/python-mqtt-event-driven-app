#!/bin/bash

# MQTT Event-Driven Architecture Demo - System Startup Script
# This script starts all components of the system

echo "🚀 Starting MQTT Event-Driven Architecture Demo System"
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Check if Mosquitto is running
if ! brew services list | grep -q "mosquitto.*started"; then
    echo "⚠️  Mosquitto MQTT broker is not running. Starting it now..."
    brew services start mosquitto
    sleep 3
fi

echo "✅ Mosquitto MQTT broker is running"

# Function to start a component in a new terminal
start_component() {
    local component_name=$1
    local script_name=$2
    local description=$3
    
    echo "🔄 Starting $component_name..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS - use osascript to open new terminal
        osascript -e "
        tell application \"Terminal\"
            do script \"cd $(pwd) && source venv/bin/activate && echo '🚀 $description' && python $script_name\"
            set custom title of front window to \"$component_name\"
        end tell
        "
    else
        # Linux - use gnome-terminal or xterm
        if command -v gnome-terminal &> /dev/null; then
            gnome-terminal --title="$component_name" -- bash -c "cd $(pwd) && source venv/bin/activate && echo '🚀 $description' && python $script_name; exec bash"
        elif command -v xterm &> /dev/null; then
            xterm -title "$component_name" -e "cd $(pwd) && source venv/bin/activate && echo '🚀 $description' && python $script_name; exec bash" &
        else
            echo "⚠️  Could not open new terminal. Please run manually:"
            echo "   source venv/bin/activate"
            echo "   python $script_name"
        fi
    fi
    
    sleep 2
}

# Start all components
echo ""
echo "📱 Starting Web Application..."
start_component "Web Dashboard" "web_app.py" "Web Dashboard - Real-time MQTT data visualization"

echo ""
echo "📡 Starting MQTT Publisher..."
start_component "MQTT Publisher" "mqtt_publisher.py" "MQTT Publisher - Simulating IoT sensor data"

echo ""
echo "👂 Starting MQTT Subscriber..."
start_component "MQTT Subscriber" "mqtt_subscriber.py" "MQTT Subscriber - Processing incoming messages"

echo ""
echo "🎉 System startup complete!"
echo ""
echo "📋 Component Status:"
echo "   ✅ Mosquitto MQTT Broker"
echo "   ✅ Web Dashboard (http://localhost:5000)"
echo "   ✅ MQTT Publisher (simulating sensors)"
echo "   ✅ MQTT Subscriber (processing messages)"
echo ""
echo "🌐 Open your browser and navigate to: http://localhost:8080"
echo ""
echo "📱 The system is now running with:"
echo "   - Real-time sensor data streaming every 5 seconds"
echo "   - Device status updates every 30 seconds"
echo "   - Live web dashboard with WebSocket updates"
echo "   - Command control panel for device management"
echo ""
echo "🛑 To stop the system, close the terminal windows or press Ctrl+C in each"
echo ""
echo "🔧 For troubleshooting, check the README.md file"
