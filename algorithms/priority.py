"""
Priority CPU Scheduling Algorithm (Non-Preemptive).
Executes arrived processes based on priority value (lower numerical value = higher priority).
"""
from utils.metrics import calculate_metrics

def run_priority(processes_input):
    """
    Simulates Non-Preemptive Priority CPU Scheduling.

    Convention: Lower numerical priority value indicates higher priority (e.g., 1 > 2).

    Args:
        processes_input (list): List of process dictionaries with 'pid', 'arrival_time', 'burst_time', 'priority'.

    Returns:
        dict: Standardized simulation result dictionary.
    """
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
        # Find arrived processes
        arrived = [p for p in unprocessed if p["arrival_time"] <= current_time]

        if not arrived:
            # Idle CPU
            next_arrival = min(p["arrival_time"] for p in unprocessed)
            gantt_chart.append({
                "pid": "IDLE",
                "start_time": current_time,
                "end_time": next_arrival,
                "is_idle": True
            })
            logs.append(f"Time {current_time}: CPU is Idle until Time {next_arrival}")
            current_time = next_arrival
            arrived = [p for p in unprocessed if p["arrival_time"] <= current_time]

        # Select process with highest priority (lowest priority number).
        # Tie-breaker: arrival_time, then PID
        selected = min(arrived, key=lambda p: (p["priority"], p["arrival_time"], str(p["pid"])))

        pid = selected["pid"]
        at = selected["arrival_time"]
        bt = selected["burst_time"]
        priority = selected["priority"]

        logs.append(f"Time {current_time}: Process {pid} selected (Priority: {priority})")
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

        unprocessed.remove(selected)

    result = calculate_metrics(completed_processes, gantt_chart)
    result["gantt_chart"] = gantt_chart
    result["logs"] = logs
    result["execution_order"] = execution_order

    return result
