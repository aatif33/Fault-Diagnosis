# RAG.md — PROTOSEM Legacy Manufacturing Fault Diagnosis

**Project:** Intelligent Fault Diagnosis for Legacy Manufacturing Equipment  
**Working prototype name in earlier implementation notes:** Vortiq CNC AI  
**Problem owner / domain guidance:** Nunnari Labs Private Limited  
**Programme / technical mentorship:** FORGE Innovation & Ventures  
**Primary use:** Local, evidence-grounded support for maintenance technicians working with legacy manufacturing equipment  
**Document status:** Working knowledge base and retrieval design specification  
**Last consolidated:** 13 October 2026

> **Important status note:** This file consolidates the supplied Statement of Work (SoW), System Requirements Document (SRD), the Vortiq implementation handoff, and earlier project discussions. The implementation handoff states that Qwen fine-tuning had not yet been run at the time that handoff was written. The current project update says the model now gives basic error/cause/solution details. These statements do not establish whether that improvement came from fine-tuning, retrieval, prompt changes, or a combination. Record the current model version, training method, dataset version, and evaluation results before describing the model as fine-tuned or validated.

---

## 1. Purpose of this file

This file is the first structured knowledge source for a local Retrieval-Augmented Generation (RAG) system supporting fault diagnosis on legacy manufacturing equipment.

It is intended to help the system:

1. Explain a detected alarm or fault using relevant machine documentation.
2. Describe the technical background in language a maintenance technician can understand.
3. Separate documented facts from hypotheses and unknowns.
4. Retrieve appropriate inspection and diagnostic checks.
5. Explain why a check is relevant and what evidence would support or weaken a possible cause.
6. Keep a traceable link between every factual claim and its source.
7. Avoid inventing causes, procedures, parameter values, wiring details, or machine states.
8. Preserve the hard boundary that the system is **read-only** and does not control machine operation.

This is not an OEM service manual and must not override the machine manufacturer's documentation, site procedures, or a qualified maintenance engineer. It is a structured retrieval layer that organizes verified evidence. It must not be treated as proof that a particular fault has been diagnosed correctly.

## 2. Project context and intended scope

Legacy manufacturing machines can remain productive for many years while using older interfaces, vendor-specific protocols, incomplete documentation, paper manuals, and undocumented maintenance knowledge. Troubleshooting can therefore depend heavily on experienced technicians interpreting alarms, readings, and machine history.

The project aims to build a **Minimum Usable Prototype (MUP)** of an edge-deployed Agentic AI layer that:

- Connects to legacy machines using approved interfaces.
- Collects data without writing to or controlling the machine.
- Normalizes machine-specific data into a common representation.
- Detects fault or stop conditions using structured, deterministic logic.
- Retrieves relevant technical documentation and historical evidence.
- Runs bounded diagnostic probes that are explicitly read-only.
- Produces ranked fault hypotheses with supporting evidence.
- Shows technicians the evidence, uncertainty, and recommended checks.
- Records diagnosis history and technician-confirmed outcomes.
- Maintains a reusable machine profile and documentation history.
- Operates locally without requiring cloud inference for core diagnosis.

### In-scope capabilities

- Read-only connectivity through supported interfaces such as RS-232, RS-485, Ethernet, and isolated digital I/O, subject to the agreed protocol scope and host-site approval.
- Protocol adapters that map machine-specific signals into a common data model.
- Fault/alarm identification using exact machine/controller scope.
- Retrieval from manuals, alarm tables, troubleshooting documents, maintenance records, scanned pages, photographs, and validated historical fault records.
- Deterministic signal checks and read-only diagnostic probe sequences.
- Local technician interface, evidence display, audit trail, and technician feedback.
- English and Tamil interface support.
- Machine-profile generation and versioning.

### Explicitly out of scope

The system must not:

- Send commands that reset, acknowledge, clear, start, stop, jog, home, or control machine motion.
- Write CNC/PLC parameters, registers, programs, configuration, or safety settings.
- Modify, patch, or reprogram the machine controller.
- Bypass interlocks or safety systems.
- Make safety-critical decisions or autonomously authorize a repair.
- Claim predictive maintenance, remaining-useful-life estimation, or failure forecasting as a project capability.
- Require cloud access for core diagnosis.
- Present a model-generated answer as a confirmed root cause without sufficient evidence.

**Read-only is a design constraint, not a UI option.** It must be enforced at the adapter and hardware/interface layers, not merely through a prompt telling the model not to write.

---

## 3. System architecture and responsibility boundaries

The intended diagnostic path is:

```text
Legacy machine / approved external sensors
                 |
                 v
     Read-only hardware interface
                 |
                 v
       Machine-specific adapter
                 |
                 v
      Normalized machine data model
                 |
       +---------+----------+
       |                    |
       v                    v
Deterministic signal    Event/history store
checks and probes       (local database)
       |                    |
       +---------+----------+
                 |
                 v
       Fault/alarm context builder
                 |
          +------+------+
          |             |
          v             v
  Exact structured   RAG retrieval
  alarm lookup       from manuals,
                     records and profiles
          |             |
          +------+------+
                 |
                 v
       Bounded diagnostic reasoning
       (local Small Language Model)
                 |
                 v
  Ranked hypotheses + evidence + uncertainty
                 |
                 v
       Technician-facing dashboard
                 |
                 v
     Technician-confirmed outcome/audit log
```

### What each layer is responsible for

| Layer | Responsibility | Must not do |
|---|---|---|
| Hardware/interface | Electrically/logically isolated, read-only acquisition | Drive machine inputs or expose write capability |
| Protocol adapter | Decode supported protocol fields and report quality/status | Guess unknown registers or silently substitute values |
| Normalization | Convert known fields into common units/types | Remove the original raw value or its provenance |
| Deterministic checks | Thresholds, state transitions, rule checks, safe read-only probes | Let an LLM choose arbitrary raw signals or issue commands |
| Structured alarm database | Exact controller/model + code lookup | Return an arbitrary record based only on a shared alarm code |
| RAG retrieval | Find relevant manual passages, procedures, signal maps, and historical records | Treat a semantically similar passage as proof for a different controller |
| Local language model | Explain retrieved evidence and compare bounded hypotheses | Invent evidence, signal interpretation, confidence, or corrective actions |
| Dashboard | Present state, alarm, evidence, uncertainty, and audit trail | Hide source references or imply the machine is safe to operate |
| Technician | Verify evidence, perform approved work, record actual cause/action | Be replaced by autonomous AI decisions |

### Model role

The local Small Language Model (SLM) is best used for retrieval-assisted explanation, classification within a bounded set of options, comparison of documented hypotheses, natural-language interaction, and drafting machine documentation. It should not be relied on to interpret dense sensor streams or infer machine state directly from unprocessed values.

Signal interpretation and deviation detection should be handled by deterministic rules and, if justified by data, specialized time-series or conventional ML methods. The model should receive already-normalized readings and the results of known checks.

---

## 4. Knowledge-source hierarchy and evidence quality

The RAG system must preserve the difference between an authoritative source, a local record, an observed value, a technician hypothesis, and model-generated text.

### Recommended source priority

1. **Applicable OEM manual or official controller documentation** for the exact manufacturer, controller family, model, and manual revision.
2. **Approved machine-specific documentation** supplied by the host site, including electrical drawings, signal maps, parameter descriptions, and machine manuals.
3. **Validated maintenance procedure** approved by the responsible engineer or host site.
4. **Technician-confirmed historical fault record** with machine identity, observed evidence, actual cause, corrective action, and outcome.
5. **Structured alarm dataset** whose source has been checked and whose controller scope is known.
6. **Unverified third-party content or imported records** — usable as a search lead only, not as final authority.
7. **Model prior knowledge** — never sufficient by itself to establish an alarm definition or machine-specific procedure.

A `source_manual` or `source_url` field is not proof that a record is official. The source itself must be checked. A record with missing provenance must be marked unverified.

### Evidence status vocabulary

Use these labels consistently:

- `VERIFIED_OEM`: checked against an applicable official OEM document.
- `VERIFIED_SITE`: reviewed and approved for the specific machine by the host site or qualified engineer.
- `TECHNICIAN_CONFIRMED`: outcome recorded by a technician after a real case; include who/when where permitted.
- `SECONDARY_SOURCE`: sourced from a non-OEM reference; not yet verified.
- `UNVERIFIED`: source or applicability has not been established.
- `CONFLICTING`: two or more sources disagree.
- `INCOMPLETE`: useful record, but key fields are missing.
- `SUPERSEDED`: retained for audit, but a newer applicable revision exists.

The retrieval layer should prefer verified applicable sources, but it must not hide conflicts. If sources disagree, display the conflict and ask for engineering review instead of silently selecting one.

### Minimum source metadata

Every retrievable chunk or record should carry, where available:

```yaml
source_id: unique stable ID
source_title: title of manual, document, or record
source_type: OEM_MANUAL | SITE_DOCUMENT | ALARM_TABLE | TROUBLESHOOTING | HISTORY | MACHINE_PROFILE
manufacturer: manufacturer name
machine_type: lathe | milling_machine | other | unknown
controller_family: exact family or unknown
controller_model: exact model or unknown
machine_id: site machine identifier, if applicable
manual_revision: revision/date if available
page_number: page or section number, if applicable
section_heading: original heading
source_url_or_path: local path or URL
verification_status: one status from the vocabulary above
verified_by: reviewer/role if applicable
verified_at: ISO-8601 timestamp if applicable
effective_scope: models/variants the source applies to
language: en | ta | other
chunk_id: stable chunk identifier
ingested_at: ISO-8601 timestamp
```

Do not fabricate missing metadata. Use `unknown` or `null` and lower the evidence status as appropriate.

---

## 5. Alarm identity and exact matching

An alarm code must never be interpreted in isolation when different manufacturers or controller families may reuse the same code.

### Required identity tuple

At minimum, use:

```text
manufacturer + controller family/model + alarm code
```

Where available, include machine model, controller software/version, and the applicable manual revision.

### Matching policy

1. Normalize harmless formatting differences only (for example, trim surrounding whitespace and normalize case where the controller's code semantics allow it).
2. Preserve meaningful prefixes, suffixes, leading zeros, punctuation, and alphanumeric characters.
3. Do not convert an alarm code to an integer.
4. Search for an exact code within the exact controller scope first.
5. If one exact applicable record is found, return it with source metadata.
6. If multiple applicable records conflict, return an ambiguity/conflict result.
7. If the controller scope is missing or only a code-only match is possible, ask for the controller/model or state that the record cannot be safely identified.
8. Do not fall back silently to a record from a different controller.
9. If no applicable record exists, report “No verified matching record found” and provide only generic, clearly labelled next steps such as obtaining the correct manual or asking a qualified technician to identify the controller.

### Why this matters

The project handoff documents a concrete hallucination: when the first frontend sent `FANUC Series 0i-D` and `SV0411` directly to Qwen, the model returned a spindle-speed-related explanation. The structured database lookup instead returned the record labelled `EXCESS ERROR (MOVING)` and associated with servo/position control.

This demonstrates the reason for exact retrieval: fluent model output is not a substitute for an applicable alarm reference.

---

## 6. Structured alarm knowledge schema

Structured alarm records should remain separate from long-form RAG chunks. Use exact database lookup for codes and RAG for explanatory passages.

Recommended normalized record:

```yaml
record_id: stable unique ID
manufacturer: FANUC
machine_type: milling_machine
controller_family: Series 0i
controller_model: Series 0i-D
controller_scope: exact documented applicability
alarm_code: "SV0411"
alarm_message: "EXCESS ERROR (MOVING)"
official_description: "Position deviation during travel exceeded parameter No. 1828."
affected_component: "Servo / position control"
documented_possible_causes: []  # Populate only from a verified source
documented_corrective_actions: []  # Populate only from a verified source
severity: unknown
source_id: reference to source metadata
verification_status: UNVERIFIED  # Change only after source review
last_reviewed_at: null
notes: "Do not infer missing causes or solutions."
```

**The example above deliberately leaves causes, actions, and severity empty.** The supplied handoff supports the code, message, description, and component label, but it does not provide a verified, complete cause list or corrective procedure. Do not fill these fields from guesswork.

### Import/data-cleaning rules

The current implementation handoff describes three CSVs:

- `alarm.csv`: 31 FANUC records, 11 columns.
- `alarm2.csv`: 14 Haas records, 9 columns.
- `alarm3.csv`: 14 Haas records, 12 columns.

That is 59 raw rows before deduplication, not 59 verified unique alarm conditions. Some Haas codes (including 107, 120, and 123) appeared in both files during earlier inspection. The CSV column names differ.

Before treating the data as a trusted knowledge base:

- Map synonymous column names into a single schema.
- Preserve the original row and source file for audit.
- Normalize controller labels without losing the original literal value.
- Preserve alarm codes as strings.
- Detect duplicates using controller scope + code + source and content.
- Do not merge records merely because their codes match.
- Flag contradictory descriptions and corrective actions.
- Verify source manuals, URLs, revisions, and applicability.
- Keep missing values missing; never create causes or actions to make records look complete.
- Keep a validation status and record-level audit trail.

Suggested normalized fields:

```text
record_id, manufacturer, machine_type, controller_family, controller_model,
controller_scope, alarm_code, alarm_message, official_description,
documented_possible_causes, documented_corrective_actions, affected_component,
severity, source_id, source_title, source_manual_revision, source_url_or_path,
verification_status, reviewed_by, reviewed_at, original_file, original_row
```

---

## 7. Long-document ingestion and chunking

RAG should support PDF manuals, plain-text documents, alarm tables, scanned manual pages, photographs of technical documents, troubleshooting documents, and historical fault records. Use OCR when a document is image-based; preserve the page image and OCR text together when practical so uncertain readings can be checked.

### Ingestion pipeline

1. **Register the source** and record its origin, owner, revision, and verification status.
2. **Extract text** while preserving page numbers, section headings, tables, warning blocks, and figure captions.
3. **OCR when required** for scanned pages or photographs.
4. **Review OCR quality** for alarm codes, parameter numbers, units, polarity, decimal points, terminal labels, and tables. These are high-risk OCR fields.
5. **Split by semantic structure**: manual section, alarm entry, procedure, table row/group, warning, or machine-profile section.
6. **Attach metadata** to every chunk, including controller scope and source page.
7. **Index locally** in a keyword index and/or local vector index.
8. **Run retrieval tests** using known questions and exact alarm codes.
9. **Version the index** so a source update can be traced and rolled back.
10. **Retain the source** so technicians can inspect the original page.

### Chunking recommendations

- Prefer one alarm entry per chunk for alarm tables.
- Prefer one troubleshooting procedure or coherent subsection per chunk for manuals.
- Keep safety warnings with the procedure they qualify.
- Do not split a table row away from its column headers.
- Do not join unrelated controller families into one chunk.
- Keep page number, heading, model applicability, and source ID on every chunk.
- Use overlap only where needed to preserve cross-paragraph context; do not create duplicate chunks that can dominate retrieval.
- Avoid excessively large chunks that bury the relevant instruction in unrelated material.
- Store the original document and the extracted chunk separately.

Chunk size and overlap should be selected through retrieval testing rather than treated as universal constants. A practical starting point is a few hundred tokens per prose chunk, with smaller chunks for alarm rows and tables. Preserve larger procedure blocks when splitting them would separate a step from its warning or prerequisite.

### Hybrid retrieval

Use a combination of:

- **Exact structured lookup** for manufacturer/controller/alarm code.
- **Keyword/BM25 retrieval** for exact terms, parameter numbers, alarm text, terminal labels, and codes.
- **Vector retrieval** for semantically phrased questions such as “why does the axis lag during travel?”
- **Metadata filters** for manufacturer, controller, machine ID, source status, and revision.
- **Reranking** where feasible to order relevant results after initial retrieval.

Do not rely on vector similarity alone for exact alarm identification. Exact identifiers often carry more weight than semantic similarity.

---

## 8. Retrieval and context-building procedure

For each diagnostic request, build a context package before calling the language model.

### Step A — Establish the case

Capture as many of these as are available:

```yaml
case_id: unique case identifier
observed_at: ISO-8601 timestamp from the application
machine_id: site identifier or unknown
manufacturer: known value or unknown
machine_type: known value or unknown
controller_model: exact model or unknown
controller_version: known value or unknown
alarm_code: exact string or null
alarm_text_from_machine: exact observed text or null
machine_state: RUNNING | IDLE | STOPPED | ALARM | POWER_OFF | MAINTENANCE | UNKNOWN
state_source: controller | external_sensor | technician_entry | simulator | unknown
signal_readings: normalized readings with units and quality
recent_events: relevant recent events with timestamps
operator_question: original question
```

Do not assume `ALARM` means the machine is stopped or powered off. Alarm status, execution state, and power state are separate observations.

### Step B — Retrieve exact structured alarm record

Query by the identity tuple. Return the exact record, source status, and source metadata. If the match is ambiguous, stop automatic diagnosis and request clarification.

### Step C — Retrieve relevant documentation

Use the alarm code, alarm message, affected component, controller/model, symptom description, and observed readings to search:

- OEM alarm definitions.
- Relevant troubleshooting procedure.
- Relevant signal/register descriptions.
- Warnings and prerequisites.
- Machine-specific wiring or interface documentation.
- Similar technician-confirmed cases for the same machine/controller.
- Recent machine history relevant to this event.

A similar case from another controller may be useful as a general clue, but must not be represented as the same alarm definition or an applicable procedure.

### Step D — Retrieve machine history

Include only history that is relevant to the current case, such as:

- State transitions before and after the alarm.
- Earlier occurrences of the same alarm on the same machine.
- Time since last known normal operation, if actually measured.
- Readings before/during/after the event, with units and quality.
- Previous corrective actions and whether they were technician-confirmed.
- Known maintenance or configuration changes recorded by the site.

Do not infer an event timestamp from the current application clock if the machine timestamp is unavailable. Label application-observed time and controller-reported time separately.

### Step E — Select only approved deterministic checks

Choose checks from a reviewed probe library. A probe must specify:

```yaml
probe_id: stable identifier
applicable_machine_scope: exact models/controllers
purpose: what uncertainty this check addresses
preconditions: prerequisites and safety conditions
inputs: approved read-only signals or observations
method: deterministic procedure
expected_observations: documented possible results
interpretation_rules: explicit mapping from results to evidence
stop_conditions: conditions requiring the check to stop
write_capability: none
source_ids: references for the procedure
approval_status: reviewed | unreviewed
```

The model may explain why an approved probe matters, but must not invent a new probe against raw registers or propose a write operation.

### Step F — Build a bounded context

Send the model only the relevant records, evidence, source references, and allowed actions. Clearly mark:

- `DOCUMENTED_FACT`
- `OBSERVED_MACHINE_DATA`
- `DETERMINISTIC_CHECK_RESULT`
- `TECHNICIAN_REPORTED`
- `HYPOTHESIS`
- `UNKNOWN_OR_MISSING`

This reduces the risk that the model confuses a possible cause with a confirmed cause.

---

## 9. Diagnostic reasoning policy

The goal is an evidence-based ranked list of probable causes, not a confident-sounding single answer.

### Required reasoning sequence

1. Identify the exact alarm only when the controller/model scope matches.
2. Summarize what the applicable source says the alarm means.
3. List only documented causes as documented causes.
4. Compare each candidate cause against available observations.
5. Identify missing evidence that prevents discrimination between causes.
6. Select the next relevant, approved, read-only diagnostic check.
7. Rank hypotheses using explicit evidence, not invented numerical confidence.
8. State when no candidate is sufficiently supported.
9. Show the source references used.
10. Leave final confirmation and corrective work to the qualified technician.

### Hypothesis structure

```yaml
hypothesis_id: H1
statement: concise possible cause
status: DOCUMENTED_POSSIBILITY | SUPPORTED_BY_EVIDENCE | WEAKLY_SUPPORTED | NOT_SUPPORTED | UNKNOWN
supporting_evidence:
  - evidence_id: ...
    explanation: ...
contradicting_evidence:
  - evidence_id: ...
    explanation: ...
missing_evidence:
  - ...
source_ids:
  - ...
next_read_only_check: approved probe ID or "none available"
```

Do not assign a probability such as “87% likely” unless a calibrated, evaluated statistical method actually produces that probability. A language model's self-reported confidence is not a calibrated probability. If ranking is heuristic, label it as a ranking, not a measured probability.

### Evidence rules

- An alarm description establishes what the documentation says the alarm indicates; it does not automatically establish the root cause.
- A cause listed in a manual is a possibility, not proof it occurred in this case.
- A correlation between a reading and an alarm is not automatically causation.
- Missing data is not evidence that a component is healthy.
- A sensor reading without unit, timestamp, calibration/context, or quality flag may be unusable.
- If source records conflict, surface the conflict.
- If evidence is insufficient, say so.
- Do not create parameter values, thresholds, terminal numbers, or repair steps that are absent from applicable sources.
- Do not present a suggested check as approved unless the probe library or applicable manual supports it.

---

## 10. Recommended technician-facing answer format

Use the following structure for an alarm diagnosis. Keep every section short enough to scan on a shop floor, but allow a detailed explanation when the technician asks for it.

```text
ALARM / FAULT
- Manufacturer:
- Machine:
- Controller:
- Alarm code:
- Alarm message:
- Match status: Exact / Ambiguous / Not found
- Machine state: observed value or UNKNOWN
- Observed at: timestamp and source

DOCUMENTED MEANING
- Plain-language explanation:
- Source: document title, revision, page/section
- Verification status:

WHAT IS KNOWN
- Facts directly supported by the alarm record or readings.

POSSIBLE CAUSES
1. Cause — documented or hypothesized?
   - Supporting evidence:
   - Contradicting evidence:
   - Missing evidence:
   - Source:

RECOMMENDED NEXT CHECK
- Approved read-only check:
- Why it is relevant:
- Expected observations:
- How to interpret results:
- Preconditions / stop conditions:
- Source:

LIMITATIONS / UNCERTAINTY
- What cannot currently be concluded.
- What additional information is required.

SAFETY / AUTHORITY
- No machine command or parameter change has been made.
- Follow the applicable site procedure and qualified technician guidance.

AUDIT
- Case ID:
- Retrieved source IDs:
- Model/runtime version:
- Technician outcome: pending / recorded
```

If no exact record is found, do not fill in the “documented meaning” from the model's memory. State that the record was not found and request the missing controller/model or applicable manual.

---

## 11. Worked reference case: FANUC SV0411

This is a reference case drawn from the supplied implementation handoff. It is a retrieval and integration test case, not a complete verified troubleshooting procedure.

### Facts supported by the supplied record

- Manufacturer: FANUC.
- Controller scope described in the handoff: Series 0i-D / 0i Mate-D; the tested request used `FANUC Series 0i-D`.
- Alarm code: `SV0411`.
- Alarm message: `EXCESS ERROR (MOVING)`.
- Description: position deviation during travel exceeded parameter No. 1828.
- Affected component label: servo / position control.
- The SQLite lookup endpoint returned a record containing these fields in the recorded test.

### What this does and does not establish

It establishes that a structured lookup was reported to return the stored record for the tested controller/code combination. It does **not** prove that:

- The record was checked against the current official manual revision.
- The controller model on a real machine has been confirmed.
- The listed description applies to every Series 0i variant.
- Any particular component has failed.
- A cause or corrective action has been validated.
- The live dashboard is now using the database response.
- The system is connected to a real CNC controller.

### Safe RAG response for the current evidence

**Documented meaning:** The stored record labels SV0411 as “EXCESS ERROR (MOVING)” and describes position deviation during travel exceeding parameter No. 1828.

**Possible causes:** The currently supplied handoff does not contain a verified, complete list of causes. Do not invent one.

**Corrective action:** The currently supplied handoff does not contain a verified, applicable troubleshooting sequence. Retrieve the appropriate official FANUC manual and machine-specific documentation before giving a procedure.

**Next action:** Verify the exact controller model and applicable manual revision; retrieve the matching official alarm entry and its troubleshooting section. Any subsequent checks must be reviewed, read-only, and consistent with the host site's safety procedures.

### Integration regression test

Input:

```json
{
  "controller": "FANUC Series 0i-D",
  "alarm_code": "SV0411"
}
```

Expected behaviour:

- `/api/check-alarm` returns the exact structured record and source metadata.
- The dashboard displays `EXCESS ERROR (MOVING)` and the stored description.
- The initial alarm identification does not call the LLM as the authority for the alarm's identity.
- The model, if used, explains the retrieved record without replacing it or adding undocumented causes.
- The result includes source/verification status and makes missing cause/action information visible.
- An ambiguous controller match returns an ambiguity response instead of an arbitrary record.

The earlier handoff also reports a frontend/backend contract mismatch in the follow-up question route: the frontend sent a `question` plus an `alarm` object, while the backend expected `question`, `controller`, and `alarm_code`. Verify and align the API contract before treating follow-up chat as complete.

---

## 12. Machine data, Arduino, and sensor integration

Earlier project discussions considered collecting machine/sensor data, storing it, integrating values generated through Arduino IDE, sending structured data to a model, testing real-time inference, and displaying diagnosis on a dashboard.

This remains compatible with the current project only if sensor acquisition is treated as one approved data source within the broader read-only architecture. Arduino output by itself is not ground truth about a CNC controller and does not replace protocol adapters.

### Data path for approved external sensors

```text
Approved sensor(s)
       |
       v
Microcontroller / acquisition firmware
       |
       v
Timestamped raw reading + unit + quality
       |
       v
Local ingestion endpoint / edge service
       |
       v
Validation + normalization + derived features
       |
       +--------------------------+
       |                          |
       v                          v
Local time-series/event store   Deterministic rules
       |                          |
       +-------------+------------+
                     |
                     v
         Diagnosis context builder
                     |
             RAG + local SLM
                     |
                     v
     Evidence-backed technician display
```

### Minimum reading envelope

Each reading should include:

```yaml
machine_id: stable machine identifier
sensor_id: stable sensor identifier
timestamp: ISO-8601 with timezone
timestamp_source: device | edge_application | controller | unknown
signal_name: normalized signal name
raw_value: unmodified observed value
normalized_value: converted value or null
unit: explicit unit or unknown
sampling_rate_hz: configured/observed rate if known
quality: GOOD | STALE | MISSING | OUT_OF_RANGE | SENSOR_ERROR | UNKNOWN
calibration_reference: calibration ID/date if applicable
acquisition_source: Arduino/serial adapter/PLC/etc.
firmware_version: if available
notes: optional
```

Do not silently replace missing, stale, or invalid values with zero. Preserve raw values and flag data-quality failures. Keep timestamps and units attached through every transformation.

### Storage guidance

The current Vortiq proof of concept uses SQLite for local alarm lookup and proposes local event/history tables. SQLite is sufficient for a small single-edge-device prototype and structured alarm knowledge. For frequent time-series samples, evaluate expected sampling rate, retention, concurrency, and query needs before choosing a separate time-series store. Do not introduce a second database without a clear requirement.

Separate the following logical data domains:

- `alarm_knowledge`: static, source-backed alarm definitions.
- `machines`: machine identity, controller, approved interface, and profile metadata.
- `machine_events`: timestamped state transitions and events.
- `alarm_history`: each occurrence, raised/cleared time, duration, state before/during/after.
- `sensor_readings`: timestamped readings with unit, quality, and acquisition source, if required by the chosen sampling volume.
- `diagnostic_cases`: retrieval results, hypotheses, checks, sources, and final outcome.
- `technician_feedback`: actual cause, corrective action, observations, and reviewer details.

These are proposed logical entities, not proof that all tables are currently implemented.

### Do not confuse these states

- `alarm_status`: whether an alarm is present.
- `machine_execution_state`: running, idle, stopped, or unknown.
- `power_state`: powered, off, or unknown.
- `program_state`: executing, paused, complete, or unknown.
- `spindle_state`: running, stopped, or unknown.

One must not be inferred from another unless a documented machine-specific rule supports the inference.

### Real-time diagnosis

“Real-time” must be defined as a measurable latency target. Record the time from acquisition to display and the configured poll/sampling interval. The polling rate must not degrade the machine's control performance. If the connection is lost or data becomes stale, report that status rather than continuing to present old values as current.

---

## 13. Event logging and technician feedback

The event/history workflow was proposed but not fully verified in the implementation handoff.

### Minimum event lifecycle

1. Record a machine state observation with timestamp and source.
2. Detect an alarm or stop condition using a defined rule.
3. Create an event/case record.
4. Snapshot the relevant readings and data-quality flags.
5. Retrieve alarm knowledge and supporting documentation.
6. Record the generated hypotheses and sources.
7. Record approved checks and their observed results.
8. Record when the alarm clears, if clearing is actually observed.
9. Calculate duration only when both start and end timestamps are available and comparable.
10. Ask the technician to record actual cause, corrective action, and observations.
11. Mark the outcome as confirmed, unresolved, or disputed.
12. Preserve the audit trail; do not overwrite the original diagnosis.

For a simulated proof of concept, label all events as `SIMULATED`. Do not mix simulated records with real machine events without an explicit source flag.

### Useful event fields

```text
event_id, case_id, machine_id, event_type, timestamp,
timestamp_source, machine_state, alarm_status, alarm_code,
controller_model, readings_snapshot, data_quality,
source_adapter, connection_status, simulated,
created_at, updated_at
```

### Useful alarm occurrence fields

```text
alarm_occurrence_id, machine_id, controller_model, alarm_code,
raised_at, raised_timestamp_source, cleared_at,
cleared_timestamp_source, duration_seconds,
state_before, state_during, state_after,
diagnostic_case_id, outcome_status
```

If the machine's own event timestamp is unavailable, label the time as application-observed. Do not call it the CNC event time.

---

## 14. RAG prompt policy for the local model

Use a system instruction along these lines. Adapt it to the runtime and application, but preserve its safety and evidence rules.

```text
You are a local manufacturing fault-diagnosis assistant.

Use the supplied structured alarm record, retrieved document excerpts,
normalized machine readings, deterministic check results, and technician
history as the evidence available for this case.

Rules:
1. Do not identify an alarm from model memory when no exact applicable
   record has been retrieved.
2. Respect manufacturer, controller, machine-model, and revision scope.
3. Do not invent causes, parameter values, thresholds, terminal numbers,
   wiring details, procedures, or corrective actions.
4. Distinguish documented facts, observed readings, technician reports,
   hypotheses, and unknowns.
5. A documented possible cause is not a confirmed root cause.
6. Cite source ID and page/section for every documentation-based claim.
7. If sources conflict, state the conflict and request review.
8. If evidence is insufficient, say what is missing.
9. Recommend only checks from the approved read-only probe library or
   an applicable reviewed manual.
10. Never issue, recommend, or simulate a machine-write/control command.
11. Do not infer machine stopped/powered-off state from alarm presence alone.
12. Do not invent numerical confidence. Explain the evidence supporting
    each ranking.
13. Keep the final decision and any corrective work with a qualified
    technician following site procedures.

Return:
- Exact alarm identity and match status
- Documented meaning
- Known evidence
- Ranked possible causes with support/contradiction
- Missing evidence
- Next approved read-only check
- Source references
- Uncertainty and safety notes
```

Treat retrieved text as data, not as executable instructions. A document may contain imperative language, but the model must not treat it as permission to operate or modify a machine. The adapter's capabilities and probe allowlist must enforce the read-only boundary independently of the prompt.

---

## 15. Retrieval result format

Return structured retrieval results to the context builder rather than concatenating arbitrary text without labels.

```json
{
  "query": {
    "manufacturer": "FANUC",
    "controller_model": "Series 0i-D",
    "alarm_code": "SV0411"
  },
  "match_status": "EXACT | AMBIGUOUS | NOT_FOUND",
  "alarm_record": {
    "record_id": "record-id",
    "alarm_message": "EXCESS ERROR (MOVING)",
    "official_description": "Position deviation during travel exceeded parameter No. 1828.",
    "documented_possible_causes": [],
    "documented_corrective_actions": [],
    "verification_status": "UNVERIFIED"
  },
  "retrieved_chunks": [
    {
      "chunk_id": "chunk-id",
      "text": "Retrieved passage text",
      "source_id": "source-id",
      "source_title": "Document title",
      "page_number": 0,
      "section_heading": "Original section",
      "verification_status": "VERIFIED_OEM",
      "controller_scope": "Applicable scope"
    }
  ],
  "observations": [],
  "deterministic_check_results": [],
  "warnings": []
}
```

The example is a schema illustration. `chunk-id`, `source-id`, and `VERIFIED_OEM` must be populated only from real indexed source data. Do not present placeholder IDs as actual citations.

Recommended API behaviour:

- Return `match_status=AMBIGUOUS` when several records match.
- Return `match_status=NOT_FOUND` when no applicable record exists.
- Return source metadata and data-quality warnings.
- Keep raw and normalized values available for audit.
- Do not make the model responsible for correcting malformed API results.

---

## 16. Evaluation and acceptance tests

Evaluate retrieval, diagnosis, and UI integration separately. A plausible answer is not sufficient evidence that the system works.

### Retrieval tests

- Exact controller + exact code returns the intended record.
- Same code under a different controller does not return the wrong record.
- Missing controller context produces a clarification/ambiguity response.
- Conflicting sources are surfaced.
- Unverified sources are labelled.
- OCR-extracted alarm codes and parameter numbers are checked against source pages.
- Retrieval returns relevant page/section references.
- Outdated revisions are not silently treated as current.
- No-match queries do not trigger an invented definition.

### Diagnosis tests

- Every documented claim is traceable to a source or observed reading.
- Possible causes are not presented as confirmed root causes.
- Missing evidence is explicitly listed.
- Suggested probes exist in the approved library.
- The model does not invent parameter values, thresholds, or corrective procedures.
- Confidence is not reported as a calibrated probability unless measured.
- Machine state is not inferred from alarm presence alone.
- A failed or stale sensor is surfaced as a data-quality issue.
- Conflicting evidence reduces certainty rather than being ignored.

### Integration tests

- `CHECK ALARM` calls the Flask endpoint, not the old direct-Ollama identification path.
- The response shown in the dashboard matches the structured backend record.
- Follow-up chat sends the API fields the backend actually expects.
- Ollama is called only after the backend has built the context.
- Source references and verification status are visible.
- A database/API/model failure is reported clearly; it does not produce a fabricated diagnosis.
- Refreshing the page does not restore a stale hard-coded or cached answer.

### Project-level acceptance targets from the SoW/SRD

The SoW describes a target of at least 15 distinct fault/alarm conditions with associated diagnostic probe sequences, and the correct cause appearing in the top three results for at least 60% of held-out real-fault cases, judged by the host maintenance engineer. Treat this as a project acceptance target, not as an achieved result.

The SoW also calls for demonstrating connectivity to at least three machines across at least two protocol families, including one serial-only machine. This is a machine-connectivity milestone, not something that can be proven by testing a CSV lookup.

Track metrics separately:

- Exact alarm retrieval accuracy.
- Correct controller-scope matching.
- Retrieval relevance and source correctness.
- Unsupported-claim rate.
- Top-3 cause inclusion on held-out real/validated cases.
- Probe validity.
- End-to-end latency.
- Data freshness and connection-loss detection.
- Technician validation results.
- Read-only safety verification.

Do not mix simulated cases with held-out real-fault cases in reported results.

---

## 17. Current implementation state and known gaps

This section records the state described by the supplied implementation handoff. It must be updated when the actual code or test evidence changes.

### Reported as implemented or tested

- Ollama 0.34.0 was installed on Windows.
- Base model `qwen2.5:3b` was downloaded and listed successfully.
- An HTML/CSS/JavaScript dashboard was created.
- A Flask backend was started after installing `flask-cors`.
- SQLite lookup for FANUC `SV0411` returned a record containing the stored alarm message and component fields.
- An earlier direct call to Qwen produced an incorrect spindle-related explanation for `SV0411`.
- A revised frontend was supplied to use the Flask lookup rather than relying on Qwen for initial alarm identity.

### Reported as incomplete or not verified in the handoff

- Full CSV normalization, source verification, deduplication, and conflict resolution.
- Successful full import of all three CSV files into the current database.
- Final browser-to-Flask-to-SQLite integration.
- Consistency between the follow-up chat payload and backend API contract.
- Safe handling of ambiguous controller/code matches.
- Machine-event and alarm-history workflow.
- Actual CNC controller connectivity.
- Live telemetry and alarm-duration validation.
- RAG over manuals, scanned pages, and maintenance documents.
- Complete retrieval evaluation and held-out fault evaluation.

### Training status must be reconciled

The handoff supplied in this conversation says no QLoRA/LoRA or supervised fine-tuning run had occurred at that time. The latest project message says the model is now trained enough to provide basic error, cause, and solution details. Before treating the model as trained, record:

```yaml
base_model: exact model ID
training_method: prompt_only | RAG_only | SFT | LoRA | QLoRA | other
training_data_version: version/hash/path
training_example_count: integer or unknown
train_validation_test_split: details or unknown
adapter_or_checkpoint_path: path or unknown
training_date: ISO-8601 or unknown
evaluation_dataset: version/path or unknown
evaluation_metrics: measured values or unknown
known_failure_cases: list
```

A model that produces better answers after adding a structured database or RAG may be improved without having been fine-tuned. These are different mechanisms and should be documented accurately.

### Immediate engineering priorities

1. Inspect the actual project directory and current database schema/data.
2. Confirm that exact alarm lookup and the dashboard response agree.
3. Fix the follow-up API contract and reject ambiguous matches.
4. Validate the CSV sources and normalize the dataset.
5. Ingest the applicable manuals and troubleshooting documents into RAG.
6. Implement chunk metadata, source references, and evidence-status labels.
7. Create and review deterministic read-only probe sequences for at least 15 distinct conditions, per the stated target.
8. Verify the model's current training/retrieval method and measure performance on held-out cases.
9. Implement and test event/history recording.
10. Validate the system against real or host-approved fault scenarios with a maintenance engineer.
11. Only then claim end-to-end MUP completion.

---

## 18. Known gaps, risks, and mitigations

| Risk | Why it matters | Required mitigation |
|---|---|---|
| Wrong controller match | Same code may mean different things across controllers | Exact scoped matching; reject ambiguous results |
| Hallucinated alarm meaning | Fluent text may be wrong | Structured lookup first; RAG evidence; no unsupported claims |
| Unverified CSV records | A populated source field does not prove accuracy | Verify the original manual/source and record status |
| Too little training data | Current handoff describes only 59 raw CSV rows before deduplication | Prioritize retrieval and deterministic logic; avoid overclaiming generalization |
| LLM interprets raw sensor values | Small models can misread dense signals and units | Normalize and analyze signals deterministically before LLM use |
| Unsafe diagnostic suggestion | Could lead to machine or operator risk | Approved probe library, human review, no write-capable adapter |
| Stale telemetry | Old values may look current | Timestamp and quality flags; explicit stale/connection-loss state |
| OCR error | A single digit or sign can change a parameter or procedure | Validate critical OCR fields against page images |
| Source conflict | Conflicting manuals or revisions can mislead diagnosis | Surface conflict and request engineering review |
| Fake confidence | Self-reported LLM confidence is not calibrated | Evidence-based ranking; evaluate any numerical score |
| Simulated data reported as real | Inflates validation claims | Label simulation at acquisition and in all reports |
| Database and frontend drift | Dashboard may display old or incorrect answer | API contract tests and browser network verification |
| Cloud dependency | Violates local-diagnosis requirement | Keep retrieval, inference, and core storage local |
| Connection affects machine | Violates the central requirement | Electrical/logical isolation, read-only interfaces, site approval |

---

## 19. Suggested repository layout

A practical layout that separates code, raw sources, normalized knowledge, retrieval index, and tests:

```text
project/
├── app.py
├── database.py
├── index.html
├── style.css
├── script.js
├── RAG.md
├── config/
│   ├── machine_profiles/
│   └── approved_probes/
├── data/
│   ├── raw/
│   │   ├── alarm.csv
│   │   ├── alarm2.csv
│   │   └── alarm3.csv
│   ├── normalized/
│   │   └── master_alarms.csv
│   ├── documents/
│   │   ├── manuals/
│   │   ├── troubleshooting/
│   │   ├── maintenance/
│   │   └── scanned_pages/
│   └── history/
├── rag/
│   ├── ingest.py
│   ├── chunk.py
│   ├── index.py
│   ├── retrieve.py
│   └── context_builder.py
├── training/
│   ├── train.jsonl
│   ├── validation.jsonl
│   └── test.jsonl
├── tests/
│   ├── test_exact_alarm_lookup.py
│   ├── test_ambiguous_match.py
│   ├── test_retrieval_sources.py
│   ├── test_no_unsupported_claims.py
│   └── test_api_contract.py
└── logs/
```

This is a proposed structure, not a statement that these files currently exist. Keep the original uploaded documents immutable; store cleaned/extracted versions separately.

---

## 20. Glossary

- **Alarm dictionary / alarm knowledge:** Structured records describing alarm codes, messages, scope, documented meaning, and references.
- **Agentic diagnostic layer:** A bounded workflow that gathers evidence, retrieves knowledge, selects approved checks, compares hypotheses, and presents results. “Agentic” must not mean autonomous machine control.
- **Common machine-data model:** A consistent representation of machine state, alarms, axes, spindle, I/O, program/job, cycle, and signal data across different adapters.
- **Deterministic probe:** A pre-defined, reviewed read-only check with known inputs and interpretation rules.
- **Edge deployment:** Running acquisition, storage, retrieval, and inference on local hardware near the machine.
- **Hallucination:** Model-generated information that is unsupported or incorrect.
- **Machine profile:** Versioned record of the machine interface, protocol, signal map, alarm dictionary, observed behaviour, and related documentation.
- **MUP:** Minimum Usable Prototype.
- **Normalization:** Converting machine-specific data into standard names, types, units, and quality flags while preserving raw values.
- **RAG:** Retrieval-Augmented Generation; the system retrieves relevant source material and supplies it to the model to ground the response.
- **Read-only:** The system can observe approved machine information but cannot write parameters, issue control commands, or influence machine motion.
- **SLM:** Small Language Model, a compact local language model used for bounded language/retrieval tasks.
- **SFT:** Supervised fine-tuning using examples of desired inputs and outputs.
- **LoRA/QLoRA:** Parameter-efficient fine-tuning methods. They are distinct from RAG and are not required for a working retrieval pipeline.
- **Source provenance:** Information showing where a claim or data record came from, its revision, applicability, and verification status.
- **Top-3 cause inclusion:** Whether the maintenance engineer's accepted cause appears among the three highest-ranked hypotheses.

---

## 21. Source basis and limits of this document

This file consolidates information from:

1. **System Requirements Document (SRD), Version 1, 20 August 2026**, prepared by Nunnari Labs Private Limited for FORGE Innovation & Ventures. It defines the five-layer architecture, local operation, read-only constraint, deterministic signal interpretation/probing, RAG over manuals and scanned documentation, machine profile, technician UI, audit history, and reliability/security requirements.
2. **Statement of Work (SoW), dated 01/09/2026**, for the challenge “Intelligent Fault Diagnosis for Legacy Manufacturing Equipment.” It defines the MUP scope, critical features, protocol connectivity target, 15 diagnostic conditions target, top-3 cause acceptance target, deliverables, milestones, and exclusions.
3. **Vortiq CNC AI — Complete Project Handoff & Model Training Context**, supplied as pasted text. It records the current implementation notes, the three CSV datasets, the `SV0411` example, Ollama/Qwen/Flask/SQLite architecture, known integration issues, and the training status at the time of that handoff.
4. **Earlier project discussion context**, summarized in the conversation history: data collection/storage, Arduino-generated values, real-time diagnosis, local model integration, manual retrieval, evidence/confidence display, and technician dashboard requirements.

### Limits

- The actual three CSV files and official OEM manuals were not included in the material used to write this consolidated file. Their full contents and authenticity have therefore not been independently audited here.
- The `SV0411` facts above are from the implementation handoff, not an independent check of the official FANUC manual.
- No code repository or live machine connection was inspected as part of this document creation.
- This file describes a retrieval and diagnostic design; it does not claim that all components have been implemented or validated.
- Where the source documents define a requirement, it is described as a requirement/target, not as an achieved result.
- Where a cause, corrective action, threshold, or parameter detail is absent from the supplied sources, it is intentionally left unspecified.

**Maintenance rule:** Update this file when a source is verified, a probe is approved, a machine profile changes, or a technician confirms a real fault. Record the source/revision and date of every substantive update. Never silently replace a prior diagnosis or source record.
