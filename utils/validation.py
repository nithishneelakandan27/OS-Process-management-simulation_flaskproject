"""
Input Validation Module for CPU Scheduling Simulator.
Ensures process data and parameters are valid before running simulations.
"""

def validate_simulation_input(data):
    """
    Validates the input payload for CPU scheduling simulation.
    
    Args:
        data (dict): Request body JSON dictionary containing 'algorithm', 'processes', and optional 'time_quantum'.
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not isinstance(data, dict):
        return False, "Invalid request body. Expected a JSON object."

    algorithm = data.get("algorithm")
    valid_algorithms = ["FCFS", "SJF", "PRIORITY", "RR"]
    if not algorithm or str(algorithm).upper() not in valid_algorithms:
        return False, f"Invalid algorithm. Must be one of: {', '.join(valid_algorithms)}"

    processes = data.get("processes")
    if not isinstance(processes, list) or len(processes) == 0:
        return False, "Process list cannot be empty."

    # Validate algorithm specific parameter
    if str(algorithm).upper() == "RR":
        time_quantum = data.get("time_quantum")
        if time_quantum is None:
            return False, "Time quantum is required for Round Robin algorithm."
        try:
            tq = int(time_quantum)
            if tq <= 0:
                return False, "Time quantum must be a positive integer greater than 0."
        except (ValueError, TypeError):
            return False, "Time quantum must be a valid integer."

    seen_pids = set()
    for idx, p in enumerate(processes):
        if not isinstance(p, dict):
            return False, f"Process at index {idx} must be a valid object."

        pid = p.get("pid")
        if pid is None or str(pid).strip() == "":
            return False, f"Process at index {idx} has an empty Process ID (PID)."
        
        pid_str = str(pid).strip()
        if pid_str in seen_pids:
            return False, f"Duplicate Process ID found: '{pid_str}'."
        seen_pids.add(pid_str)

        # Validate Arrival Time
        try:
            arrival_time = float(p.get("arrival_time")) if p.get("arrival_time") is not None else None
            if arrival_time is None or arrival_time < 0 or not arrival_time.is_integer():
                return False, f"Process '{pid_str}' has invalid Arrival Time. Must be an integer >= 0."
        except (ValueError, TypeError):
            return False, f"Process '{pid_str}' has non-numeric Arrival Time."

        # Validate Burst Time
        try:
            burst_time = float(p.get("burst_time")) if p.get("burst_time") is not None else None
            if burst_time is None or burst_time <= 0 or not burst_time.is_integer():
                return False, f"Process '{pid_str}' has invalid Burst Time. Must be an integer > 0."
        except (ValueError, TypeError):
            return False, f"Process '{pid_str}' has non-numeric Burst Time."

        # Validate Priority
        try:
            priority = float(p.get("priority")) if p.get("priority") is not None else None
            if priority is None or priority < 0 or not priority.is_integer():
                return False, f"Process '{pid_str}' has invalid Priority. Must be an integer >= 0."
        except (ValueError, TypeError):
            return False, f"Process '{pid_str}' has non-numeric Priority."

    return True, ""
