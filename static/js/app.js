/**
 * MQTT Event-Driven Architecture Demo - Frontend JavaScript
 * Handles WebSocket connections, real-time data updates, and user interactions
 */

class MQTTDashboard {
    constructor() {
        this.socket = null;
        this.isConnected = false;
        this.messageCount = 0;
        this.latestSensorData = null;
        this.latestDeviceStatus = null;
        
        this.initializeSocket();
        this.bindEvents();
        this.updateConnectionStatus();
        
        // Request initial data
        this.requestInitialData();
    }
    
    /**
     * Initialize Socket.IO connection
     */
    initializeSocket() {
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('Connected to WebSocket server');
            this.isConnected = true;
            this.updateConnectionStatus();
            this.showAlert('Connected to real-time data stream', 'success');
        });
        
        this.socket.on('disconnect', () => {
            console.log('Disconnected from WebSocket server');
            this.isConnected = false;
            this.updateConnectionStatus();
            this.showAlert('Disconnected from real-time data stream', 'error');
        });
        
        this.socket.on('sensor_data', (data) => {
            this.handleSensorData(data);
        });
        
        this.socket.on('device_status', (data) => {
            this.handleDeviceStatus(data);
        });
        
        this.socket.on('connect_error', (error) => {
            console.error('WebSocket connection error:', error);
            this.showAlert('WebSocket connection error', 'error');
        });
    }
    
    /**
     * Bind DOM events
     */
    bindEvents() {
        // Send command button
        document.getElementById('send-command').addEventListener('click', () => {
            this.sendCommand();
        });
        
        // Command select change
        document.getElementById('command-select').addEventListener('change', (e) => {
            this.handleCommandTypeChange(e.target.value);
        });
        
        // Enter key in command parameters
        document.getElementById('command-params').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                this.sendCommand();
            }
        });
    }
    
    /**
     * Request initial data from the server
     */
    async requestInitialData() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            if (data.latest_sensor_data) {
                this.handleSensorData(data.latest_sensor_data);
            }
            
            if (data.latest_device_status) {
                this.handleDeviceStatus(data.latest_device_status);
            }
            
            this.messageCount = data.message_count || 0;
            this.updateMessageCount();
            
        } catch (error) {
            console.error('Error fetching initial data:', error);
        }
    }
    
    /**
     * Handle incoming sensor data
     */
    handleSensorData(data) {
        this.latestSensorData = data;
        this.messageCount++;
        
        this.updateSensorDisplay(data);
        this.updateMessageCount();
        this.updateSensorStatus();
        this.addToMessageHistory('sensor_data', data);
        
        // Emit to WebSocket if connected
        if (this.socket && this.isConnected) {
            this.socket.emit('sensor_data_received', data);
        }
    }
    
    /**
     * Handle incoming device status
     */
    handleDeviceStatus(data) {
        this.latestDeviceStatus = data;
        this.messageCount++;
        
        this.updateDeviceDisplay(data);
        this.updateMessageCount();
        this.updateDeviceStatus();
        this.addToMessageHistory('device_status', data);
        
        // Emit to WebSocket if connected
        if (this.socket && this.isConnected) {
            this.socket.emit('device_status_received', data);
        }
    }
    
    /**
     * Update sensor data display
     */
    updateSensorDisplay(data) {
        const sensorContainer = document.getElementById('sensor-data');
        const sensors = data.sensors || {};
        
        let html = `
            <div class="mb-4 p-4 bg-blue-50 rounded-lg">
                <div class="flex items-center justify-between mb-3">
                    <h3 class="font-semibold text-gray-800">
                        <i class="fas fa-microchip text-blue-500 mr-2"></i>
                        Device: ${data.device_id || 'Unknown'}
                    </h3>
                    <span class="text-sm text-gray-500">
                        ${this.formatTimestamp(data.timestamp)}
                    </span>
                </div>
                <div class="grid grid-cols-2 gap-4">
        `;
        
        Object.entries(sensors).forEach(([sensorName, value]) => {
            const unit = this.getSensorUnit(sensorName);
            const icon = this.getSensorIcon(sensorName);
            const color = this.getSensorColor(sensorName, value);
            
            html += `
                <div class="sensor-card ${color}">
                    <div class="flex items-center justify-between">
                        <div>
                            <div class="text-sm opacity-80">${sensorName.charAt(0).toUpperCase() + sensorName.slice(1)}</div>
                            <div class="sensor-value">${value}</div>
                            <div class="sensor-unit">${unit}</div>
                        </div>
                        <i class="${icon} text-3xl opacity-80"></i>
                    </div>
                </div>
            `;
        });
        
        html += `
                </div>
                <div class="mt-3 text-sm text-gray-600">
                    <i class="fas fa-map-marker-alt mr-1"></i>
                    Location: ${data.location || 'Unknown'}
                </div>
            </div>
        `;
        
        sensorContainer.innerHTML = html;
    }
    
    /**
     * Update device status display
     */
    updateDeviceDisplay(data) {
        const deviceContainer = document.getElementById('device-info');
        
        const batteryLevel = data.battery || 0;
        const signalStrength = data.signal_strength || 0;
        const uptime = data.uptime || 0;
        
        let html = `
            <div class="space-y-4">
                <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div class="flex items-center">
                        <i class="fas fa-mobile-alt text-blue-500 mr-3"></i>
                        <div>
                            <p class="font-medium text-gray-800">Device ID</p>
                            <p class="text-sm text-gray-600">${data.device_id || 'Unknown'}</p>
                        </div>
                    </div>
                    <div class="text-right">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            <span class="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
                            ${data.status || 'Unknown'}
                        </span>
                    </div>
                </div>
                
                <div class="grid grid-cols-1 gap-4">
                    <div class="flex items-center justify-between p-3 bg-white border border-gray-200 rounded-lg">
                        <div class="flex items-center">
                            <i class="fas fa-battery-three-quarters text-green-500 mr-3"></i>
                            <span class="text-gray-700">Battery Level</span>
                        </div>
                        <div class="flex items-center">
                            <div class="w-20 bg-gray-200 rounded-full h-2 mr-2">
                                <div class="bg-green-500 h-2 rounded-full" style="width: ${batteryLevel}%"></div>
                            </div>
                            <span class="font-medium ${batteryLevel < 20 ? 'text-red-600' : 'text-gray-700'}">${batteryLevel}%</span>
                        </div>
                    </div>
                    
                    <div class="flex items-center justify-between p-3 bg-white border border-gray-200 rounded-lg">
                        <div class="flex items-center">
                            <i class="fas fa-signal text-blue-500 mr-3"></i>
                            <span class="text-gray-700">Signal Strength</span>
                        </div>
                        <span class="font-medium ${signalStrength < -50 ? 'text-red-600' : 'text-gray-700'}">${signalStrength} dBm</span>
                    </div>
                    
                    <div class="flex items-center justify-between p-3 bg-white border border-gray-200 rounded-lg">
                        <div class="flex items-center">
                            <i class="fas fa-clock text-purple-500 mr-3"></i>
                            <span class="text-gray-700">Uptime</span>
                        </div>
                        <span class="font-medium text-gray-700">${this.formatUptime(uptime)}</span>
                    </div>
                </div>
                
                <div class="text-sm text-gray-500 text-center">
                    Last updated: ${this.formatTimestamp(data.timestamp)}
                </div>
            </div>
        `;
        
        deviceContainer.innerHTML = html;
    }
    
    /**
     * Send command to MQTT broker
     */
    async sendCommand() {
        const commandSelect = document.getElementById('command-select');
        const targetDevice = document.getElementById('target-device').value;
        const commandParams = document.getElementById('command-params').value;
        
        const command = commandSelect.value;
        let parameters = {};
        
        try {
            if (commandParams.trim()) {
                parameters = JSON.parse(commandParams);
            }
        } catch (error) {
            this.showAlert('Invalid JSON in parameters field', 'error');
            return;
        }
        
        const commandData = {
            command: command,
            target_device: targetDevice,
            parameters: parameters
        };
        
        try {
            const response = await fetch('/api/send_command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(commandData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showAlert('Command sent successfully!', 'success');
                this.addToMessageHistory('command', commandData);
            } else {
                this.showAlert(`Error: ${result.error}`, 'error');
            }
            
        } catch (error) {
            console.error('Error sending command:', error);
            this.showAlert('Failed to send command', 'error');
        }
    }
    
    /**
     * Handle command type change
     */
    handleCommandTypeChange(commandType) {
        const paramsField = document.getElementById('command-params');
        
        switch (commandType) {
            case 'restart':
                paramsField.value = '{"force": true}';
                break;
            case 'calibrate':
                paramsField.value = '{"sensors": ["temperature", "humidity", "pressure", "light"]}';
                break;
            case 'update':
                paramsField.value = '{"version": "1.2.0", "auto_restart": true}';
                break;
            case 'custom':
                paramsField.value = '';
                paramsField.placeholder = '{"key": "value"}';
                break;
        }
    }
    
    /**
     * Add message to history
     */
    addToMessageHistory(type, data) {
        const historyTable = document.getElementById('message-history');
        
        // Remove "No messages yet" row if it exists
        const noMessagesRow = historyTable.querySelector('td[colspan="3"]');
        if (noMessagesRow) {
            noMessagesRow.parentElement.remove();
        }
        
        const row = document.createElement('tr');
        row.className = 'hover:bg-gray-50';
        
        const typeCell = document.createElement('td');
        typeCell.className = 'px-6 py-4 whitespace-nowrap';
        typeCell.innerHTML = `
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                type === 'sensor_data' ? 'bg-blue-100 text-blue-800' :
                type === 'device_status' ? 'bg-green-100 text-green-800' :
                'bg-purple-100 text-purple-800'
            }">
                ${type.replace('_', ' ').toUpperCase()}
            </span>
        `;
        
        const timestampCell = document.createElement('td');
        timestampCell.className = 'px-6 py-4 whitespace-nowrap text-sm text-gray-500';
        timestampCell.textContent = this.formatTimestamp(data.timestamp || Date.now() / 1000);
        
        const dataCell = document.createElement('td');
        dataCell.className = 'px-6 py-4 text-sm text-gray-900';
        dataCell.innerHTML = `<pre class="text-xs">${JSON.stringify(data, null, 2)}</pre>`;
        
        row.appendChild(typeCell);
        row.appendChild(timestampCell);
        row.appendChild(dataCell);
        
        historyTable.appendChild(row);
        
        // Keep only last 20 messages
        const rows = historyTable.querySelectorAll('tr');
        if (rows.length > 20) {
            rows[1].remove(); // Remove oldest message (skip header)
        }
    }
    
    /**
     * Update connection status display
     */
    updateConnectionStatus() {
        const statusIndicator = document.getElementById('status-indicator');
        const statusText = document.getElementById('status-text');
        
        if (this.isConnected) {
            statusIndicator.className = 'w-3 h-3 rounded-full bg-green-500';
            statusText.textContent = 'Connected';
        } else {
            statusIndicator.className = 'w-3 h-3 rounded-full bg-red-500';
            statusText.textContent = 'Disconnected';
        }
    }
    
    /**
     * Update message count display
     */
    updateMessageCount() {
        const messageCountElement = document.getElementById('message-count');
        if (messageCountElement) {
            messageCountElement.textContent = this.messageCount;
        }
    }
    
    /**
     * Update sensor status
     */
    updateSensorStatus() {
        const sensorStatusElement = document.getElementById('sensor-status');
        if (sensorStatusElement) {
            sensorStatusElement.textContent = this.latestSensorData ? 'Active' : 'Waiting...';
        }
    }
    
    /**
     * Update device status
     */
    updateDeviceStatus() {
        const deviceStatusElement = document.getElementById('device-status');
        if (deviceStatusElement) {
            deviceStatusElement.textContent = this.latestDeviceStatus ? 'Online' : 'Waiting...';
        }
    }
    
    /**
     * Show alert message
     */
    showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-${this.getAlertIcon(type)} mr-2"></i>
                ${message}
            </div>
        `;
        
        // Insert at the top of the main content
        const main = document.querySelector('main');
        main.insertBefore(alertDiv, main.firstChild);
        
        // Remove after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
    
    /**
     * Get alert icon based on type
     */
    getAlertIcon(type) {
        const icons = {
            'info': 'info-circle',
            'success': 'check-circle',
            'warning': 'exclamation-triangle',
            'error': 'times-circle'
        };
        return icons[type] || 'info-circle';
    }
    
    /**
     * Get sensor unit
     */
    getSensorUnit(sensorName) {
        const units = {
            'temperature': '°C',
            'humidity': '%',
            'pressure': 'hPa',
            'light': 'lux'
        };
        return units[sensorName] || '';
    }
    
    /**
     * Get sensor icon
     */
    getSensorIcon(sensorName) {
        const icons = {
            'temperature': 'fa-thermometer-half',
            'humidity': 'fa-tint',
            'pressure': 'fa-compress-alt',
            'light': 'fa-sun'
        };
        return `fas ${icons[sensorName] || 'fa-sensor'}`;
    }
    
    /**
     * Get sensor color based on value
     */
    getSensorColor(sensorName, value) {
        if (sensorName === 'temperature') {
            if (value > 30) return 'bg-red-500';
            if (value < 20) return 'bg-blue-500';
            return 'bg-green-500';
        }
        if (sensorName === 'humidity') {
            if (value > 75 || value < 35) return 'bg-yellow-500';
            return 'bg-blue-500';
        }
        return 'bg-purple-500';
    }
    
    /**
     * Format timestamp
     */
    formatTimestamp(timestamp) {
        if (!timestamp) return 'Unknown';
        const date = new Date(timestamp * 1000);
        return date.toLocaleString();
    }
    
    /**
     * Format uptime
     */
    formatUptime(seconds) {
        if (!seconds) return '0s';
        
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        
        if (hours > 0) {
            return `${hours}h ${minutes}m ${secs}s`;
        } else if (minutes > 0) {
            return `${minutes}m ${secs}s`;
        } else {
            return `${secs}s`;
        }
    }
}

// Initialize the dashboard when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new MQTTDashboard();
});
