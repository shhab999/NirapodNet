# NirapodNet

## Resilient Disaster Communication, Sensing & Emergency Response Infrastructure

NirapodNet is an **offline-first, resilient disaster communication and emergency coordination platform** designed for crisis environments where Internet connectivity, cellular networks, or centralized communication services are unavailable, degraded, or intermittent.

Its core principle is:

> **Loss of Internet connectivity must not imply loss of critical local communication.**

The project starts with a secure offline emergency communication core and incrementally adds emergency response, geospatial, sensing, resilient networking, portable infrastructure, UAV, and optional satellite-backhaul capabilities.

---

## Key Features

- Offline-first local communication
- Secure real-time messaging
- Emergency broadcast
- SOS and incident management
- Safety check-in
- Role-based access control
- GPS/location sharing where connectivity permits
- Offline-capable maps and GIS
- Shelter and rescue-team coordination
- Flood and environmental monitoring
- Edge/local-server operation
- Store-and-forward synchronization
- Mesh networking
- LoRa-based low-bandwidth telemetry where appropriate
- Portable solar-powered communication nodes
- UAV/drone communication relay and situational awareness
- Optional commercial satellite Internet backhaul
- Network, sensor, and node health monitoring
- Security auditing and threat modeling

---

## Why NirapodNet?

Disasters can simultaneously disrupt:

- Cellular towers
- Internet connectivity
- Terrestrial infrastructure
- Electrical power
- Emergency-team coordination
- Access to reliable local information

A conventional cloud-dependent application can therefore become unavailable when it is needed most.

NirapodNet separates **critical local communication from Internet availability**. Local services continue operating through edge infrastructure, Wi-Fi, mesh networking, and other available communication paths. When connectivity returns, queued information can synchronize with higher-level systems.

---

## Resilience Model

NirapodNet uses layered redundancy rather than depending on a single communication technology.

```text
Internet / Cellular Available
            |
            v
     Full Connectivity
            |
            v
Internet Unavailable
            |
            v
 Local / Mesh Communication
            |
            v
Partial Network Failure
            |
            +--> Surviving Nodes
            +--> LoRa
            +--> Portable Nodes
            +--> UAV Relay
            |
            v
Connectivity Restored
            |
            v
Authenticated Store-and-Forward Sync
            |
            v
Remote / Regional System

Optional:
Local Disaster Network
        |
      Gateway
        |
Satellite Terminal
        |
    Internet
        |
Remote Command Center
```

**Satellite connectivity is treated as optional backhaul, not as a core dependency.**

---

## High-Level Architecture

```text
                    Remote Command Center
                    Monitoring / Analytics
                              |
                    Internet / Satellite
                              |
                       Gateway Node
                              |
                    Resilient Backbone
                              |
        +-----------+---------+---------+-----------+
        |           |                   |           |
      Node 01     Node 02             Node 03     Node N
        |           |                   |           |
     Sensors     Shelter             Rescue       Users
        |           |                   |
        +-----------+---------+---------+
                              |
                       Local Edge Server
                         /                                 Wi-Fi          LoRa
                       |              |
                     Users         Sensors

                              +
                         UAV / Drone
                              |
                       Camera + Relay
                              |
                       Aerial Network
```

The architecture is modular so that communication technologies can be introduced or removed without redesigning the application layer.

---

## Core System Components

### 1. Local Emergency Communication

The initial implementation focuses on a functional local-area communication system providing:

- User authentication
- Real-time messaging
- Role-based access
- Emergency broadcast
- SOS
- Safety check-in

The first prototype is intended to demonstrate communication between multiple devices on the same local network without requiring Internet access.

### 2. Edge Computing

Each operational area can contain a local server/edge node maintaining:

- Local user sessions
- Messages
- SOS records
- Emergency alerts
- Cached maps
- Local incident information
- Sensor data
- Temporary event queues

This allows critical services to continue during Internet outages.

### 3. Store-and-Forward Synchronization

Disconnected nodes retain locally generated events until a valid communication path becomes available.

Synchronization requires:

- Unique event IDs
- Timestamps
- Source-node identifiers
- Authentication
- Integrity verification
- Conflict-handling rules
- Duplicate detection

### 4. Emergency Broadcast

Authorized operators can issue authenticated high-priority alerts such as:

- Evacuation warnings
- Flood warnings
- Fire alerts
- Security threats
- Medical emergencies
- Shelter instructions

The system must distinguish between raw sensor measurements, calculated indicators, automated alerts, and officially authorized warnings.

### 5. SOS and Incident Management

SOS events can contain:

- User identifier
- GPS coordinates where available
- Emergency type
- Timestamp
- Optional description
- Communication status

Each emergency event is represented as a structured incident with an identifier, priority, location, affected persons, assigned response team, destination, and lifecycle status.

Example lifecycle:

```text
OPEN
  -> RESPONDING
  -> ON-SCENE
  -> RESOLVED
```

### 6. Geospatial Information

The offline-capable GIS layer can contain:

- Shelters
- Hospitals
- Rescue teams
- Communication nodes
- Sensor nodes
- Flood zones
- Roads
- Bridges
- Safe zones
- Affected areas
- UAV locations
- Incident locations

Cached geographic data keeps essential maps useful when external map services are unreachable.

### 7. Flood and Environmental Monitoring

Physical sensor nodes can provide measurements including:

- Water level
- Water-level rise rate
- Rainfall
- Temperature
- Humidity
- Atmospheric conditions
- Sensor health
- Battery status

Sensor data can feed a warning pipeline:

```text
Sensor Data
    |
Validation
    |
Historical / Threshold Analysis
    |
Rate-of-Rise Assessment
    |
Risk Classification
    |
Operator / Authorized Alert
    |
Emergency Broadcast
```

Potential risk states:

- Normal
- Watch
- Warning
- Critical

### 8. Shelter and Rescue Coordination

Shelters can maintain structured information such as:

- Capacity
- Occupancy
- Food and water availability
- Medical capability
- Accessibility
- Location
- Communication status

Rescue teams can be represented by:

- Team ID
- Members
- Current location
- Availability
- Communication status
- Vehicle/boat
- Medical capability
- Equipment
- Assigned incidents

### 9. Mesh and Alternative Networking

Future networking layers will investigate:

- Wi-Fi mesh
- Dedicated mesh radios
- LoRa for suitable low-bandwidth telemetry
- Multi-hop forwarding
- Portable communication nodes
- UAV relay nodes

Technology selection will depend on range, bandwidth, latency, power consumption, spectrum constraints, and deployment environment.

### 10. UAV / Drone Layer

UAVs have two planned roles.

**Situational awareness**

- Flood assessment
- Infrastructure inspection
- Route assessment
- Locating stranded populations

**Communication relay**

A UAV may carry:

- Router
- Wi-Fi radio
- Mesh radio
- LoRa equipment where appropriate

This can temporarily restore connectivity between fragmented ground networks.

### 11. Portable Communication Nodes

Portable nodes may include:

```text
Solar Panel
    |
Charge Controller
    |
Battery
    |
Power Management
    |
Router / Mesh Radio
    |
LoRa Gateway
    |
Antenna
```

Potential deployment locations include shelters, schools, elevated buildings, emergency posts, community centers, and other flood-resilient locations.

---

## Security

Security is part of the system architecture from the beginning.

### Authentication

- Secure password hashing
- Authenticated sessions
- Role-based access control

### Data Security

- Encryption
- Integrity verification
- Secure transport where applicable

### Message Authenticity

Emergency broadcasts can use cryptographic authentication/signatures so clients can verify the origin of high-priority messages.

### Replay Protection

Events can include:

- Unique identifiers
- Timestamps
- Sequence information

### Auditability

Critical actions should generate immutable or tamper-evident logs where technically appropriate.

### Threat Model

The project considers:

- Malicious users
- Unauthorized operators
- Forged emergency messages
- Replay attacks
- Credential compromise
- Message interception
- Compromised nodes
- Sensor spoofing
- Network disruption
- Physical node theft
- Denial-of-service conditions

Each major security mechanism should be mapped to the threat it mitigates.

---

## Technology Stack

### Backend

- Python
- FastAPI / Flask
- WebSocket
- PostgreSQL
- SQLite for appropriate edge/local storage

### Frontend

- HTML
- CSS
- JavaScript

A modern frontend framework may be introduced later if system complexity justifies it.

### Data Processing

- Python
- pandas
- NumPy
- matplotlib

### Development

- Git
- GitHub
- Linux
- VS Code
- Automated testing / CI where appropriate

### Embedded / Hardware

Potential development platforms and components include:

- ESP32 / STM32-class microcontrollers
- Environmental sensors
- GPS modules
- LoRa radios
- Batteries
- Solar panels
- Charge controllers
- Weatherproof enclosures
- Routers
- Mesh-capable radios
- LoRa gateways
- Antennas
- Portable power systems

Exact hardware will be selected after requirements analysis and field testing.

---

## Development Roadmap

| Phase | Focus |
|---|---|
| 0 | Foundation: Python, networking, Git, Linux, web development |
| 1 | Core prototype: LAN messaging and local server |
| 2 | Emergency system: authentication, roles, SOS, broadcast, check-in |
| 3 | Security: encryption, authentication, signatures, replay protection, threat model |
| 4 | Measurement: latency, load, reliability, security testing |
| 5 | First real pilot: school/community deployment and emergency drill |
| 6 | Geospatial layer: GPS, maps, shelters, rescue teams |
| 7 | Sensor network: water-level and environmental monitoring |
| 8 | Resilient networking: mesh, LoRa, edge nodes, store-and-forward |
| 9 | Portable infrastructure: solar-powered nodes and field gateways |
| 10 | UAV integration: camera, GPS, communication relay |
| 11 | Satellite backhaul: optional commercial satellite connectivity |
| 12 | Multi-node deployment: large-area field testing |
| 13 | Research & validation: analysis, failure studies, publication, further deployment |

---

## Testing and Validation

The project is intended to be experimentally evaluated rather than demonstrated only through a working prototype.

### Communication

- End-to-end latency
- Throughput
- Packet loss
- Delivery reliability
- Broadcast propagation time

### Scalability

Testing targets include:

- 10 users
- 20 users
- 50 users
- Larger loads as infrastructure permits

### Security

- Unauthorized access attempts
- Replay attacks
- Forged broadcast attempts
- Compromised credentials
- Malformed messages

### Resilience

- Internet loss
- Node failure
- Gateway failure
- Intermittent connectivity
- Weak signal
- Power loss
- Partial network partition

### Hardware

- Battery endurance
- Solar charging
- Sensor accuracy
- Weather exposure
- Communication range

---

## Field Deployment Strategy

Deployment progresses from controlled environments toward operational environments:

1. **Laboratory** — Validate software and networking.
2. **Controlled local deployment** — Test multiple devices and nodes.
3. **School/community pilot** — Use real users and structured emergency drills.
4. **Multi-node field deployment** — Integrate sensors, GPS, mesh, and communication nodes.
5. **UAV integration** — Test aerial relay and observation.
6. **Satellite-backed deployment** — Add commercial satellite connectivity as external backhaul.
7. **Authorized real-world deployment** — Deploy only after safety, reliability, security, and operational validation.

---

## Research Questions

The project can investigate:

1. How reliably can an offline-first emergency network maintain communication during Internet disruption?
2. What architecture provides the best trade-off between range, bandwidth, latency, and power consumption?
3. How effectively can edge computing reduce dependency on remote infrastructure?
4. How quickly can distributed nodes propagate emergency alerts?
5. How does network performance degrade as nodes or users increase?
6. How can store-and-forward synchronization preserve event consistency during intermittent connectivity?
7. What are the security implications of an emergency network operating under partial infrastructure failure?
8. How effectively can water-level trends support localized flood awareness?
9. How can UAV-based communication relays restore connectivity in physically fragmented environments?

---

## Project Deliverables

### Engineering

- Functioning software platform
- Embedded sensor nodes
- Communication nodes
- Resilient network architecture
- UAV integration
- Satellite-backhaul integration where feasible

### Research

- Threat model
- Experimental methodology
- Datasets
- Performance analysis
- Field-test results
- Security analysis
- Research paper

### Documentation / Portfolio

- GitHub repository
- Technical documentation
- Architecture diagrams
- Hardware schematics
- Bill of materials
- API documentation
- Deployment procedures
- Experimental datasets
- Test methodology and results
- Failure reports
- Field-test documentation
- Demonstration/field-test videos
- Deployment report
- Presentation materials

---

## Operational Safety and Governance

NirapodNet is intended for disaster-response environments, so technical functionality alone is insufficient.

Deployment requires appropriate consideration of:

- Deployment authorization
- Operator training
- Data-privacy procedures
- Emergency communication protocols
- Hardware safety
- Electrical safety
- UAV regulatory compliance
- Radio-frequency compliance
- Secure credential management
- Backup procedures
- Incident logging

**NirapodNet is intended to complement, not replace, official emergency services and public warning systems.**

---

## Immediate Development Priority

The project is intentionally developed incrementally.

The immediate target is:

> **Build a secure, reliable offline emergency communication core first.**

Only after the core is operational and experimentally validated should the project integrate flood sensing, geospatial intelligence, mesh networking, portable nodes, UAVs, and satellite backhaul.

This staged approach keeps the system testable, measurable, and resilient while reducing unnecessary complexity during early development.

---

## License

NirapodNet is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for the complete license text.

Copyright (c) 2026 NirapodNet Contributors

