"""
Metrics Calculation Module for CPU Scheduling Simulator.
Calculates per-process metrics (Turnaround Time, Waiting Time, Response Time)
and aggregate performance metrics (Averages, CPU Utilization, Throughput).
"""

def calculate_metrics(processes, gantt_chart):
    """
    Calculates detailed metrics for each process and aggregate metrics for the schedule.
    
    Args:
        processes (list): List of process dictionaries with 'pid', 'arrival_time', 'burst_time',
                          'completion_time', 'first_start_time'.
        gantt_chart (list): List of Gantt chart blocks [{'pid': ..., 'start_time': ..., 'end_time': ..., 'is_idle': bool}].
        
    Returns:
        dict: {
            "processes": list of processed dictionaries with TAT, WT, RT,
            "metrics": dict of aggregate metrics
        }
    """
    if not processes:
        return {
            "processes": [],
            "metrics": {
                "avg_waiting_time": 0.0,
                "avg_turnaround_time": 0.0,
                "avg_response_time": 0.0,
                "cpu_utilization": 0.0,
                "throughput": 0.0
            }
        }

    total_wt = 0
    total_tat = 0
    total_rt = 0
    num_processes = len(processes)

    processed_list = []
    min_arrival = min(p["arrival_time"] for p in processes)
    max_completion = max(p["completion_time"] for p in processes) if processes else 0

    for p in processes:
        pid = p["pid"]
        at = int(p["arrival_time"])
        bt = int(p["burst_time"])
        priority = int(p.get("priority", 0))
        ct = int(p["completion_time"])
        first_start = int(p["first_start_time"])

        tat = ct - at
        wt = tat - bt
        rt = first_start - at

        total_tat += tat
        total_wt += wt
        total_rt += rt

        processed_list.append({
            "pid": pid,
            "arrival_time": at,
            "burst_time": bt,
            "priority": priority,
            "completion_time": ct,
            "turnaround_time": tat,
            "waiting_time": wt,
            "response_time": rt
        })

    # Sort output processes by PID or Arrival Time for predictable presentation
    processed_list.sort(key=lambda x: (x["arrival_time"], x["pid"]))

    # Total CPU Busy Time = sum of burst times of non-idle Gantt entries
    total_busy_time = sum(b["end_time"] - b["start_time"] for b in gantt_chart if not b.get("is_idle", False))
    total_simulation_time = max_completion - min_arrival if max_completion > min_arrival else max_completion

    cpu_utilization = (total_busy_time / total_simulation_time * 100.0) if total_simulation_time > 0 else 0.0
    throughput = (num_processes / total_simulation_time) if total_simulation_time > 0 else 0.0

    avg_waiting_time = round(total_wt / num_processes, 2)
    avg_turnaround_time = round(total_tat / num_processes, 2)
    avg_response_time = round(total_rt / num_processes, 2)
    cpu_utilization = round(cpu_utilization, 2)
    throughput = round(throughput, 4)

    return {
        "processes": processed_list,
        "metrics": {
            "avg_waiting_time": avg_waiting_time,
            "avg_turnaround_time": avg_turnaround_time,
            "avg_response_time": avg_response_time,
            "cpu_utilization": cpu_utilization,
            "throughput": throughput
        }
    }
