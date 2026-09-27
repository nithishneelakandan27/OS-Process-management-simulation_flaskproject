/**
 * Frontend JavaScript for Operating System CPU Scheduling Simulator.
 * Manages UI interactions, form validation, API calls to Flask,
 * rendering Gantt charts, metrics, logs, and process state animation.
 */

document.addEventListener("DOMContentLoaded", () => {
    // UI Elements
    const algorithmSelect = document.getElementById("algorithm-select");
    const tqContainer = document.getElementById("tq-container");
    const timeQuantumInput = document.getElementById("time-quantum");
    const processRows = document.getElementById("process-rows");
    const btnAddProcess = document.getElementById("btn-add-process");
    const btnSimulate = document.getElementById("btn-simulate");
    const btnClear = document.getElementById("btn-clear");
    const btnPreset1 = document.getElementById("btn-preset-1");
    const btnPreset2 = document.getElementById("btn-preset-2");
    const errorBox = document.getElementById("error-box");

    // Visualization & Metrics Elements
    const ganttContainer = document.getElementById("gantt-container");
    const resultsRows = document.getElementById("results-rows");
    const terminalLog = document.getElementById("terminal-log");
    const valAvgWt = document.getElementById("val-avg-wt");
    const valAvgTat = document.getElementById("val-avg-tat");
    const valAvgRt = document.getElementById("val-avg-rt");
    const valCpuUtil = document.getElementById("val-cpu-util");
    const valThroughput = document.getElementById("val-throughput");

    // Animation Controls
    const btnPlay = document.getElementById("btn-play");
    const btnPause = document.getElementById("btn-pause");
    const btnResetAnim = document.getElementById("btn-reset-anim");
    const speedSlider = document.getElementById("speed-slider");
    const boxNew = document.getElementById("box-new");
    const boxReady = document.getElementById("box-ready");
    const boxRunning = document.getElementById("box-running");
    const boxTerminated = document.getElementById("box-terminated");
    const preemptArrow = document.getElementById("preempt-arrow");

    // State Variables
    let currentSimulationData = null;
    let animInterval = null;
    let currentAnimStep = 0;
    let isPlaying = false;

    // Process Color Palette Map
    const processColors = {};
    const colorPalette = [
        "#38bdf8", "#34d399", "#f43f5e", "#fbbf24", "#a855f7",
        "#ec4899", "#14b8a6", "#f97316", "#8b5cf6", "#06b6d4"
    ];

    function getProcessColor(pid) {
        if (pid === "IDLE") return "#475569";
        if (!processColors[pid]) {
            const index = Object.keys(processColors).length % colorPalette.length;
            processColors[pid] = colorPalette[index];
        }
        return processColors[pid];
    }

    // Toggle Time Quantum container based on selected algorithm
    algorithmSelect.addEventListener("change", () => {
        if (algorithmSelect.value === "RR") {
            tqContainer.classList.remove("hidden");
        } else {
            tqContainer.classList.add("hidden");
        }
    });

    // Add Process Row to Input Table
    function addProcessRow(pid = "", arrivalTime = 0, burstTime = 1, priority = 1) {
        const rowCount = processRows.children.length + 1;
        const defaultPid = pid || `P${rowCount}`;

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><input type="text" class="table-input pid-input" value="${defaultPid}" placeholder="e.g. P1"></td>
            <td><input type="number" class="table-input at-input" value="${arrivalTime}" min="0" step="1"></td>
            <td><input type="number" class="table-input bt-input" value="${burstTime}" min="1" step="1"></td>
            <td><input type="number" class="table-input prio-input" value="${priority}" min="0" step="1"></td>
            <td><button class="btn btn-danger-outline btn-remove">Delete</button></td>
        `;

        tr.querySelector(".btn-remove").addEventListener("click", () => {
            tr.remove();
        });

        processRows.appendChild(tr);
    }

    // Clear All Process Rows
    function clearProcessRows() {
        processRows.innerHTML = "";
        hideError();
    }

    // Preset 1: Standard Multi-process Scenario
    function loadPreset1() {
        clearProcessRows();
        algorithmSelect.value = "FCFS";
        tqContainer.classList.add("hidden");
        addProcessRow("P1", 0, 4, 2);
        addProcessRow("P2", 1, 3, 1);
        addProcessRow("P3", 2, 1, 3);
        addProcessRow("P4", 5, 2, 2);
        logTerminal("[SYSTEM] Loaded Preset 1: Standard multi-process scenario.");
    }

    // Preset 2: Round Robin Preemption Scenario
    function loadPreset2() {
        clearProcessRows();
        algorithmSelect.value = "RR";
        tqContainer.classList.remove("hidden");
        timeQuantumInput.value = 2;
        addProcessRow("P1", 0, 5, 1);
        addProcessRow("P2", 1, 4, 1);
        addProcessRow("P3", 2, 2, 1);
        addProcessRow("P4", 4, 1, 1);
        logTerminal("[SYSTEM] Loaded Preset 2: Round Robin preemption scenario.");
    }

    // Initial default rows
    loadPreset1();

    // Event Listeners for Row Management
    btnAddProcess.addEventListener("click", () => addProcessRow());
    btnClear.addEventListener("click", () => {
        clearProcessRows();
        resetVisualization();
        logTerminal("[SYSTEM] Cleared all process inputs.");
    });
    btnPreset1.addEventListener("click", loadPreset1);
    btnPreset2.addEventListener("click", loadPreset2);

    // Read Input Form & Perform Frontend Validation
    function getFormProcesses() {
        const rows = processRows.querySelectorAll("tr");
        const processes = [];
        const seenPids = new Set();

        if (rows.length === 0) {
            showError("Please add at least one process to simulate.");
            return null;
        }

        for (let i = 0; i < rows.length; i++) {
            const row = rows[i];
            const pid = row.querySelector(".pid-input").value.trim();
            const atStr = row.querySelector(".at-input").value;
            const btStr = row.querySelector(".bt-input").value;
            const prioStr = row.querySelector(".prio-input").value;

            if (!pid) {
                showError(`Row ${i + 1} has an empty Process ID.`);
                return null;
            }
            if (seenPids.has(pid)) {
                showError(`Duplicate Process ID '${pid}' found. Each process must have a unique ID.`);
                return null;
            }
            seenPids.add(pid);

            const at = parseInt(atStr, 10);
            const bt = parseInt(btStr, 10);
            const prio = parseInt(prioStr, 10);

            if (isNaN(at) || at < 0) {
                showError(`Process '${pid}' has invalid Arrival Time. Must be an integer ≥ 0.`);
                return null;
            }
            if (isNaN(bt) || bt <= 0) {
                showError(`Process '${pid}' has invalid Burst Time. Must be an integer > 0.`);
                return null;
            }
            if (isNaN(prio) || prio < 0) {
                showError(`Process '${pid}' has invalid Priority. Must be an integer ≥ 0.`);
                return null;
            }

            processes.push({
                pid: pid,
                arrival_time: at,
                burst_time: bt,
                priority: prio
            });
        }

        const algorithm = algorithmSelect.value;
        let timeQuantum = null;

        if (algorithm === "RR") {
            const tq = parseInt(timeQuantumInput.value, 10);
            if (isNaN(tq) || tq <= 0) {
                showError("Time quantum must be a positive integer greater than 0.");
                return null;
            }
            timeQuantum = tq;
        }

        hideError();
        return {
            algorithm: algorithm,
            processes: processes,
            time_quantum: timeQuantum
        };
    }

    function showError(msg) {
        errorBox.textContent = msg;
        errorBox.classList.remove("hidden");
    }

    function hideError() {
        errorBox.textContent = "";
        errorBox.classList.add("hidden");
    }

    function logTerminal(msg, type = "system") {
        const div = document.createElement("div");
        div.className = `log-line ${type}`;
        div.textContent = msg;
        terminalLog.appendChild(div);
        terminalLog.scrollTop = terminalLog.scrollHeight;
    }

    // Run Simulation Button Click Handler
    btnSimulate.addEventListener("click", async () => {
        const payload = getFormProcesses();
        if (!payload) return;

        resetVisualization();
        logTerminal(`[API] Sending simulation request for ${payload.algorithm}...`);

        try {
            const response = await fetch("/api/simulate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                showError(data.error || "Simulation failed.");
                logTerminal(`[ERROR] ${data.error || 'Simulation failed.'}`, "preempt");
                return;
            }

            currentSimulationData = data;
            renderGanttChart(data.gantt_chart);
            renderMetrics(data.metrics);
            renderResultsTable(data.processes);
            renderLogs(data.logs);

            // Enable Animation Controls
            btnPlay.disabled = false;
            btnResetAnim.disabled = false;

            logTerminal(`[SYSTEM] Simulation completed successfully for ${data.algorithm}.`, "exec");

        } catch (err) {
            showError("Failed to connect to backend server. Make sure Flask app is running.");
            logTerminal(`[ERROR] Connection error: ${err.message}`, "preempt");
        }
    });

    // Render Gantt Chart
    function renderGanttChart(ganttBlocks) {
        ganttContainer.innerHTML = "";
        if (!ganttBlocks || ganttBlocks.length === 0) {
            ganttContainer.innerHTML = '<div class="placeholder-text">No Gantt chart data.</div>';
            return;
        }

        const timeline = document.createElement("div");
        timeline.className = "gantt-timeline";

        const totalDuration = ganttBlocks[ganttBlocks.length - 1].end_time;

        ganttBlocks.forEach((block, idx) => {
            const duration = block.end_time - block.start_time;
            const flexWidth = (duration / totalDuration) * 100;

            const blockDiv = document.createElement("div");
            blockDiv.className = `gantt-block`;
            blockDiv.style.flex = `${flexWidth} 0 ${Math.max(flexWidth, 5)}%`;
            blockDiv.dataset.index = idx;

            const color = getProcessColor(block.pid);

            const barDiv = document.createElement("div");
            barDiv.className = `gantt-bar ${block.is_idle ? 'idle' : ''}`;
            barDiv.style.backgroundColor = color;
            barDiv.textContent = block.is_idle ? "IDLE" : block.pid;
            barDiv.title = `${block.pid}: ${block.start_time} ➔ ${block.end_time} (${duration} units)`;

            const ticksDiv = document.createElement("div");
            ticksDiv.className = "gantt-ticks";
            ticksDiv.innerHTML = `<span>${block.start_time}</span><span>${block.end_time}</span>`;

            blockDiv.appendChild(barDiv);
            blockDiv.appendChild(ticksDiv);
            timeline.appendChild(blockDiv);
        });

        ganttContainer.appendChild(timeline);
    }

    // Render Performance Metrics
    function renderMetrics(metrics) {
        valAvgWt.textContent = metrics.avg_waiting_time;
        valAvgTat.textContent = metrics.avg_turnaround_time;
        valAvgRt.textContent = metrics.avg_response_time;
        valCpuUtil.textContent = metrics.cpu_utilization;
        valThroughput.textContent = metrics.throughput;
    }

    // Render Process Results Table
    function renderResultsTable(processes) {
        resultsRows.innerHTML = "";
        processes.forEach(p => {
            const tr = document.createElement("tr");
            const color = getProcessColor(p.pid);
            tr.innerHTML = `
                <td><span class="process-badge" style="background-color:${color}">${p.pid}</span></td>
                <td>${p.arrival_time}</td>
                <td>${p.burst_time}</td>
                <td>${p.priority}</td>
                <td>${p.completion_time}</td>
                <td>${p.turnaround_time}</td>
                <td>${p.waiting_time}</td>
                <td>${p.response_time}</td>
            `;
            resultsRows.appendChild(tr);
        });
    }

    // Render Event Logs
    function renderLogs(logs) {
        terminalLog.innerHTML = "";
        logs.forEach(log => {
            let type = "system";
            if (log.includes("started execution") || log.includes("completed execution")) {
                type = "exec";
            } else if (log.includes("Time quantum expired") || log.includes("moved to Ready Queue")) {
                type = "preempt";
            } else if (log.includes("Idle")) {
                type = "idle";
            }
            logTerminal(log, type);
        });
    }

    // Reset Visualization State
    function resetVisualization() {
        pauseAnimation();
        currentAnimStep = 0;
        btnPlay.disabled = true;
        btnPause.disabled = true;
        btnResetAnim.disabled = true;
        ganttContainer.innerHTML = '<div class="placeholder-text">Run a simulation to generate the Gantt chart timeline.</div>';
        resultsRows.innerHTML = '<tr><td colspan="8" class="text-center text-muted">No simulation data available</td></tr>';
        valAvgWt.textContent = "-";
        valAvgTat.textContent = "-";
        valAvgRt.textContent = "-";
        valCpuUtil.textContent = "-";
        valThroughput.textContent = "-";
        clearStateBoxes();
    }

    function clearStateBoxes() {
        boxNew.innerHTML = "";
        boxReady.innerHTML = "";
        boxRunning.innerHTML = "";
        boxTerminated.innerHTML = "";
        preemptArrow.classList.add("hidden");

        const activeBlocks = ganttContainer.querySelectorAll(".active-gantt");
        activeBlocks.forEach(b => b.classList.remove("active-gantt"));
    }

    // Create Process Badge Element
    function createBadge(pid) {
        const badge = document.createElement("span");
        badge.className = "process-badge";
        badge.style.backgroundColor = getProcessColor(pid);
        badge.textContent = pid;
        return badge;
    }

    // Step Animation Logic for State Pipeline & Gantt Chart
    function updateAnimationStep(stepIndex) {
        if (!currentSimulationData || !currentSimulationData.gantt_chart) return;
        const gantt = currentSimulationData.gantt_chart;
        if (stepIndex >= gantt.length) {
            pauseAnimation();
            logTerminal("[ANIMATION] Playback completed.", "system");
            return;
        }

        clearStateBoxes();

        // Highlight active Gantt Block
        const blockDivs = ganttContainer.querySelectorAll(".gantt-block");
        if (blockDivs[stepIndex]) {
            blockDivs[stepIndex].classList.add("active-gantt");
            blockDivs[stepIndex].scrollIntoView({ behavior: 'smooth', inline: 'center' });
        }

        const currentBlock = gantt[stepIndex];
        const currentTime = currentBlock.end_time;
        const runningPid = currentBlock.is_idle ? null : currentBlock.pid;

        // Categorize processes into states at currentTime
        const inputProcs = currentSimulationData.processes;

        inputProcs.forEach(p => {
            const pid = p.pid;
            const at = p.arrival_time;
            const ct = p.completion_time;

            if (at > currentTime) {
                // Process hasn't arrived yet
                boxNew.appendChild(createBadge(pid));
            } else if (ct <= currentTime && (runningPid !== pid || currentBlock.end_time === ct)) {
                // Process has terminated
                boxTerminated.appendChild(createBadge(pid));
            } else if (runningPid === pid) {
                // Process currently running in CPU
                boxRunning.appendChild(createBadge(pid));
            } else {
                // Arrived and not terminated -> Ready Queue
                boxReady.appendChild(createBadge(pid));
            }
        });

        // Show preemption indicator if this block represents a preemption
        if (currentSimulationData.algorithm === "RR" && !currentBlock.is_idle) {
            const isCompleted = inputProcs.find(p => p.pid === currentBlock.pid).completion_time === currentBlock.end_time;
            if (!isCompleted) {
                preemptArrow.classList.remove("hidden");
                preemptArrow.textContent = `↺ Preemption: Process ${currentBlock.pid} exceeded quantum (${timeQuantumInput.value}s) and returned to Ready Queue`;
            }
        }
    }

    function playAnimation() {
        if (isPlaying) return;
        isPlaying = true;
        btnPlay.disabled = true;
        btnPause.disabled = false;

        const speed = 2200 - parseInt(speedSlider.value, 10);

        animInterval = setInterval(() => {
            updateAnimationStep(currentAnimStep);
            currentAnimStep++;
            if (currentAnimStep >= currentSimulationData.gantt_chart.length) {
                pauseAnimation();
            }
        }, speed);
    }

    function pauseAnimation() {
        isPlaying = false;
        clearInterval(animInterval);
        btnPlay.disabled = false;
        btnPause.disabled = true;
    }

    function resetAnimation() {
        pauseAnimation();
        currentAnimStep = 0;
        clearStateBoxes();
        if (currentSimulationData && currentSimulationData.gantt_chart.length > 0) {
            updateAnimationStep(0);
        }
    }

    btnPlay.addEventListener("click", playAnimation);
    btnPause.addEventListener("click", pauseAnimation);
    btnResetAnim.addEventListener("click", resetAnimation);
});
