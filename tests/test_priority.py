import unittest
from algorithms.priority import run_priority

class TestPriority(unittest.TestCase):
    def test_priority_non_preemptive(self):
        processes = [
            {"pid": "P1", "arrival_time": 0, "burst_time": 10, "priority": 3},
            {"pid": "P2", "arrival_time": 1, "burst_time": 1, "priority": 1},
            {"pid": "P3", "arrival_time": 2, "burst_time": 2, "priority": 2},
        ]
        # At t=0, P1 starts (priority 3, bt=10). Completes at t=10.
        # At t=10, P2(prio 1) and P3(prio 2) arrived. P2 selected (higher prio = lower num). Completes t=11.
        # P3 completes t=13.
        res = run_priority(processes)
        self.assertEqual(res["execution_order"], ["P1", "P2", "P3"])
        p2 = next(p for p in res["processes"] if p["pid"] == "P2")
        self.assertEqual(p2["completion_time"], 11)
        self.assertEqual(p2["waiting_time"], 9)

if __name__ == "__main__":
    unittest.main()
