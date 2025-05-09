# 🚀 Space Mission Control Backend

This project simulates a backend system for a space mission control application. It models critical subsystems such as fuel management, power distribution, thermal control, communication, telemetry, navigation, command queues, anomaly detection, and many others — all designed to reflect real-world spacecraft mission scenarios.

---

## 🧠 Overview

This application is ideal for simulation, testing, and showcasing backend engineering skills in the context of critical aerospace software systems.

It is fully modular and scalable, using **FastAPI** and **SQLAlchemy** to simulate the backend of a realistic space mission control system.

---

## 🧩 Features

### ✅ Core Subsystems

* **Fuel System**: Tracks fuel levels, consumption rate, and temperature.
* **Power System**: Monitors battery level, solar panel status, generation, and consumption.
* **Thermal Control System**: Monitors internal and external temperatures, cooling system status.
* **Communication System**: Handles latency, signal strength, uplink/downlink status, last contact time.
* **Navigation System**: Simulates trajectory, course corrections, and status.
* **Anomaly Detection**: Logs alerts, anomalies, and priority levels.
* **Mission Events**: Tracks key events like engine burns, orbital insertion, and stage separation.

### 📡 Telemetry and Real-Time Monitoring

* **Telemetry Data**: Constantly updated stream of system readings.
* **Command Queue**: Allows scheduling, prioritizing, and execution of spacecraft commands.
* **Abort/Recovery System**: Monitors emergency aborts and recovery procedures.
* **Event Timeline**: Chronological listing of mission-critical events.
* **Sensor Array**: Simulates physical environmental readings and statuses.

### 💡 Mission Operations

* **Life Support System**: Tracks oxygen, CO₂, humidity, and crew vitals.
* **Software Update Log**: Simulates OTA software updates.
* **Ground Control Log**: Captures messages between ground and spacecraft.
* **Alert System**: Prioritized and categorized system alerts.
* **Docking System**: Docking operations and partner spacecraft status.
* **Payload System**: Monitors payloads, mass, power, and operational status.
* **Command Log**: Execution history of issued commands.

### 🔧 Resource Management

* **Resource Usage Log**: Tracks usage of oxygen, power, and other consumables.
* **Environment Monitor**: Monitors radiation, pressure, and magnetic fields.

---

## 🛠️ Technologies Used

* **FastAPI**: High-performance Python web framework
* **SQLAlchemy**: ORM for database modeling and management
* **PostgreSQL** (or any SQL DB): Database backend
* **Uvicorn**: ASGI server
* **Pydantic**: Data validation and parsing

---

## 📁 Project Structure

```
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── routes/
├── LICENSE.txt
├── README.md
├── requirements.txt
```

---

## 🧪 How to Run

1. Clone this repository
2. Create a virtual environment
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:

   ```bash
   uvicorn app.main:app --reload
   ```

---

## 🎯 Author Goals

This project was built by **Maria Izabel Vieira Passos**, a UX/UI Designer transitioning into front-end, backend and aerospace software engineering.

The goal is to demonstrate high-level backend architecture, critical system modeling, and readiness for working in aerospace-grade environments.

---

## 📩 Contact

* GitHub: [@MariaIzabelVieiraPassos](https://github.com/belvpassos)
* Email: ([mariaizabel09@outlook.com](mailto:mariaizabel09@outlook.com))

---

## License

© 2025 Maria Izabel Vieira Passos
All rights reserved.

This software and its source code are the intellectual property of the author.
No part of this project may be copied, modified, distributed, or used in any form without explicit written permission from the author.

Unauthorized use is strictly prohibited and may result in legal action.
