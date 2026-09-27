# Interactive CPU Scheduling & Process Management Simulator

A lightweight, web-based Operating Systems CPU scheduling and process state simulator built with **Python + Flask** on the backend and modern **HTML5 + CSS3 + Vanilla JavaScript** on the frontend.

---

## 📌 Project Overview & Problem Statement

In Operating Systems, **CPU Scheduling** is the core process by which the OS kernel allocates CPU execution time among competing processes in the Ready Queue. Understanding how different scheduling algorithms manage execution order, context switches, ready queue management, and metrics like turnaround time, waiting time, and response time is essential for OS engineering and computer science technical interviews.

This simulator allows users to visually configure process arrival times, burst times, priorities, and algorithm-specific parameters (such as Time Quantum in Round Robin), simulate CPU execution in real-time, view Gantt charts, trace process state transitions (`New` ➔ `Ready Queue` ➔ `Running` ➔ `Terminated`), and analyze comprehensive performance metrics.

---

## 🎯 Objectives

1. **Educational & Interview Ready**: Simple, modular design without over-engineering or extra abstractions.
2. **Algorithm Implementation**: Pure Python implementations from scratch for FCFS, SJF (Non-Preemptive), Priority (Non-Preemptive), and Round Robin (Preemptive).
3. **Real-Time Visualization**: Dynamic Gantt chart rendering and animated step-by-step process state pipeline.
4. **Comprehensive Metrics**: Automatic calculation of Completion Time ($CT$), Turnaround Time ($TAT$), Waiting Time ($WT$), Response Time ($RT$), CPU Utilization ($U$), and Throughput ($TP$).
5. **Robust Validation**: Extensive server-side and client-side validation to catch invalid inputs, negative numbers, missing fields, duplicate PIDs, or invalid time quanta.

---

## 🛠 Technology Stack

- **Backend**: Python 3.x, Flask (Lightweight REST API framework)
- **Frontend**: HTML5, CSS3 (Flexbox/Grid, Dark OS Theme), Vanilla JavaScript (ES6+, Fetch API)
- **Testing**: Python `unittest` framework
- **Dependencies**: Minimal (`Flask`, `pytest`)

---

## 🏗 Architecture & Project Structure

```text
os-cpu-scheduler/
│
├── app.py                      # Flask REST API endpoints and web server entry point
│
├── algorithms/                 # CPU Scheduling algorithm implementations
│   ├── __init__.py             # Exposes algorithm module functions
│   ├── fcfs.py                 # First Come First Serve scheduling logic
│   ├── sjf.py                  # Shortest Job First (Non-Preemptive) logic
│   ├── priority.py             # Priority Scheduling (Non-Preemptive) logic
│   └── round_robin.py          # Round Robin (Preemptive) logic with Ready Queue
│
├── utils/                      # Helper & utility modules
│   ├── __init__.py
│   ├── metrics.py              # Per-process & aggregate performance metrics calculator
│   └── validation.py           # Strict payload and process input validator
│
├── templates/
│   └── index.html              # Single page simulator interface template
│
├── static/
│   ├── css/
│   │   └── style.css           # OS-themed dark styles & Gantt chart styling
│   └── js/
│       └── app.js              # DOM handler, API client, Gantt renderer & animation playback
│
├── tests/                      # Automated unit test suite
│   ├── test_fcfs.py
│   ├── test_sjf.py
│   ├── test_priority.py
│   └── test_round_robin.py
│
├── requirements.txt            # Dependency specification file
├── README.md                   # Project documentation
└── PROJECT_INTERVIEW_GUIDE.md  # Comprehensive technical interview preparation guide
```

---

## ⚙️ Scheduling Formulas

1. **Completion Time ($CT$)**: Timestamp at which a process finishes execution.
2. **Turnaround Time ($TAT$)**:
   $$\text{Turnaround Time} = CT - AT$$
3. **Waiting Time ($WT$)**:
   $$\text{Waiting Time} = TAT - BT$$
4. **Response Time ($RT$)**:
   $$\text{Response Time} = \text{Time of First CPU Allocation} - AT$$
5. **CPU Utilization ($U$)**:
   $$\text{CPU Utilization (\%)} = \left( \frac{\text{Total Busy CPU Time}}{\text{Total Simulation Duration}} \right) \times 100$$
6. **Throughput ($TP$)**:
   $$\text{Throughput} = \frac{\text{Total Completed Processes}}{\text{Total Simulation Duration}}$$

---

## 🔄 Request-Response API Flow

1. **User interaction**: User configures processes and selects an algorithm, then clicks "Run Simulation".
2. **Client Validation & HTTP POST**: `app.js` validates inputs and sends a POST request to `/api/simulate`.
3. **Flask Route**: `app.py` catches the POST request and passes data to `validate_simulation_input()`.
4. **Algorithm Dispatch**: `app.py` calls the targeted scheduling function (e.g. `run_round_robin(processes, time_quantum)`).
5. **Metrics Computation**: The algorithm computes Gantt chart blocks and calls `calculate_metrics()` in `utils/metrics.py`.
6. **JSON Response**: Flask returns structured JSON data containing Gantt chart intervals, detailed process metrics, aggregate metrics, and timestamped event logs.
7. **Frontend Rendering**: `app.js` dynamically populates the Gantt chart, metrics cards, process table, and terminal log, and initializes step-by-step playback controls.

---

## 🚀 How to Run the Project

### 1. Prerequisites
Ensure Python 3.8+ is installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Flask Server
```bash
python app.py
```
The server will start at `http://127.0.0.1:5000/`. Open this URL in any web browser.

### 4. Run Unit Tests
```bash
python -m unittest discover -s tests
```

---

## 📝 Example API Request & Response

### Request (`POST /api/simulate`)
```json
{
  "algorithm": "RR",
  "processes": [
    { "pid": "P1", "arrival_time": 0, "burst_time": 5, "priority": 1 },
    { "pid": "P2", "arrival_time": 1, "burst_time": 3, "priority": 1 }
  ],
  "time_quantum": 2
}
```

### Response (`200 OK`)
```json
{
  "success": true,
  "algorithm": "RR",
  "execution_order": ["P1", "P2", "P1", "P2", "P1"],
  "gantt_chart": [
    { "pid": "P1", "start_time": 0, "end_time": 2, "is_idle": false },
    { "pid": "P2", "start_time": 2, "end_time": 4, "is_idle": false },
    { "pid": "P1", "start_time": 4, "end_time": 6, "is_idle": false },
    { "pid": "P2", "start_time": 6, "end_time": 7, "is_idle": false },
    { "pid": "P1", "start_time": 7, "end_time": 8, "is_idle": false }
  ],
  "metrics": {
    "avg_waiting_time": 3.0,
    "avg_turnaround_time": 7.0,
    "avg_response_time": 0.5,
    "cpu_utilization": 100.0,
    "throughput": 0.25
  },
  "processes": [
    { "pid": "P1", "arrival_time": 0, "burst_time": 5, "priority": 1, "completion_time": 8, "turnaround_time": 8, "waiting_time": 3, "response_time": 0 },
    { "pid": "P2", "arrival_time": 1, "burst_time": 3, "priority": 1, "completion_time": 7, "turnaround_time": 6, "waiting_time": 3, "response_time": 1 }
  ],
  "logs": [
    "Time 0: Process P1 entered Ready Queue",
    "Time 0: Process P1 started execution",
    "Time 1: Process P2 entered Ready Queue",
    "Time 2: Time quantum (2) expired for Process P1 (Remaining burst: 3)",
    "Time 2: Process P1 moved to Ready Queue",
    "Time 2: Process P2 started execution",
    "..."
  ]
}
```
