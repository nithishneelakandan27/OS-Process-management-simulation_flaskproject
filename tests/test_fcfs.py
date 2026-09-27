import unittest
from algorithms.fcfs import run_fcfs

class TestFCFS(unittest.TestCase):
    def test_same_arrival_time(self):
        processes = [
            {"pid": "P1", "arrival_time": 0, "burst_time": 4, "priority": 1},
            {"pid": "P2", "arrival_time": 0, "burst_time": 3, "priority": 2},
        ]
        res = run_fcfs(processes)
        self.assertEqual(res["execution_order"], ["P1", "P2"])
        p1 = next(p for p in res["processes"] if p["pid"] == "P1")
        p2 = next(p for p in res["processes"] if p["pid"] == "P2")
        self.assertEqual(p1["completion_time"], 4)
        self.assertEqual(p1["turnaround_time"], 4)
        self.assertEqual(p1["waiting_time"], 0)
        self.assertEqual(p2["completion_time"], 7)
        self.assertEqual(p2["turnaround_time"], 7)
        self.assertEqual(p2["waiting_time"], 4)

    def test_idle_cpu(self):
        processes = [
            {"pid": "P1", "arrival_time": 2, "burst_time": 3, "priority": 1},
        ]
        res = run_fcfs(processes)
        self.assertTrue(res["gantt_chart"][0]["is_idle"])
        self.assertEqual(res["gantt_chart"][0]["end_time"], 2)
        p1 = res["processes"][0]
        self.assertEqual(p1["completion_time"], 5)
        self.assertEqual(p1["waiting_time"], 0)
        self.assertEqual(p1["response_time"], 0)

    def test_multiple_processes_different_arrival(self):
        processes = [
            {"pid": "P1", "arrival_time": 0, "burst_time": 5, "priority": 1},
            {"pid": "P2", "arrival_time": 1, "burst_time": 3, "priority": 1},
            {"pid": "P3", "arrival_time": 2, "burst_time": 1, "priority": 1},
        ]
        res = run_fcfs(processes)
        self.assertEqual(res["execution_order"], ["P1", "P2", "P3"])
        p3 = next(p for p in res["processes"] if p["pid"] == "P3")
        self.assertEqual(p3["completion_time"], 9)
        self.assertEqual(p3["turnaround_time"], 7)
        self.assertEqual(p3["waiting_time"], 6)

if __name__ == "__main__":
    unittest.main()
