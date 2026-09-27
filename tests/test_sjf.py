import unittest
from algorithms.sjf import run_sjf

class TestSJF(unittest.TestCase):
    def test_sjf_non_preemptive(self):
        processes = [
            {"pid": "P1", "arrival_time": 0, "burst_time": 7, "priority": 1},
            {"pid": "P2", "arrival_time": 2, "burst_time": 4, "priority": 1},
            {"pid": "P3", "arrival_time": 4, "burst_time": 1, "priority": 1},
            {"pid": "P4", "arrival_time": 5, "burst_time": 4, "priority": 1},
        ]
        # At t=0, P1 starts (bt=7). P1 finishes at t=7.
        # At t=7, P2(bt=4), P3(bt=1), P4(bt=4) have arrived.
        # P3 (bt=1) selected, finishes at t=8.
        # At t=8, P2 (bt=4, AT=2) vs P4 (bt=4, AT=5) -> P2 selected (arrived earlier). Finishes t=12.
        # Then P4 finishes t=16.
        res = run_sjf(processes)
        self.assertEqual(res["execution_order"], ["P1", "P3", "P2", "P4"])
        p3 = next(p for p in res["processes"] if p["pid"] == "P3")
        self.assertEqual(p3["completion_time"], 8)
        self.assertEqual(p3["waiting_time"], 3)

    def test_single_process(self):
        processes = [{"pid": "P1", "arrival_time": 0, "burst_time": 5, "priority": 1}]
        res = run_sjf(processes)
        self.assertEqual(res["execution_order"], ["P1"])
        self.assertEqual(res["processes"][0]["completion_time"], 5)

if __name__ == "__main__":
    unittest.main()
