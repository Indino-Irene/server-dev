

 1. Overview

This project implements an IoT-based AC light dimmer system controlled through a backend server.
The hardware consists of an ESP32 microcontroller connected to an AC dimmer circuit (TRIAC + zero-cross detection). The server communicates with the ESP32 using HTTP requests to control brightness and monitor device status.

The server is responsible for managing devices, validating commands, maintaining system state, and ensuring reliable communication between users and hardware devices.

The backend is implemented using Python with the Flask web framework.



2. System Architecture

The system follows a simple client-server architecture.

User / Control Interface
↓
Python Server (API)
↓
ESP32 Device
↓
AC Dimmer Circuit (TRIAC

)
 Component Roles

Server

-Handles control requests
- Manages device information
- Stores system state
  -Sends brightness commands to devices

ESP32

-Connects to WiFi
  - Receives brightness commands
- Controls TRIAC timing
- Reports its state to the server

AC Dimmer Circuit

- Physically controls the AC power delivered to the lamp.

Note
The microcontroller handles the timing of the TRIAC switching. The server only sends brightness values (0–100).


Server Responsibilities

The server performs several critical roles in the system.

 Device Management

The server must maintain information about all connected devices.

Each device should have the following attributes:

- device_id (unique identifier)
- device_name
- ip_address
- current_brightness
- device_status (online/offline)
- last_seen_timestamp

This allows the server to track device availability and state.


Command Processing

When a brightness change request is received, the server:

1. Receives request from user or frontend
2. Validates the input
3. Finds the target device
4. Sends HTTP command to the ESP32
5. Waits for device response
6. Updates stored device state

Example command flow:

User Request
- Server validates brightness value
- Server sends command to ESP32
- ESP32 adjusts dimmer
- Server updates system state


 State Synchronization

State synchronization ensures the server and device maintain the same brightness value.

Problems that may occur:

- ESP32 reboot
  -Power failure
  -Network disconnection

To solve this, the ESP32 sends a synchronization message to the server whenever it boots.

Example:

Device Boot
- Device sends current brightness to server
-Server updates stored state

This prevents inconsistencies between server data and hardware state.



 Communication Interface (HTTP API)

The server exposes a REST-style API for interacting with devices.

Example endpoints:

POST /devices
Register a new device.

POST /devices/<device_id>/brightness
Set brightness of a device.

POST /devices/<device_id>/sync
Synchronize device state with the server.

GET /devices
List all devices.

GET /devices/<device_id>
Get status of a specific device.



 4. Input Validation

The server must validate all incoming data to prevent errors.

Example validation rules:

Brightness value:

- Must be an integer
- Must be between 0 and 100

Device ID:

- Must be unique
- Must exist in the system before issuing commands

Invalid inputs must return appropriate error responses.


 5. Error Handling

The server must handle communication failures and unexpected behavior.

Possible failure scenarios include:

ESP32 unreachable
Network timeout
Invalid device ID
Invalid brightness value

Recommended handling strategy:

-Use request timeouts
- Catch exceptions
- Return clear error messages
- Mark device as offline if unreachable



6. Device Communication Model

Communication between the server and ESP32 is based on HTTP requests.

Server → Device
Used for sending brightness commands.

Device → Server
Used for synchronization and status updates.

Example brightness command:

POST http://DEVICE_IP/set

Payload

{
"brightness": 70
}

Example synchronization request:

POST /devices/<device_id>/sync

Payload

{
"brightness": 70
}



 7. Data Storage

Initially, device information may be stored in memory for simplicity.

However, a database is recommended for long-term persistence.

Recommended database options:

SQLite – suitable for small local projects.
PostgreSQL – suitable for larger systems.

Stored data may include:

- Device information
- Current brightness level
- Device status
- System logs



 8. Security Considerations

Basic security should be implemented even in small IoT systems.

Recommended measures:

API input validation
Device authentication
HTTPS communication (for production deployment)

Future improvements may include:

- API keys
- Token authentication
- Firewall rules
- Reverse proxy


9. Reliability Considerations

A reliable system should tolerate network interruptions and device restarts.

Recommended practices:

- Devices should store last brightness value locally
- Devices should reconnect automatically to WiFi
-Devices should periodically synchronize with the server
-Server should detect offline devices

Optional feature:

Heartbeat messages every 30 seconds to confirm device availability.



 10. Scalability Considerations

Although the initial system may contain only one device, the server should support future expansion.

Scalability considerations include:

- Supporting multiple devices
-Grouping devices into rooms
- Supporting heduscling features
- Logging brightness history
- Supporting multiple users

Future upgrades may involve switching from HTTP polling to message brokers such as MQTT.


11. Development Stack

Backend Language
Python

Web Framework
Flask

Communication Protocol
HTTP REST API

Hardware Platform
ESP32 Microcontroller

Lighting Control
TRIAC-based AC dimmer circuit


12. Key Design Principles

The following principles guide the system design:

The server controls device behavior at a high level.
The ESP32 handles real-time electrical timing.
All inputs must be validated.
System state must remain synchronized between server and device.
The system must tolerate device or network failures.


