import unittest
from algorithms.round_robin import run_round_robin

class TestRoundRobin(unittest.TestCase):
    def test_round_robin_preemption(self):
        processes = [
            {"pid": "P1", "arrival_time": 0, "burst_time": 5, "priority": 1},
            {"pid": "P2", "arrival_time": 1, "burst_time": 3, "priority": 1},
            {"pid": "P3", "arrival_time": 2, "burst_time": 1, "priority": 1},
        ]
        tq = 2
        # t=0: Queue=[P1]. P1 runs 0..2 (rem=3).
        # At t=2: P2 (AT=1) and P3 (AT=2) arrived. Queue=[P2, P3]. P1 re-added -> [P2, P3, P1].
        # P2 runs 2..4 (rem=1). Queue=[P3, P1]. P2 re-added -> [P3, P1, P2].
        # P3 runs 4..5 (rem=0, completed!). Queue=[P1, P2].
        # P1 runs 5..7 (rem=1). Queue=[P2]. P1 re-added -> [P2, P1].
        # P2 runs 7..8 (rem=0, completed!). Queue=[P1].
        # P1 runs 8..9 (rem=0, completed!). Queue=[].
        # Execution order: P1, P2, P3, P1, P2, P1
        res = run_round_robin(processes, tq)
        self.assertEqual(res["execution_order"], ["P1", "P2", "P3", "P1", "P2", "P1"])
        p1 = next(p for p in res["processes"] if p["pid"] == "P1")
        p2 = next(p for p in res["processes"] if p["pid"] == "P2")
        p3 = next(p for p in res["processes"] if p["pid"] == "P3")
        self.assertEqual(p1["completion_time"], 9)
        self.assertEqual(p2["completion_time"], 8)
        self.assertEqual(p3["completion_time"], 5)
        self.assertEqual(p1["response_time"], 0)
        self.assertEqual(p2["response_time"], 1) # First start 2 - AT 1 = 1
        self.assertEqual(p3["response_time"], 2) # First start 4 - AT 2 = 2

    def test_rr_with_idle(self):
        processes = [
            {"pid": "P1", "arrival_time": 2, "burst_time": 3, "priority": 1},
        ]
        res = run_round_robin(processes, 2)
        self.assertEqual(res["gantt_chart"][0]["is_idle"], True)
        self.assertEqual(res["processes"][0]["completion_time"], 5)

if __name__ == "__main__":
    unittest.main()
