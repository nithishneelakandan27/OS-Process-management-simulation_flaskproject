"""
Shortest Job First (SJF) CPU Scheduling Algorithm (Non-Preemptive).
Selects the process with the shortest burst time among available (arrived) processes.
"""
from utils.metrics import calculate_metrics

def run_sjf(processes_input):
    """
    Simulates SJF Non-Preemptive CPU Scheduling.

    Args:
        processes_input (list): List of process dictionaries.

    Returns:
        dict: Standardized simulation result dictionary.
    """
    # Create list of remaining processes
    unprocessed = [
        {
            "pid": p["pid"],
            "arrival_time": int(p["arrival_time"]),
            "burst_time": int(p["burst_time"]),
            "priority": int(p.get("priority", 0))
        }
        for p in processes_input
    ]

    gantt_chart = []
    logs = []
    execution_order = []
    completed_processes = []

    current_time = 0
    total_count = len(unprocessed)

    while len(completed_processes) < total_count:
        # Find all processes that have arrived on or before current_time
        arrived = [p for p in unprocessed if p["arrival_time"] <= current_time]

        if not arrived:
            # CPU is idle until the next process arrives
            next_arrival = min(p["arrival_time"] for p in unprocessed)
            gantt_chart.append({
                "pid": "IDLE",
                "start_time": current_time,
                "end_time": next_arrival,
                "is_idle": True
            })
            logs.append(f"Time {current_time}: CPU is Idle until Time {next_arrival}")
            current_time = next_arrival
            # Re-fetch arrived processes at updated current_time
            arrived = [p for p in unprocessed if p["arrival_time"] <= current_time]

        # Select process with shortest burst time. Tie breaker: arrival time, then PID
        selected = min(arrived, key=lambda p: (p["burst_time"], p["arrival_time"], str(p["pid"])))

        pid = selected["pid"]
        at = selected["arrival_time"]
        bt = selected["burst_time"]
        priority = selected["priority"]

        logs.append(f"Time {current_time}: Process {pid} selected (Shortest burst time: {bt})")
        logs.append(f"Time {current_time}: Process {pid} started execution")

        first_start_time = current_time
        start_time = current_time
        end_time = start_time + bt
        current_time = end_time

        gantt_chart.append({
            "pid": pid,
            "start_time": start_time,
            "end_time": end_time,
            "is_idle": False
        })
        execution_order.append(pid)
        logs.append(f"Time {current_time}: Process {pid} completed execution")

        completed_processes.append({
            "pid": pid,
            "arrival_time": at,
            "burst_time": bt,
            "priority": priority,
            "completion_time": current_time,
            "first_start_time": first_start_time
        })

        # Remove selected process from unprocessed list
        unprocessed.remove(selected)

    result = calculate_metrics(completed_processes, gantt_chart)
    result["gantt_chart"] = gantt_chart
    result["logs"] = logs
    result["execution_order"] = execution_order

    return result
