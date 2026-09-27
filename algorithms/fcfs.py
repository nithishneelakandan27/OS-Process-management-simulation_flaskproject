"""
First Come First Serve (FCFS) CPU Scheduling Algorithm.
Non-preemptive algorithm that executes processes in order of their arrival time.
"""
from utils.metrics import calculate_metrics

def run_fcfs(processes_input):
    """
    Simulates FCFS CPU Scheduling.

    Args:
        processes_input (list): List of process dictionaries with 'pid', 'arrival_time', 'burst_time', 'priority'.

    Returns:
        dict: Standardized simulation result containing gantt_chart, processes, metrics, execution_order, and logs.
    """
    # Make a copy of processes sorted by arrival_time, maintaining original order on tie
    processes = [dict(p) for p in processes_input]
    processes.sort(key=lambda p: (int(p["arrival_time"]), p["pid"]))

    gantt_chart = []
    logs = []
    execution_order = []
    completed_processes = []

    current_time = 0

    for process in processes:
        pid = process["pid"]
        at = int(process["arrival_time"])
        bt = int(process["burst_time"])
        priority = int(process.get("priority", 0))

        # Check if CPU needs to sit idle until process arrives
        if current_time < at:
            idle_duration = at - current_time
            gantt_chart.append({
                "pid": "IDLE",
                "start_time": current_time,
                "end_time": at,
                "is_idle": True
            })
            logs.append(f"Time {current_time}: CPU is Idle for {idle_duration} unit(s) until Time {at}")
            current_time = at

        # Process starts execution
        logs.append(f"Time {current_time}: Process {pid} arrived / entered Ready Queue")
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

    result = calculate_metrics(completed_processes, gantt_chart)
    result["gantt_chart"] = gantt_chart
    result["logs"] = logs
    result["execution_order"] = execution_order

    return result
