"""
Flask Application for Operating System CPU Scheduling Simulator.
Provides web UI routes and REST API endpoint /api/simulate.
"""
from flask import Flask, render_template, request, jsonify
from utils.validation import validate_simulation_input
from algorithms import run_fcfs, run_sjf, run_priority, run_round_robin

app = Flask(__name__)

@app.route("/")
def index():
    """Renders the main simulator interface."""
    return render_template("index.html")

@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "message": "CPU Scheduling API is running."})

@app.route("/api/simulate", methods=["POST"])
def simulate():
    """
    API Endpoint: /api/simulate
    Accepts process inputs and scheduling configuration.
    Executes requested scheduling algorithm and returns calculated metrics and Gantt chart.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON request body."}), 400

    # Perform strict input validation
    is_valid, error_msg = validate_simulation_input(data)
    if not is_valid:
        return jsonify({"success": False, "error": error_msg}), 400

    algorithm = data.get("algorithm").upper()
    processes = data.get("processes")
    time_quantum = data.get("time_quantum")

    try:
        if algorithm == "FCFS":
            result = run_fcfs(processes)
        elif algorithm == "SJF":
            result = run_sjf(processes)
        elif algorithm == "PRIORITY":
            result = run_priority(processes)
        elif algorithm == "RR":
            result = run_round_robin(processes, time_quantum)
        else:
            return jsonify({"success": False, "error": "Unsupported algorithm."}), 400

        result["success"] = True
        result["algorithm"] = algorithm
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"success": False, "error": f"Internal simulation error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
