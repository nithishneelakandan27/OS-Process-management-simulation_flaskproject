"""
Round Robin (RR) CPU Scheduling Algorithm (Preemptive).
Executes processes in round-robin order with a fixed Time Quantum.
"""
from collections import deque
from utils.metrics import calculate_metrics

def run_round_robin(processes_input, time_quantum):
    """
    Simulates Round Robin Preemptive CPU Scheduling.

    Args:
        processes_input (list): List of process dictionaries.
        time_quantum (int): Maximum CPU slice allotted per process execution.

    Returns:
        dict: Standardized simulation result dictionary.
    """
    time_quantum = int(time_quantum)
    
    # Clone and sort incoming processes by arrival time
    unprocessed = sorted(
        [
            {
                "pid": p["pid"],
                "arrival_time": int(p["arrival_time"]),
                "burst_time": int(p["burst_time"]),
                "priority": int(p.get("priority", 0))
            }
            for p in processes_input
        ],
        key=lambda x: (x["arrival_time"], x["pid"])
    )

    remaining_burst = {p["pid"]: p["burst_time"] for p in unprocessed}
    first_start_times = {}
    completion_times = {}

    gantt_chart = []
    logs = []
    execution_order = []

    ready_queue = deque()
    enqueued = set()

    current_time = 0
    total_processes = len(unprocessed)
    completed_count = 0

    # Helper function to enqueue processes that have arrived by target_time
    def enqueue_new_arrivals(target_time):
        for p in unprocessed:
            pid = p["pid"]
            if p["arrival_time"] <= target_time and pid not in enqueued:
                ready_queue.append(p)
                enqueued.add(pid)
                logs.append(f"Time {p['arrival_time']}: Process {pid} entered Ready Queue")

    # Initial check at time 0
    enqueue_new_arrivals(current_time)

    while completed_count < total_processes:
        if not ready_queue:
            # CPU is idle until the next process arrives
            next_p = min(
                [p for p in unprocessed if p["pid"] not in enqueued],
                key=lambda x: (x["arrival_time"], x["pid"])
            )
            next_arrival = next_p["arrival_time"]
            gantt_chart.append({
                "pid": "IDLE",
                "start_time": current_time,
                "end_time": next_arrival,
                "is_idle": True
            })
            logs.append(f"Time {current_time}: CPU is Idle until Time {next_arrival}")
            current_time = next_arrival
            enqueue_new_arrivals(current_time)

        # Dequeue next process to run
        current_proc = ready_queue.popleft()
        pid = current_proc["pid"]

        # Record response time (first CPU allocation)
        if pid not in first_start_times:
            first_start_times[pid] = current_time

        exec_time = min(time_quantum, remaining_burst[pid])
        start_time = current_time
        end_time = start_time + exec_time
        current_time = end_time
        remaining_burst[pid] -= exec_time

        gantt_chart.append({
            "pid": pid,
            "start_time": start_time,
            "end_time": end_time,
            "is_idle": False
        })
        execution_order.append(pid)

        logs.append(f"Time {start_time}: Process {pid} started execution")

        # CRITICAL ROUND ROBIN STEP:
        # First, enqueue any new processes that arrived while this process was executing (arrival_time <= end_time)
        enqueue_new_arrivals(current_time)

        if remaining_burst[pid] > 0:
            logs.append(f"Time {end_time}: Time quantum ({time_quantum}) expired for Process {pid} (Remaining burst: {remaining_burst[pid]})")
            ready_queue.append(current_proc)
            logs.append(f"Time {end_time}: Process {pid} moved to Ready Queue")
        else:
            completed_count += 1
            completion_times[pid] = current_time
            logs.append(f"Time {end_time}: Process {pid} completed execution")

    # Build completed processes list for metrics calculation
    completed_processes = []
    for p in processes_input:
        pid = p["pid"]
        completed_processes.append({
            "pid": pid,
            "arrival_time": int(p["arrival_time"]),
            "burst_time": int(p["burst_time"]),
            "priority": int(p.get("priority", 0)),
            "completion_time": completion_times[pid],
            "first_start_time": first_start_times[pid]
        })

    result = calculate_metrics(completed_processes, gantt_chart)
    result["gantt_chart"] = gantt_chart
    result["logs"] = logs
    result["execution_order"] = execution_order

    return result
