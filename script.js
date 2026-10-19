const API_BASE = "http://127.0.0.1:8000";

let currentAlarm = "";
let currentAlarmData = null;
let alarmDetectedAt = null;
let currentView = "dashboard";
let lastRenderedHardwareAlarmCode = null;

// -------------------------
// CLOCK
// -------------------------
function updateClock() {
    const now = new Date();
    document.getElementById("date").textContent = now.toLocaleDateString("en-IN", {
        day: "2-digit", month: "short", year: "numeric"
    });
    document.getElementById("time").textContent = now.toLocaleTimeString("en-IN");
}
setInterval(updateClock, 1000);
updateClock();

function setText(id, value, fallback = "Not available.") {
    const element = document.getElementById(id);
    if (element) element.textContent = value == null || String(value).trim() === "" ? fallback : String(value);
}

function setMachineLight(state) {
    const light = document.getElementById("machineStatusLight");
    if (!light) return;
    light.classList.remove("green", "yellow", "red");
    if (state === "RUNNING") light.classList.add("green");
    else if (state === "STOPPED") light.classList.add("yellow");
    else light.classList.add("red");
}

function setSource(manual, url, section) {
    const manualElement = document.getElementById("sourceManual");
    const link = document.getElementById("sourceLink");

    const cleanLabel = (value) => String(value || "")
        .replace(/^#+\\s*/gm, "")
        .replace(/\\s*---\\s*/g, " — ")
        .replace(/\\s+/g, " ")
        .trim();

    const cleanManual = cleanLabel(manual);
    const cleanSection = cleanLabel(section);
    const sourceText = [cleanManual, cleanSection]
        .filter(Boolean)
        .filter((value, index, list) => list.indexOf(value) === index)
        .join(" — ");

    if (manualElement) {
        manualElement.textContent = sourceText || "No source manual is recorded for this alarm.";
    }

    // Only expose valid HTTP(S) links from the backend.
    let validUrl = "";
    try {
        const parsed = new URL(url || "");
        if (parsed.protocol === "http:" || parsed.protocol === "https:") validUrl = parsed.href;
    } catch (_) {}

    if (link) {
        if (validUrl) {
            link.href = validUrl;
            link.classList.remove("hidden");
        } else {
            link.removeAttribute("href");
            link.classList.add("hidden");
        }
    }
}

// -------------------------
// CHECK ALARM
// -------------------------
async function checkAlarm() {
    const alarmCode = document.getElementById("alarmCode").value.trim();
    const machineState = document.getElementById("machineState").value;

    if (!alarmCode) {
        alert("Please enter an alarm code.");
        return;
    }

    currentAlarm = alarmCode;
    currentAlarmData = null;
    alarmDetectedAt = new Date();

    document.getElementById("resultSection").classList.add("hidden");
    document.getElementById("chatSection").classList.add("hidden");

    setText("machineStatus", machineState);
    setMachineLight(machineState);
    setText("resultCode", alarmCode);
    setText("resultMachine", machineState);
    setText("detectedTime", alarmDetectedAt.toLocaleString("en-IN"));

    const button = document.getElementById("checkBtn");
    button.disabled = true;
    button.textContent = "SEARCHING...";

    try {
        const response = await fetch(`${API_BASE}/api/search-alarm`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ alarm_code: alarmCode })
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok || !data.success) {
            throw new Error(data.message || "Alarm search failed.");
        }

        if (!data.matches || data.matches.length === 0) {
            document.getElementById("resultSection").classList.remove("hidden");
            setText("fault", "No exact alarm-code match was found in the local database.");
            setText("causes", "No controller-specific causes can be confirmed from the current knowledge base.");
            setText("solution", "Verify the code and add the correct OEM documentation. Related semantic results must not be treated as confirmed alarm identity.");
            setSource("", "", "");
            addChatMessage("AI", data.message || "No exact match found. Vortiq cannot safely identify this alarm from the current local records.");
            return;
        }

        let matches = data.matches;
        if (matches.length > 1) {
            const fanuc0iD = matches.filter((item) =>
                String(item.brand || "").toUpperCase().includes("FANUC") &&
                /0I-D|0I MATE-D|0I MATE D/i.test(String(item.controller_model || ""))
            );
            if (fanuc0iD.length === 1) matches = fanuc0iD;
            else {
                document.getElementById("resultSection").classList.remove("hidden");
                setText("fault", `Found ${matches.length} exact records for ${alarmCode}, but the local database cannot uniquely identify the FANUC 0i-D record.`);
                setText("causes", "No controller-specific cause can be selected safely.");
                setText("solution", "Add or correct the controller scope in the local knowledge base. Vortiq will not guess.");
                setSource("", "", "");
                addChatMessage("AI", "Multiple exact-code records exist, and no unique FANUC 0i-D / 0i Mate-D record was found. Automatic diagnosis was skipped.");
                return;
            }
        }
        await selectAlarmMatch(matches[0], machineState);
    } catch (error) {
        console.error("Alarm search failed:", error);
        document.getElementById("resultSection").classList.remove("hidden");
        setText("fault", "Unable to search the Vortiq database.");
        setText("causes", "Check that the updated backend is running.");
        setText("solution", "Run: python app.py");
    } finally {
        button.disabled = false;
        button.innerHTML = 'CHECK ALARM <span>→</span>';
    }
}

async function selectAlarmMatch(match, machineState) {
    currentAlarmData = match;

    document.getElementById("resultSection").classList.remove("hidden");
    document.getElementById("chatSection").classList.remove("hidden");

    setText("resultCode", match.alarm_code || currentAlarm);
    setText("resultMachine", machineState);
    setText("detectedTime", alarmDetectedAt ? alarmDetectedAt.toLocaleString("en-IN") : "Not recorded");
    setText("fault", match.description || match.alarm_message);
    setText("causes", match.possible_causes);
    setText("solution", match.corrective_action);
    setSource(match.source_manual || "", match.source_url || "", match.source_section || "");

    addChatMessage("AI", `Exact alarm-code match selected: ${match.alarm_code} — ${match.alarm_message || "message not recorded"}. The source record is shown below. Recovery must follow the applicable OEM procedure.`);

    // Save manually entered alarms as explicitly simulated events.
    try {
        const eventResponse = await fetch(`${API_BASE}/api/record-alarm-event`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                alarm_code: match.alarm_code || currentAlarm,
                machine_state: machineState
            })
        });
        const eventData = await eventResponse.json().catch(() => ({}));
        const status = document.getElementById("historyStatus");
        if (!eventResponse.ok || !eventData.success) {
            console.error("Alarm event save failed:", eventData.message || eventResponse.statusText);
            if (status) status.textContent = "Alarm identified, but saving the simulated event failed. Check the Flask terminal.";
        } else {
            if (status) status.textContent = eventData.already_recorded
                ? "This simulated alarm is already saved as an active history event."
                : "Simulated alarm event saved to local history.";
            if (typeof loadAlarmHistory === "function") await loadAlarmHistory();
        }
    } catch (error) {
        console.error("Alarm event save request failed:", error);
    }
}

// -------------------------
// ASK AI
// -------------------------
async function askAI() {
    const questionInput = document.getElementById("question");
    const question = questionInput.value.trim();

    if (!question) return;
    if (!currentAlarmData) {
        addChatMessage("AI", "Please check an alarm first.");
        return;
    }

    addChatMessage("YOU", question);
    questionInput.value = "";

    const button = document.getElementById("askBtn");
    button.disabled = true;

    try {
        const response = await fetch(`${API_BASE}/api/ask-ai`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question, alarm: currentAlarmData })
        });

        const data = await response.json().catch(() => ({}));

        if (!response.ok || !data.success) {
            addChatMessage("AI", data.message || "Unable to get an AI response.");
            return;
        }

        addChatMessage("AI", data.answer || "No response received.");

        // Update citation from AI endpoint when it returns source metadata.
        if (data.source || data.source_url || data.section) {
            setSource(
                data.source || currentAlarmData.source_manual || "",
                data.source_url || currentAlarmData.source_url || "",
                data.section || currentAlarmData.source_section || ""
            );
        }
    } catch (error) {
        console.error("Ask AI failed:", error);
        addChatMessage("AI", "Unable to connect to the Vortiq AI backend.");
    } finally {
        button.disabled = false;
        questionInput.focus();
    }
}


// -------------------------
// ALARM HISTORY (READ EXISTING RECORDS ONLY)
// -------------------------
function formatHistoryDate(value) {
    if (!value) return "—";
    const parsed = new Date(value);
    return Number.isNaN(parsed.getTime()) ? String(value) : parsed.toLocaleString("en-IN");
}

function formatHistoryDuration(seconds) {
    if (seconds === null || seconds === undefined || seconds === "") return "Ongoing / not recorded";
    const total = Math.max(0, Number(seconds));
    if (!Number.isFinite(total)) return "Not recorded";
    const hours = Math.floor(total / 3600);
    const minutes = Math.floor((total % 3600) / 60);
    const secs = Math.floor(total % 60);
    if (hours) return `${hours}h ${minutes}m ${secs}s`;
    if (minutes) return `${minutes}m ${secs}s`;
    return `${secs}s`;
}

async function loadAlarmHistory() {
    const status = document.getElementById("historyStatus");
    const tbody = document.getElementById("historyTableBody");
    if (!status || !tbody) return;

    status.textContent = "Loading saved alarm history...";
    tbody.replaceChildren();

    try {
        const response = await fetch(`${API_BASE}/api/alarm-history?limit=50`);
        const data = await response.json().catch(() => ({}));
        if (!response.ok || !data.success) throw new Error(data.message || "History request failed.");

        const records = Array.isArray(data.records) ? data.records : [];
        if (!records.length) {
            status.textContent = "No alarm-history records are currently stored. This view does not create or simulate machine events.";
            const row = document.createElement("tr");
            const cell = document.createElement("td");
            cell.colSpan = 6;
            cell.textContent = "No saved records";
            row.appendChild(cell);
            tbody.appendChild(row);
            return;
        }

        status.textContent = `Showing ${records.length} most recent saved record(s).`;
        for (const record of records) {
            const row = document.createElement("tr");
            const values = [
                record.alarm_code || "—",
                formatHistoryDate(record.raised_at),
                formatHistoryDate(record.cleared_at),
                formatHistoryDuration(record.duration_seconds),
                record.machine_id || "—",
                record.state_during_alarm || "—"
            ];
            for (const value of values) {
                const cell = document.createElement("td");
                cell.textContent = String(value);
                row.appendChild(cell);
            }
            tbody.appendChild(row);
        }
    } catch (error) {
        console.error("Alarm history failed:", error);
        status.textContent = "Unable to load alarm history. Check that Vortiq backend is running.";
        const row = document.createElement("tr");
        const cell = document.createElement("td");
        cell.colSpan = 6;
        cell.textContent = "History unavailable";
        row.appendChild(cell);
        tbody.appendChild(row);
    }
}

// -------------------------
// CHAT MESSAGE (safe text rendering)
// -------------------------
function addChatMessage(sender, message) {
    const container = document.getElementById("chatMessages");
    const wrapper = document.createElement("div");
    wrapper.className = sender === "YOU" ? "message user-message" : "message ai-message";

    const label = document.createElement("strong");
    label.className = "message-sender";
    label.textContent = sender;

    const body = document.createElement("div");
    body.className = "message-body";
    const text = String(message ?? "");
    const headings = [
        "Meaning:",
        "Documented information:",
        "Safe next steps:",
        "What remains unverified:"
    ];

    // Recognized headings are rendered as separate sections; content is text-only.
    if (sender !== "YOU" && headings.some((heading) => text.includes(heading))) {
        const matches = headings
            .map((heading) => ({ heading, index: text.indexOf(heading) }))
            .filter((item) => item.index >= 0)
            .sort((a, b) => a.index - b.index);

        const intro = text.slice(0, matches[0].index).trim();
        if (intro) {
            const introEl = document.createElement("p");
            introEl.className = "answer-intro";
            introEl.textContent = intro;
            body.appendChild(introEl);
        }

        matches.forEach((item, index) => {
            const end = index + 1 < matches.length ? matches[index + 1].index : text.length;
            const section = document.createElement("section");
            section.className = "answer-section";
            const title = document.createElement("strong");
            title.className = "answer-section-title";
            title.textContent = item.heading.replace(/:$/, "");
            const paragraph = document.createElement("p");
            paragraph.textContent = text.slice(item.index + item.heading.length, end).trim()
                || "Not specified in the available record.";
            section.append(title, paragraph);
            body.appendChild(section);
        });
    } else {
        body.textContent = text;
    }

    wrapper.append(label, body);
    container.appendChild(wrapper);
    container.scrollTop = container.scrollHeight;
}


// -------------------------
// DIRECT CNC FOCAS MONITOR (READ-ONLY)
// -------------------------
function renderHardwareStatus(data) {
    const pill = document.getElementById("hardwareConnection");
    const set = (id, value) => { const el = document.getElementById(id); if (el) el.textContent = value ?? "—"; };
    const connected = data.connected === true;
    if (pill) {
        pill.textContent = connected ? "CNC CONNECTED · FOCAS" : "CNC DISCONNECTED / UNKNOWN";
        pill.classList.toggle("online", connected);
        pill.classList.toggle("offline", !connected);
    }
    set("telemetryController", data.controller_model || "Unknown");
    set("telemetryMachine", data.machine_id || "CNC-FOCAS-01");
    set("telemetryAlarmCount", connected ? (data.alarms || []).length : "Unknown");
    set("telemetrySource", "FANUC FOCAS · READ ONLY");
    set("telemetryAxis", connected ? "CONNECTED" : "ALARM STATE UNKNOWN");
    set("telemetryLastSeen", data.last_seen ? new Date(data.last_seen).toLocaleTimeString("en-IN") : "No CNC response");
    const banner = document.getElementById("hardwareAlarmBanner");
    const diagnosis = document.getElementById("hardwareDiagnosis");
    const alarms = Array.isArray(data.alarms) ? data.alarms : [];
    if (banner) {
        banner.classList.remove("hidden");
        if (!connected) {
            banner.textContent = `CNC COMMUNICATION UNAVAILABLE — ${data.connection_error || "No recent controller response."} Active alarm state cannot be verified. Vortiq will not assume alarms are cleared.`;
            banner.style.borderColor = "var(--yellow)";
        } else if (alarms.length) {
            banner.textContent = `CONTROLLER-REPORTED ALARM${alarms.length === 1 ? "" : "S"}: ` + alarms.map(a => `${a.alarm_code}${a.axis ? ` (axis ${a.axis})` : ""} — ${a.message || "No message returned"}`).join(" | ");
            banner.style.borderColor = "var(--red)";
        } else {
            banner.textContent = "CNC CONNECTED — the controller currently reports no active alarm messages.";
            banner.style.borderColor = "var(--green)";
        }
    }
    if (diagnosis) { diagnosis.classList.add("hidden"); diagnosis.replaceChildren(); }
    const resultSection = document.getElementById("resultSection");
    const chatSection = document.getElementById("chatSection");
    if (!connected || alarms.length === 0) {
        lastRenderedHardwareAlarmCode = null;
        if (resultSection) resultSection.classList.add("hidden");
        if (chatSection) chatSection.classList.add("hidden");
        currentAlarmData = null;
        if (connected) { setText("machineStatus", "CONNECTED · NO ACTIVE ALARM"); setMachineLight("RUNNING"); }
        else { setText("machineStatus", "CNC CONNECTION UNKNOWN"); setMachineLight("STOPPED"); }
        return;
    }
    const alarm = alarms[0];
    currentAlarm = alarm.alarm_code;
    currentAlarmData = {
        alarm_code: alarm.alarm_code,
        alarm_message: alarm.message || `${alarm.alarm_type || "CNC"} alarm ${alarm.alarm_number}`,
        description: `The CNC controller reported ${alarm.alarm_code}${alarm.axis ? ` on axis ${alarm.axis}` : ""}. Controller message: ${alarm.message || "No text message was returned by FOCAS."}`,
        possible_causes: "Use the matching CNC/controller and machine OEM documentation to interpret this alarm. Vortiq will not guess causes when the controller model is unknown.",
        corrective_action: "Check the exact controller and machine OEM manual for this alarm. Follow the approved site procedure; Vortiq does not send commands to the CNC.",
        condition: "Read directly from the CNC controller through FANUC FOCAS. Not simulated.",
        simulation: false,
        source: "FANUC FOCAS live controller response"
    };
    if (resultSection) resultSection.classList.remove("hidden");
    if (chatSection) chatSection.classList.remove("hidden");
    setText("resultCode", alarm.alarm_code);
    setText("detectedTime", data.last_seen ? new Date(data.last_seen).toLocaleString("en-IN") : "Received from controller");
    setText("resultMachine", `${data.machine_id || "CNC"} · ${data.controller_model || "Controller unknown"}`);
    setText("fault", currentAlarmData.description);
    setText("causes", currentAlarmData.possible_causes);
    setText("solution", currentAlarmData.corrective_action);
    setSource("Live CNC controller message (FOCAS)", "", "");
    setText("machineStatus", `ALARM ACTIVE · ${alarms.length} controller alarm(s)`);
    setMachineLight("STOPPED");
    if (lastRenderedHardwareAlarmCode !== alarm.alarm_code) {
        addChatMessage("System", `Controller-reported alarm received: ${alarm.alarm_code}. ${alarm.message || "No message returned."} This is live FOCAS data, not a simulated event. Check the matching OEM manual.`);
        lastRenderedHardwareAlarmCode = alarm.alarm_code;
    }
}

async function pollHardwareStatus() {
    try {
        const response = await fetch(`${API_BASE}/api/cnc-status`, { cache: "no-store" });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        if (data.success) renderHardwareStatus(data);
    } catch (error) {
        const pill = document.getElementById("hardwareConnection");
        if (pill) { pill.textContent = "VORTIQ BACKEND OFFLINE · CNC STATE UNKNOWN"; pill.classList.add("offline"); pill.classList.remove("online"); }
    }
}
setInterval(pollHardwareStatus, 1000);
setInterval(() => { if (currentView === "history") loadAlarmHistory(); }, 3000);
window.addEventListener("DOMContentLoaded", () => { loadAlarmHistory(); pollHardwareStatus(); });




// -------------------------
// SIDEBAR VIEWS
// -------------------------
function showView(view) {
    currentView = view;
    const dashboard = document.getElementById("dashboardView");
    const history = document.getElementById("historyView");
    if (dashboard) dashboard.classList.toggle("hidden", view === "history");
    if (history) history.classList.toggle("hidden", view !== "history");

    document.querySelectorAll(".sidebar nav a[data-view]").forEach((link) => {
        const active = link.dataset.view === view || (view === "dashboard" && link.dataset.view === "status");
        link.classList.toggle("active", active);
        if (active) link.setAttribute("aria-current", "page");
        else link.removeAttribute("aria-current");
    });

    if (view === "history") loadAlarmHistory();
    if (view === "status") {
        const statusPanel = document.getElementById("machineStatusPanel");
        if (statusPanel) statusPanel.scrollIntoView({ behavior: "smooth", block: "start" });
    }
}

document.querySelectorAll(".sidebar nav a[data-view]").forEach((link) => {
    link.addEventListener("click", (event) => {
        event.preventDefault();
        const view = link.dataset.view === "status" ? "dashboard" : link.dataset.view;
        showView(view);
    });
});
