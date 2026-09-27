"""
CPU Scheduling Algorithms Package.
Includes FCFS, SJF (Non-Preemptive), Priority (Non-Preemptive), and Round Robin.
"""
from .fcfs import run_fcfs
from .sjf import run_sjf
from .priority import run_priority
from .round_robin import run_round_robin

__all__ = ["run_fcfs", "run_sjf", "run_priority", "run_round_robin"]
