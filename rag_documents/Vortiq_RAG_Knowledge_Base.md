# Vortiq CNC Alarm Knowledge Base --- RAG Document

## Purpose

This document is a retrieval source for the Vortiq offline CNC
diagnostic assistant. It contains normalized alarm records from the
supplied FANUC and Haas CSV datasets. It is not a replacement for the
machine-specific OEM manual, site safety procedures, or a qualified
technician.

## Retrieval and safety rules

-   Match the manufacturer, controller family/model, machine type, and
    exact alarm code before using a record.
-   Do not treat identical alarm codes from different controller
    families as equivalent.
-   Use only the documented description, causes, and corrective action
    shown in each record. Do not invent missing steps, parameter values,
    reset sequences, or machine movements.
-   If the record does not answer the operator's question, state that
    the available indexed documentation is insufficient and request the
    exact controller/manual revision or a qualified technician's review.
-   Any corrective action involving electrical cabinets, servo drives,
    parameter changes, axis motion, stored energy, or safety circuits
    must follow the OEM manual and the site's lockout/tagout and
    qualification requirements.
-   The source URL and document title are retained per record where
    provided. Verify the manual revision and source provenance before
    treating an instruction as authoritative.

## Coverage and limitations

-   Records in this document: 45
-   Brands: FANUC, HAAS
-   This is an initial knowledge base assembled from the provided CSVs;
    it is not a comprehensive alarm library.
-   The Haas instruction/input/output examples are preserved where
    available as supplementary training context, not counted as
    additional unique alarm records.
-   Live machine state, alarm raise/clear timestamps, and alarm duration
    belong in Vortiq's event/history database, not in this static
    knowledge document.

## Alarm records

### Record 1: FANUC --- Alarm PS0000

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** PS0000
-   **Alarm message:** PLEASE TURN OFF POWER
-   **Affected component:** Parameter / CNC
-   **Severity:** Not specified in the available source record.

**Documented description** A parameter that requires power-off was
input.

**Documented possible causes** A parameter requiring power-off was
changed.

**Documented corrective action / troubleshooting direction** Turn CNC
power OFF and ON after the required parameter change, following the
maintenance manual.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://www.drivesul.com.br/template/imagens/manuais/manuais-fanuc/fanuc-series-0i-model-d/B-64305EN03%20-Series%200i-Model%20D%20-Maintenance%20Manual.pdf

------------------------------------------------------------------------

### Record 2: FANUC --- Alarm PS0100

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** PS0100
-   **Alarm message:** PARAMETER WRITE ENABLE
-   **Affected component:** Parameter setting
-   **Severity:** Not specified in the available source record.

**Documented description** Parameter-write-enable is active.

**Documented possible causes** PWE (parameter write enable) is set ON.

**Documented corrective action / troubleshooting direction** After
completing the intended parameter change, set parameter write enable
back to OFF and reset as specified by the manual.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://www.drivesul.com.br/template/imagens/manuais/manuais-fanuc/fanuc-series-0i-model-d/B-64305EN03%20-Series%200i-Model%20D%20-Maintenance%20Manual.pdf

------------------------------------------------------------------------

### Record 3: FANUC --- Alarm SV0401

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SV0401
-   **Alarm message:** IMPROPER V_READY OFF
-   **Affected component:** Servo amplifier / axis control
-   **Severity:** Not specified in the available source record.

**Documented description** The servo ready signal VRDY of a servo
amplifier is OFF although the position-control ready signal PRDY is ON.

**Documented possible causes** Servo amplifier not ready; another servo
alarm may be the preceding cause; power magnetic circuit around
amplifier; servo amplifier or CNC axis-control hardware fault.

**Documented corrective action / troubleshooting direction** If another
servo alarm is present, troubleshoot the first alarm first. Check the
power magnetic circuit around the amplifier and the applicable servo
amplifier/CNC axis-control hardware.

**Source document** B-64305EN/03 Appendix A; maintenance section on
SV0401

**Source URL**
https://servicetex.ru/wp-content/uploads/lib/cnc/FANUC/30i%2031i%2032i%20-MB/%D0%A0%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE%20%D0%BF%D0%BE%20%D1%82%D0%B5%D1%85%D0%BE%D0%B1%D1%81%D0%BB%D1%83%D0%B6%D0%B8%D0%B2%D0%B0%D0%BD%D0%B8%D1%8E.pdf

------------------------------------------------------------------------

### Record 4: FANUC --- Alarm SV0403

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SV0403
-   **Alarm message:** CARD/SOFT MISMATCH
-   **Affected component:** Axis control / servo software
-   **Severity:** Not specified in the available source record.

**Documented description** The combination of the axis-control card and
servo software is incorrect.

**Documented possible causes** Incorrect axis-control card; incorrect
servo software installed in flash memory.

**Documented corrective action / troubleshooting direction** Verify the
installed axis-control card and the servo software installed in flash
memory against the machine configuration.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://manuals.plus/m/a72521220f3a20e1cb0207a43607552fd815cce25b3d4085bd6123a5785d5f96.pdf

------------------------------------------------------------------------

### Record 5: FANUC --- Alarm SV0404

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SV0404
-   **Alarm message:** IMPROPER V_READY ON
-   **Affected component:** Servo control
-   **Severity:** Not specified in the available source record.

**Documented description** The servo velocity-control ready signal VRDY
is ON although position-control ready PRDY is OFF.

**Documented possible causes** Servo ready-state mismatch between
position and velocity control.

**Documented corrective action / troubleshooting direction** Check the
servo-control state and follow the FANUC servo troubleshooting procedure
for the machine configuration.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://manuals.plus/m/a72521220f3a20e1cb0207a43607552fd815cce25b3d4085bd6123a5785d5f96.pdf

------------------------------------------------------------------------

### Record 6: FANUC --- Alarm SV0409

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SV0409
-   **Alarm message:** DETECT ABNORMAL TORQUE
-   **Affected component:** Servo motor / mechanical load
-   **Severity:** Not specified in the available source record.

**Documented description** An abnormal load was detected on the servo
motor; the manual notes Cs-axis or spindle-positioning cases for
T-series configurations.

**Documented possible causes** Abnormal servo-motor load.

**Documented corrective action / troubleshooting direction** Investigate
the mechanical load and servo system using FANUC servo diagnostics. The
alarm can be cancelled by RESET according to the alarm list.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://manuals.plus/m/a72521220f3a20e1cb0207a43607552fd815cce25b3d4085bd6123a5785d5f96.pdf

------------------------------------------------------------------------

### Record 7: FANUC --- Alarm SV0410

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SV0410
-   **Alarm message:** EXCESS ERROR (STOP)
-   **Affected component:** Servo / position control
-   **Severity:** Not specified in the available source record.

**Documented description** Position deviation during stopping exceeded
the value set in parameter No. 1829.

**Documented possible causes** Stopping position deviation exceeded
parameter 1829.

**Documented corrective action / troubleshooting direction** Check the
position deviation and servo tuning/mechanical condition according to
the FANUC maintenance procedure; verify parameter No. 1829.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://manuals.plus/m/a72521220f3a20e1cb0207a43607552fd815cce25b3d4085bd6123a5785d5f96.pdf

------------------------------------------------------------------------

### Record 8: FANUC --- Alarm SV0411

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SV0411
-   **Alarm message:** EXCESS ERROR (MOVING)
-   **Affected component:** Servo / position control
-   **Severity:** Not specified in the available source record.

**Documented description** Position deviation during travel exceeded the
value set in parameter No. 1828.

**Documented possible causes** Moving position deviation exceeded
parameter 1828.

**Documented corrective action / troubleshooting direction** Check the
servo system, mechanical load and parameter No. 1828 according to FANUC
maintenance procedure.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://manuals.plus/m/a72521220f3a20e1cb0207a43607552fd815cce25b3d4085bd6123a5785d5f96.pdf

------------------------------------------------------------------------

### Record 9: FANUC --- Alarm SV0413

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SV0413
-   **Alarm message:** LSI OVERFLOW
-   **Affected component:** Servo / position control
-   **Severity:** Not specified in the available source record.

**Documented description** The counter for the amount of positional
deviation overflowed.

**Documented possible causes** Positional-deviation counter overflow.

**Documented corrective action / troubleshooting direction** Use FANUC
servo diagnostics and maintenance procedures to identify the condition
that caused the deviation counter to overflow.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://manuals.plus/m/a72521220f3a20e1cb0207a43607552fd815cce25b3d4085bd6123a5785d5f96.pdf

------------------------------------------------------------------------

### Record 10: FANUC --- Alarm SV0415

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SV0415
-   **Alarm message:** MOTION VALUE OVERFLOW
-   **Affected component:** Axis motion / CNC command
-   **Severity:** Not specified in the available source record.

**Documented description** A velocity exceeding the travel-velocity
limit was commanded.

**Documented possible causes** Commanded velocity exceeded the travel
velocity limit.

**Documented corrective action / troubleshooting direction** Check the
commanded motion and the applicable axis/velocity parameters and correct
the program or configuration as required.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://manuals.plus/m/a72521220f3a20e1cb0207a43607552fd815cce25b3d4085bd6123a5785d5f96.pdf

------------------------------------------------------------------------

### Record 11: FANUC --- Alarm SV0417

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SV0417
-   **Alarm message:** ILL DGTL SERVO PARAMETER
-   **Affected component:** Servo parameters
-   **Severity:** Not specified in the available source record.

**Documented description** An illegal digital-servo parameter was
detected.

**Documented possible causes** Possible causes include an out-of-range
motor model setting at parameter 2020, incorrect motor-rotation
direction setting at parameter 2022, or other illegal digital-servo
parameter settings.

**Documented corrective action / troubleshooting direction** Identify
the cause using the FANUC diagnostic information referenced by the alarm
list and correct the applicable servo parameters.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://manuals.plus/m/a72521220f3a20e1cb0207a43607552fd815cce25b3d4085bd6123a5785d5f96.pdf

------------------------------------------------------------------------

### Record 12: FANUC --- Alarm SV0430

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SV0430
-   **Alarm message:** SV MOTOR OVERHEAT
-   **Affected component:** Servo motor
-   **Severity:** Not specified in the available source record.

**Documented description** The servo motor overheat condition is
detected.

**Documented possible causes** Servo motor temperature/overheat
condition.

**Documented corrective action / troubleshooting direction** Inspect the
servo motor, cooling condition and associated thermal/servo circuitry
using the applicable FANUC maintenance procedure.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL** https://pdfcoffee.com/fanuc-alarm-pdf-pdf-free.html

------------------------------------------------------------------------

### Record 13: FANUC --- Alarm SV0431

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SV0431
-   **Alarm message:** CNV. OVERLOAD
-   **Affected component:** Converter / power unit
-   **Severity:** Not specified in the available source record.

**Documented description** The converter is overloaded.

**Documented possible causes** Converter overload.

**Documented corrective action / troubleshooting direction** Inspect the
converter/power system using FANUC maintenance diagnostics and the
applicable drive procedure.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL** https://pdfcoffee.com/fanuc-alarm-pdf-pdf-free.html

------------------------------------------------------------------------

### Record 14: FANUC --- Alarm SV0432

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SV0432
-   **Alarm message:** CNV. LOW VOLT CONTROL
-   **Affected component:** Converter / power supply
-   **Severity:** Not specified in the available source record.

**Documented description** The converter control-voltage condition is
too low.

**Documented possible causes** Converter control-voltage low condition.

**Documented corrective action / troubleshooting direction** Check the
converter/power-supply system and associated wiring according to the
FANUC maintenance procedure.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL** https://pdfcoffee.com/fanuc-alarm-pdf-pdf-free.html

------------------------------------------------------------------------

### Record 15: FANUC --- Alarm SV0433

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SV0433
-   **Alarm message:** CNV. LOW VOLT DC LINK
-   **Affected component:** DC link / converter
-   **Severity:** Not specified in the available source record.

**Documented description** The converter DC-link voltage is too low.

**Documented possible causes** Converter DC-link low-voltage condition.

**Documented corrective action / troubleshooting direction** Check
incoming power, converter and DC-link circuitry according to FANUC
maintenance procedure.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL** https://pdfcoffee.com/fanuc-alarm-pdf-pdf-free.html

------------------------------------------------------------------------

### Record 16: FANUC --- Alarm SV0434

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SV0434
-   **Alarm message:** INV. LOW VOLT CONTROL
-   **Affected component:** Inverter / power supply
-   **Severity:** Not specified in the available source record.

**Documented description** The inverter control-voltage condition is too
low.

**Documented possible causes** Inverter control-voltage low condition.

**Documented corrective action / troubleshooting direction** Check
inverter power/control circuitry using FANUC maintenance diagnostics.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL** https://pdfcoffee.com/fanuc-alarm-pdf-pdf-free.html

------------------------------------------------------------------------

### Record 17: FANUC --- Alarm SV0435

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SV0435
-   **Alarm message:** INV. LOW VOLT DC LINK
-   **Affected component:** DC link / inverter
-   **Severity:** Not specified in the available source record.

**Documented description** The inverter DC-link voltage is too low.

**Documented possible causes** Inverter DC-link low-voltage condition.

**Documented corrective action / troubleshooting direction** Check the
inverter, DC-link circuit and incoming power according to FANUC
maintenance procedure.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL** https://pdfcoffee.com/fanuc-alarm-pdf-pdf-free.html

------------------------------------------------------------------------

### Record 18: FANUC --- Alarm SV0436

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SV0436
-   **Alarm message:** SOFTTHERMAL (OVC)
-   **Affected component:** Servo / motor
-   **Severity:** Not specified in the available source record.

**Documented description** A soft-thermal/overload condition is detected
in the servo system.

**Documented possible causes** Servo overload/thermal accumulation.

**Documented corrective action / troubleshooting direction** Check servo
load, acceleration/deceleration, mechanical resistance and cooling
according to FANUC servo troubleshooting.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL** https://pdfcoffee.com/fanuc-alarm-pdf-pdf-free.html

------------------------------------------------------------------------

### Record 19: FANUC --- Alarm OT0500

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** OT0500
-   **Alarm message:** + OVERTRAVEL (SOFT 1)
-   **Affected component:** Axis travel / software limit
-   **Severity:** Not specified in the available source record.

**Documented description** The positive-side stored-stroke check 1 was
exceeded.

**Documented possible causes** Commanded or actual axis position
exceeded the positive stored-stroke-check-1 limit.

**Documented corrective action / troubleshooting direction** Move the
axis back within the permitted travel using the machine's approved
recovery procedure; check stored-stroke parameters and machine
configuration before resuming.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://www.drivesul.com.br/template/imagens/manuais/manuais-fanuc/fanuc-series-0i-model-d/B-64305EN03%20-Series%200i-Model%20D%20-Maintenance%20Manual.pdf

------------------------------------------------------------------------

### Record 20: FANUC --- Alarm OT0501

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** OT0501
-   **Alarm message:** - OVERTRAVEL (SOFT 1)
-   **Affected component:** Axis travel / software limit
-   **Severity:** Not specified in the available source record.

**Documented description** The negative-side stored-stroke check 1 was
exceeded.

**Documented possible causes** Commanded or actual axis position
exceeded the negative stored-stroke-check-1 limit.

**Documented corrective action / troubleshooting direction** Move the
axis back within the permitted travel using the machine's approved
recovery procedure; check stored-stroke parameters and machine
configuration before resuming.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://www.drivesul.com.br/template/imagens/manuais/manuais-fanuc/fanuc-series-0i-model-d/B-64305EN03%20-Series%200i-Model%20D%20-Maintenance%20Manual.pdf

------------------------------------------------------------------------

### Record 21: FANUC --- Alarm OT0502

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** OT0502
-   **Alarm message:** + OVERTRAVEL (SOFT 2)
-   **Affected component:** Axis travel / software limit / barrier
-   **Severity:** Not specified in the available source record.

**Documented description** The positive-side stored-stroke check 2 was
exceeded; the manual also describes a positive-direction entry into an
inhibited area for applicable chuck/tailstock barrier configurations.

**Documented possible causes** Positive stored-stroke-check-2 violation
or applicable barrier violation.

**Documented corrective action / troubleshooting direction** Use the
machine's approved recovery procedure to return inside the permitted
area and verify stored-stroke/barrier settings.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://www.drivesul.com.br/template/imagens/manuais/manuais-fanuc/fanuc-series-0i-model-d/B-64305EN03%20-Series%200i-Model%20D%20-Maintenance%20Manual.pdf

------------------------------------------------------------------------

### Record 22: FANUC --- Alarm OT0503

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** OT0503
-   **Alarm message:** - OVERTRAVEL (SOFT 2)
-   **Affected component:** Axis travel / software limit / barrier
-   **Severity:** Not specified in the available source record.

**Documented description** The negative-side stored-stroke check 2 was
exceeded; the manual also describes a negative-direction entry into an
inhibited area for applicable chuck/tailstock barrier configurations.

**Documented possible causes** Negative stored-stroke-check-2 violation
or applicable barrier violation.

**Documented corrective action / troubleshooting direction** Use the
machine's approved recovery procedure to return inside the permitted
area and verify stored-stroke/barrier settings.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://www.drivesul.com.br/template/imagens/manuais/manuais-fanuc/fanuc-series-0i-model-d/B-64305EN03%20-Series%200i-Model%20D%20-Maintenance%20Manual.pdf

------------------------------------------------------------------------

### Record 23: FANUC --- Alarm OT0504

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** OT0504
-   **Alarm message:** + OVERTRAVEL (SOFT 3)
-   **Affected component:** Axis travel / software limit
-   **Severity:** Not specified in the available source record.

**Documented description** The positive-side stored-stroke check 3 was
exceeded.

**Documented possible causes** Positive stored-stroke-check-3 violation.

**Documented corrective action / troubleshooting direction** Use the
machine's approved recovery procedure and verify the relevant
stored-stroke settings.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://www.drivesul.com.br/template/imagens/manuais/manuais-fanuc/fanuc-series-0i-model-d/B-64305EN03%20-Series%200i%20-Model%20D%20-Maintenance%20Manual.pdf

------------------------------------------------------------------------

### Record 24: FANUC --- Alarm OT0505

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** OT0505
-   **Alarm message:** - OVERTRAVEL (SOFT 3)
-   **Affected component:** Axis travel / software limit
-   **Severity:** Not specified in the available source record.

**Documented description** The negative-side stored-stroke check 3 was
exceeded.

**Documented possible causes** Negative stored-stroke-check-3 violation.

**Documented corrective action / troubleshooting direction** Use the
machine's approved recovery procedure and verify the relevant
stored-stroke settings.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://www.drivesul.com.br/template/imagens/manuais/manuais-fanuc/fanuc-series-0i-model-d/B-64305EN03%20-Series%200i%20-Model%20D%20-Maintenance%20Manual.pdf

------------------------------------------------------------------------

### Record 25: FANUC --- Alarm OT0506

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** OT0506
-   **Alarm message:** + OVERTRAVEL (HARD)
-   **Affected component:** Axis travel / limit switch
-   **Severity:** Not specified in the available source record.

**Documented description** The positive-direction stroke-limit switch
was triggered; the manual states this alarm is generated when the
machine reaches the stroke end.

**Documented possible causes** Physical positive travel limit reached.

**Documented corrective action / troubleshooting direction** Follow the
machine-specific overtravel recovery procedure; do not bypass the safety
limit. Inspect the cause of the excessive travel before returning to
production.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://www.drivesul.com.br/template/imagens/manuais/manuais-fanuc/fanuc-series-0i-model-d/B-64305EN03%20-Series%200i%20-Model%20D%20-Maintenance%20Manual.pdf

------------------------------------------------------------------------

### Record 26: FANUC --- Alarm SP1975

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SP1975
-   **Alarm message:** ANALOG SPINDLE CONTROL ERROR
-   **Affected component:** Spindle position coder
-   **Severity:** Not specified in the available source record.

**Documented description** A position-coder error was detected on the
analog spindle.

**Documented possible causes** Analog-spindle position-coder error.

**Documented corrective action / troubleshooting direction** Inspect the
analog spindle position coder and associated wiring/connections
according to the FANUC spindle maintenance procedure.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://manuals.plus/m/a72521220f3a20e1cb0207a43607552fd815cce25b3d4085bd6123a5785d5f96.pdf

------------------------------------------------------------------------

### Record 27: FANUC --- Alarm SP1981

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SP1981
-   **Alarm message:** SERIAL SPINDLE AMP. ERROR
-   **Affected component:** Spindle amplifier
-   **Severity:** Not specified in the available source record.

**Documented description** An error occurred while reading data from the
SIC-LSI on the analog spindle amplifier side.

**Documented possible causes** Spindle-amplifier/SIC-LSI data-read
error.

**Documented corrective action / troubleshooting direction** Inspect the
spindle amplifier and associated spindle-control circuitry according to
the FANUC maintenance manual.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://manuals.plus/m/a72521220f3a20e1cb0207a43607552fd815cce25b3d4085bd6123a5785d5f96.pdf

------------------------------------------------------------------------

### Record 28: FANUC --- Alarm SP9132

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SP9132
-   **Alarm message:** SERIAL SPINDLE ALARM
-   **Affected component:** Spindle sensor / serial spindle
-   **Severity:** Not specified in the available source record.

**Documented description** A serial-spindle data error is detected.

**Documented possible causes** Serial-spindle sensor/data error.

**Documented corrective action / troubleshooting direction** The
referenced FANUC alarm list specifies replacing the sensor for this
amplifier indication; verify the exact spindle amplifier and machine
configuration before replacement.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://manuals.plus/m/a72521220f3a20e1cb0207a43607552fd815cce25b3d4085bd6123a5785d5f96.pdf

------------------------------------------------------------------------

### Record 29: FANUC --- Alarm SP9133

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SP9133
-   **Alarm message:** SERIAL SPINDLE ALARM
-   **Affected component:** Spindle sensor / serial spindle
-   **Severity:** Not specified in the available source record.

**Documented description** A serial-spindle data-transfer error is
detected.

**Documented possible causes** Serial-spindle data transfer error.

**Documented corrective action / troubleshooting direction** The
referenced FANUC alarm list specifies replacing the sensor for this
amplifier indication; verify the exact spindle amplifier and machine
configuration before replacement.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://manuals.plus/m/a72521220f3a20e1cb0207a43607552fd815cce25b3d4085bd6123a5785d5f96.pdf

------------------------------------------------------------------------

### Record 30: FANUC --- Alarm SP9134

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SP9134
-   **Alarm message:** SERIAL SPINDLE ALARM
-   **Affected component:** Spindle sensor / serial spindle
-   **Severity:** Not specified in the available source record.

**Documented description** A soft-phase error is detected in the
serial-spindle system.

**Documented possible causes** Incorrect sensor parameter setting;
electrical noise; sensor fault.

**Documented corrective action / troubleshooting direction** Check and
correct sensor parameter settings; take action against noise; replace
the sensor if required, as specified in the FANUC alarm list.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://manuals.plus/m/a72521220f3a20e1cb0207a43607552fd815cce25b3d4085bd6123a5785d5f96.pdf

------------------------------------------------------------------------

### Record 31: FANUC --- Alarm SP9135

-   **Brand:** FANUC
-   **Machine type:** CNC Milling / Machining Center
-   **Controller scope:** Series 0i-D / 0i Mate-D
-   **Alarm code:** SP9135
-   **Alarm message:** SAFETY SPEED ZERO ERROR(SP)
-   **Affected component:** Spindle / safety-speed monitoring
-   **Severity:** Not specified in the available source record.

**Documented description** The motor position exceeded the
safety-speed-zero monitoring width.

**Documented possible causes** Motor position outside the
safety-speed-zero monitoring range.

**Documented corrective action / troubleshooting direction** Perform
operation within the safety-speed-zero range, as specified by the FANUC
alarm list and applicable machine procedure.

**Source document** B-64305EN/03 Appendix A - Alarm List

**Source URL**
https://manuals.plus/m/a72521220f3a20e1cb0207a43607552fd815cce25b3d4085bd6123a5785d5f96.pdf

------------------------------------------------------------------------

### Record 32: HAAS --- Alarm 107

-   **Brand:** HAAS
-   **Machine type:** CNC Milling
-   **Controller scope:** Haas Mill control (CHC/NGC where applicable)
-   **Alarm code:** 107
-   **Alarm message:** EMERGENCY STOP
-   **Affected component:** Emergency-stop circuit
-   **Severity:** Machine operation inhibited

**Documented description** Emergency-stop condition is active. On Haas
Desktop Mill troubleshooting, the alarm may fail to reset when the
primary E-stop cable is disconnected or damaged.

**Documented possible causes** Primary E-stop cable disconnected; E-stop
cable damaged; E-stop-related connection/port problem.

**Documented corrective action / troubleshooting direction** Check the
E-stop cable and its connection. If the cable is undamaged, reconnect it
and cycle machine power; if damaged, replace it and power cycle. Follow
the applicable Haas service procedure.

**Source document** Haas Desktop Mill Troubleshooting Guide TG0058; Haas
Alarm Search Help RD0002

**Source URL**
https://www.haascnc.com/service/troubleshooting-and-how-to/troubleshooting/desktop-mill---troubleshooting-guide.html

**Supplementary training example (not a substitute for the source
manual)** - Instruction: Explain Haas CNC milling alarm 107 (EMERGENCY
STOP). Give the official description, documented possible causes, and
official troubleshooting direction. Do not invent causes. - Input:
Brand: Haas; Machine type: CNC Milling; Controller scope: Haas Mill
control (CHC/NGC where applicable); Alarm code: 107 - Output: Alarm:
107 - EMERGENCY STOP. Description: Emergency-stop condition is active.
On Haas Desktop Mill troubleshooting, the alarm may fail to reset when
the primary E-stop cable is disconnected or damaged. Possible causes:
Primary E-stop cable disconnected; E-stop cable damaged; E-stop-related
connection/port problem. Official corrective/troubleshooting direction:
Check the E-stop cable and its connection. If the cable is undamaged,
reconnect it and cycle machine power; if damaged, replace it and power
cycle. Follow the applicable Haas service procedure.

------------------------------------------------------------------------

### Record 33: HAAS --- Alarm 120

-   **Brand:** HAAS
-   **Machine type:** CNC Milling
-   **Controller scope:** Haas Mill control
-   **Alarm code:** 120
-   **Alarm message:** LOW AIR PRESSURE OR FLOW
-   **Affected component:** Pneumatic air supply / pressure sensor
-   **Severity:** Machine operation may be inhibited

**Documented description** The compressed air supplied to the machine is
below the minimum pressure or flow required.

**Documented possible causes** Insufficient compressed-air pressure or
flow; contamination affecting the air-pressure sensor.

**Documented corrective action / troubleshooting direction** Check the
air supply and pressure. Check the air-pressure sensor for
contamination; replace the sensor if required. Haas states that the air
supply should be clean and dry.

**Source document** Haas NGC Sensors and Switches Service Manual

**Source URL**
https://www.haascnc.com/service/online-manuals/next-gen-control-electrical---service-manual/ngc---sensors-and-switches.html

**Supplementary training example (not a substitute for the source
manual)** - Instruction: Explain Haas CNC milling alarm 120 (LOW AIR
PRESSURE OR FLOW). Give the official description, documented possible
causes, and official troubleshooting direction. Do not invent causes. -
Input: Brand: Haas; Machine type: CNC Milling; Controller scope: Haas
Mill control; Alarm code: 120 - Output: Alarm: 120 - LOW AIR PRESSURE OR
FLOW. Description: The compressed air supplied to the machine is below
the minimum pressure or flow required. Possible causes: Insufficient
compressed-air pressure or flow; contamination affecting the
air-pressure sensor. Official corrective/troubleshooting direction:
Check the air supply and pressure. Check the air-pressure sensor for
contamination; replace the sensor if required. Haas states that the air
supply should be clean and dry.

------------------------------------------------------------------------

### Record 34: HAAS --- Alarm 123

-   **Brand:** HAAS
-   **Machine type:** CNC Milling
-   **Controller scope:** Haas Mill control
-   **Alarm code:** 123
-   **Alarm message:** SPINDLE DRIVE FAULT
-   **Affected component:** Spindle drive / spindle power system
-   **Severity:** Spindle operation affected

**Documented description** The spindle drive has reported a fault. Haas
directs the technician to inspect the spindle-drive error code for the
specific cause.

**Documented possible causes** Multiple possible spindle-drive faults;
DC-bus problem; vector-drive short circuit; drive or motor/cable fault
depending on the machine/control configuration.

**Documented corrective action / troubleshooting direction** Read the
error code shown on the spindle drive and follow the applicable Haas
spindle-drive troubleshooting procedure. Do not assume a single root
cause from alarm 123 alone.

**Source document** Haas Spindle Drive Troubleshooting Guide TG0133;
Haas Vector Drive Troubleshooting Guides

**Source URL**
https://www.haascnc.com/service/troubleshooting-and-how-to/troubleshooting/spindle-drive---how-it-works-and-troubleshooting-guide.html

**Supplementary training example (not a substitute for the source
manual)** - Instruction: Explain Haas CNC milling alarm 123 (SPINDLE
DRIVE FAULT). Give the official description, documented possible causes,
and official troubleshooting direction. Do not invent causes. - Input:
Brand: Haas; Machine type: CNC Milling; Controller scope: Haas Mill
control; Alarm code: 123 - Output: Alarm: 123 - SPINDLE DRIVE FAULT.
Description: The spindle drive has reported a fault. Haas directs the
technician to inspect the spindle-drive error code for the specific
cause. Possible causes: Multiple possible spindle-drive faults; DC-bus
problem; vector-drive short circuit; drive or motor/cable fault
depending on the machine/control configuration. Official
corrective/troubleshooting direction: Read the error code shown on the
spindle drive and follow the applicable Haas spindle-drive
troubleshooting procedure. Do not assume a single root cause from alarm
123 alone.

------------------------------------------------------------------------

### Record 35: HAAS --- Alarm 149

-   **Brand:** HAAS
-   **Machine type:** CNC Milling
-   **Controller scope:** Haas Mill control
-   **Alarm code:** 149
-   **Alarm message:** SPINDLE TURNING
-   **Affected component:** Spindle / tool changer interface
-   **Severity:** Tool-change operation affected

**Documented description** The spindle speed is not at zero during a
tool change.

**Documented possible causes** Spindle has not stopped before the
tool-change operation.

**Documented corrective action / troubleshooting direction** Use the
Haas diagnostic data and applicable spindle/tool-change troubleshooting
procedure to identify why the spindle has not reached zero speed.

**Source document** Haas Spindle Drive Troubleshooting Guide TG0133

**Source URL**
https://www.haascnc.com/service/troubleshooting-and-how-to/troubleshooting/spindle-drive---how-it-works-and-troubleshooting-guide.html

**Supplementary training example (not a substitute for the source
manual)** - Instruction: Explain Haas CNC milling alarm 149 (SPINDLE
TURNING). Give the official description, documented possible causes, and
official troubleshooting direction. Do not invent causes. - Input:
Brand: Haas; Machine type: CNC Milling; Controller scope: Haas Mill
control; Alarm code: 149 - Output: Alarm: 149 - SPINDLE TURNING.
Description: The spindle speed is not at zero during a tool change.
Possible causes: Spindle has not stopped before the tool-change
operation. Official corrective/troubleshooting direction: Use the Haas
diagnostic data and applicable spindle/tool-change troubleshooting
procedure to identify why the spindle has not reached zero speed.

------------------------------------------------------------------------

### Record 36: HAAS --- Alarm 186

-   **Brand:** HAAS
-   **Machine type:** CNC Milling
-   **Controller scope:** Haas Mill control
-   **Alarm code:** 186
-   **Alarm message:** SPINDLE NOT TURNING
-   **Affected component:** Spindle system
-   **Severity:** Spindle operation affected

**Documented description** The spindle does not turn when commanded to.

**Documented possible causes** The spindle is not responding to the
commanded rotation; the underlying drive, motor, control signal, or
mechanical condition must be diagnosed.

**Documented corrective action / troubleshooting direction** Use the
Haas spindle troubleshooting procedure and diagnostic data to identify
why the spindle does not turn. Do not treat the alarm alone as proof of
a specific failed component.

**Source document** Haas Spindle Drive Troubleshooting Guide TG0133

**Source URL**
https://www.haascnc.com/service/troubleshooting-and-how-to/troubleshooting/spindle-drive---how-it-works-and-troubleshooting-guide.html

**Supplementary training example (not a substitute for the source
manual)** - Instruction: Explain Haas CNC milling alarm 186 (SPINDLE NOT
TURNING). Give the official description, documented possible causes, and
official troubleshooting direction. Do not invent causes. - Input:
Brand: Haas; Machine type: CNC Milling; Controller scope: Haas Mill
control; Alarm code: 186 - Output: Alarm: 186 - SPINDLE NOT TURNING.
Description: The spindle does not turn when commanded to. Possible
causes: The spindle is not responding to the commanded rotation; the
underlying drive, motor, control signal, or mechanical condition must be
diagnosed. Official corrective/troubleshooting direction: Use the Haas
spindle troubleshooting procedure and diagnostic data to identify why
the spindle does not turn. Do not treat the alarm alone as proof of a
specific failed component.

------------------------------------------------------------------------

### Record 37: HAAS --- Alarm 236

-   **Brand:** HAAS
-   **Machine type:** CNC Milling
-   **Controller scope:** Haas Mill control
-   **Alarm code:** 236
-   **Alarm message:** SPINDLE MOTOR OVERLOAD
-   **Affected component:** Spindle motor / drive system
-   **Severity:** Spindle operation affected

**Documented description** The spindle motor has entered an overload
condition.

**Documented possible causes** Internal short circuit; failed
temperature sensor; over-aggressive application; shorted vector drive;
failed vector-drive fans; incorrect or loose cable connection; shorted
spindle motor cable; burnt or shorted Wye/Delta contacts; worn or
damaged spindle encoder belt.

**Documented corrective action / troubleshooting direction** Follow the
Haas spindle-motor troubleshooting procedure for the applicable machine.
Inspect/test the spindle motor, overheat sensor, vector drive, fans,
cables, Wye/Delta contacts and encoder belt as applicable.

**Source document** Haas 30T/40T Spindle Motor Troubleshooting Guide
TG0009

**Source URL**
https://www.haascnc.com/service/troubleshooting-and-how-to/troubleshooting/spindle-motor---troubleshooting-guide.html

**Supplementary training example (not a substitute for the source
manual)** - Instruction: Explain Haas CNC milling alarm 236 (SPINDLE
MOTOR OVERLOAD). Give the official description, documented possible
causes, and official troubleshooting direction. Do not invent causes. -
Input: Brand: Haas; Machine type: CNC Milling; Controller scope: Haas
Mill control; Alarm code: 236 - Output: Alarm: 236 - SPINDLE MOTOR
OVERLOAD. Description: The spindle motor has entered an overload
condition. Possible causes: Internal short circuit; failed temperature
sensor; over-aggressive application; shorted vector drive; failed
vector-drive fans; incorrect or loose cable connection; shorted spindle
motor cable; burnt or shorted Wye/Delta contacts; worn or damaged
spindle encoder belt. Official corrective/troubleshooting direction:
Follow the Haas spindle-motor troubleshooting procedure for the
applicable machine. Inspect/test the spindle motor, overheat sensor,
vector drive, fans, cables, Wye/Delta contacts and encoder belt as
applicable.

------------------------------------------------------------------------

### Record 38: HAAS --- Alarm 254

-   **Brand:** HAAS
-   **Machine type:** CNC Milling
-   **Controller scope:** Haas Mill control
-   **Alarm code:** 254
-   **Alarm message:** SPINDLE MOTOR OVERHEAT
-   **Affected component:** Spindle motor / cooling / temperature
    sensing
-   **Severity:** Spindle operation affected

**Documented description** The spindle motor has reached an overheat
condition.

**Documented possible causes** Over-aggressive application; failed
spindle fan; spindle-motor temperature-sensor problem.

**Documented corrective action / troubleshooting direction** Adjust the
machining program/application as appropriate. Check the spindle fan and
cable. Inspect the spindle-motor temperature sensor and its
cable/connection according to the Haas procedure.

**Source document** Haas 30T/40T Spindle Motor Troubleshooting Guide
TG0009

**Source URL**
https://www.haascnc.com/service/troubleshooting-and-how-to/troubleshooting/spindle-motor---troubleshooting-guide.html

**Supplementary training example (not a substitute for the source
manual)** - Instruction: Explain Haas CNC milling alarm 254 (SPINDLE
MOTOR OVERHEAT). Give the official description, documented possible
causes, and official troubleshooting direction. Do not invent causes. -
Input: Brand: Haas; Machine type: CNC Milling; Controller scope: Haas
Mill control; Alarm code: 254 - Output: Alarm: 254 - SPINDLE MOTOR
OVERHEAT. Description: The spindle motor has reached an overheat
condition. Possible causes: Over-aggressive application; failed spindle
fan; spindle-motor temperature-sensor problem. Official
corrective/troubleshooting direction: Adjust the machining
program/application as appropriate. Check the spindle fan and cable.
Inspect the spindle-motor temperature sensor and its cable/connection
according to the Haas procedure.

------------------------------------------------------------------------

### Record 39: HAAS --- Alarm 253

-   **Brand:** HAAS
-   **Machine type:** CNC Milling
-   **Controller scope:** Haas Mill control
-   **Alarm code:** 253
-   **Alarm message:** ELECTRONICS OVERHEAT
-   **Affected component:** Control electronics / cabinet cooling
-   **Severity:** Machine operation inhibited while alarm persists

**Documented description** The control has detected an electronics
overheat condition that remains long enough to generate the alarm.

**Documented possible causes** Control-cabinet temperature too high;
clogged air filters; cooling fans not operating correctly.

**Documented corrective action / troubleshooting direction** Inspect the
control cabinet for clogged air filters and correctly operating fans.
Follow the applicable Haas electrical/service procedure.

**Source document** Haas Mill Next Generation Control Icon Guide RD0046

**Source URL**
https://www.haascnc.com/service/troubleshooting-and-how-to/reference-documents/mill---next-generation-control-icon-guide.html

**Supplementary training example (not a substitute for the source
manual)** - Instruction: Explain Haas CNC milling alarm 253 (ELECTRONICS
OVERHEAT). Give the official description, documented possible causes,
and official troubleshooting direction. Do not invent causes. - Input:
Brand: Haas; Machine type: CNC Milling; Controller scope: Haas Mill
control; Alarm code: 253 - Output: Alarm: 253 - ELECTRONICS OVERHEAT.
Description: The control has detected an electronics overheat condition
that remains long enough to generate the alarm. Possible causes:
Control-cabinet temperature too high; clogged air filters; cooling fans
not operating correctly. Official corrective/troubleshooting direction:
Inspect the control cabinet for clogged air filters and correctly
operating fans. Follow the applicable Haas electrical/service procedure.

------------------------------------------------------------------------

### Record 40: HAAS --- Alarm 160

-   **Brand:** HAAS
-   **Machine type:** CNC Milling
-   **Controller scope:** Haas Mill control
-   **Alarm code:** 160
-   **Alarm message:** LOW INCOMING AC LINE VOLTAGE
-   **Affected component:** Incoming electrical power / DC bus
-   **Severity:** Electrical power fault

**Documented description** The incoming AC line voltage is below the
required operating level.

**Documented possible causes** Low incoming line voltage; DC-bus or
power-supply condition may also be involved when this alarm occurs with
related power alarms.

**Documented corrective action / troubleshooting direction**
Measure/compare the incoming and DC-bus voltage using the applicable
Haas diagnostic procedure and inspect the power-supply/DC-bus system.

**Source document** Haas 320V Power Supply Troubleshooting Guide; Haas
Vector Drive Troubleshooting Guide

**Source URL**
https://www.haascnc.com/service/troubleshooting-and-how-to/troubleshooting/320v-power-supply--mmps----troubleshooting-guide---ngc.html

**Supplementary training example (not a substitute for the source
manual)** - Instruction: Explain Haas CNC milling alarm 160 (LOW
INCOMING AC LINE VOLTAGE). Give the official description, documented
possible causes, and official troubleshooting direction. Do not invent
causes. - Input: Brand: Haas; Machine type: CNC Milling; Controller
scope: Haas Mill control; Alarm code: 160 - Output: Alarm: 160 - LOW
INCOMING AC LINE VOLTAGE. Description: The incoming AC line voltage is
below the required operating level. Possible causes: Low incoming line
voltage; DC-bus or power-supply condition may also be involved when this
alarm occurs with related power alarms. Official
corrective/troubleshooting direction: Measure/compare the incoming and
DC-bus voltage using the applicable Haas diagnostic procedure and
inspect the power-supply/DC-bus system.

------------------------------------------------------------------------

### Record 41: HAAS --- Alarm 647

-   **Brand:** HAAS
-   **Machine type:** CNC Milling
-   **Controller scope:** Haas Mill control
-   **Alarm code:** 647
-   **Alarm message:** REGEN LOAD SHORTED
-   **Affected component:** REGEN load / power supply
-   **Severity:** Electrical fault

**Documented description** The REGEN load or associated power-supply
system is reporting a short-circuit condition.

**Documented possible causes** Problem with the REGEN load; shorted
MMPS/power-supply condition.

**Documented corrective action / troubleshooting direction** Measure
resistance across the REGEN load and inspect the MMPS/power-supply
system using the Haas procedure.

**Source document** Haas 320V Power Supply Troubleshooting Guide

**Source URL**
https://www.haascnc.com/service/troubleshooting-and-how-to/troubleshooting/320v-power-supply--mmps----troubleshooting-guide---ngc.html

**Supplementary training example (not a substitute for the source
manual)** - Instruction: Explain Haas CNC milling alarm 647 (REGEN LOAD
SHORTED). Give the official description, documented possible causes, and
official troubleshooting direction. Do not invent causes. - Input:
Brand: Haas; Machine type: CNC Milling; Controller scope: Haas Mill
control; Alarm code: 647 - Output: Alarm: 647 - REGEN LOAD SHORTED.
Description: The REGEN load or associated power-supply system is
reporting a short-circuit condition. Possible causes: Problem with the
REGEN load; shorted MMPS/power-supply condition. Official
corrective/troubleshooting direction: Measure resistance across the
REGEN load and inspect the MMPS/power-supply system using the Haas
procedure.

------------------------------------------------------------------------

### Record 42: HAAS --- Alarm 648

-   **Brand:** HAAS
-   **Machine type:** CNC Milling
-   **Controller scope:** Haas Mill control
-   **Alarm code:** 648
-   **Alarm message:** DC BUS SHORTED
-   **Affected component:** DC bus / power supply
-   **Severity:** Electrical fault

**Documented description** The DC bus or associated power-supply system
is reporting a short-circuit condition.

**Documented possible causes** Problem with the DC bus;
MMPS/power-supply short circuit.

**Documented corrective action / troubleshooting direction** Compare the
measured DC voltage with the diagnostic page and inspect the MMPS for
short circuits using the Haas service procedure.

**Source document** Haas 320V Power Supply Troubleshooting Guide

**Source URL**
https://www.haascnc.com/service/troubleshooting-and-how-to/troubleshooting/320v-power-supply--mmps----troubleshooting-guide---ngc.html

**Supplementary training example (not a substitute for the source
manual)** - Instruction: Explain Haas CNC milling alarm 648 (DC BUS
SHORTED). Give the official description, documented possible causes, and
official troubleshooting direction. Do not invent causes. - Input:
Brand: Haas; Machine type: CNC Milling; Controller scope: Haas Mill
control; Alarm code: 648 - Output: Alarm: 648 - DC BUS SHORTED.
Description: The DC bus or associated power-supply system is reporting a
short-circuit condition. Possible causes: Problem with the DC bus;
MMPS/power-supply short circuit. Official corrective/troubleshooting
direction: Compare the measured DC voltage with the diagnostic page and
inspect the MMPS for short circuits using the Haas service procedure.

------------------------------------------------------------------------

### Record 43: HAAS --- Alarm 119

-   **Brand:** HAAS
-   **Machine type:** CNC Milling
-   **Controller scope:** Haas Mill control
-   **Alarm code:** 119
-   **Alarm message:** INPUT AC LINE OVERVOLTAGE
-   **Affected component:** Incoming electrical power / DC bus / REGEN
-   **Severity:** Electrical fault

**Documented description** The incoming AC line voltage is too high.

**Documented possible causes** Incoming electrical supply overvoltage;
related REGEN/DC-bus fault may also be present.

**Documented corrective action / troubleshooting direction** Measure
incoming voltage and inspect the REGEN/DC-bus system when related alarms
occur, following the applicable Haas power-supply troubleshooting
procedure.

**Source document** Haas 320V Power Supply Troubleshooting Guide; REGEN
Troubleshooting Guide

**Source URL**
https://www.haascnc.com/service/troubleshooting-and-how-to/troubleshooting/320v-power-supply--mmps----troubleshooting-guide---ngc.html

**Supplementary training example (not a substitute for the source
manual)** - Instruction: Explain Haas CNC milling alarm 119 (INPUT AC
LINE OVERVOLTAGE). Give the official description, documented possible
causes, and official troubleshooting direction. Do not invent causes. -
Input: Brand: Haas; Machine type: CNC Milling; Controller scope: Haas
Mill control; Alarm code: 119 - Output: Alarm: 119 - INPUT AC LINE
OVERVOLTAGE. Description: The incoming AC line voltage is too high.
Possible causes: Incoming electrical supply overvoltage; related
REGEN/DC-bus fault may also be present. Official
corrective/troubleshooting direction: Measure incoming voltage and
inspect the REGEN/DC-bus system when related alarms occur, following the
applicable Haas power-supply troubleshooting procedure.

------------------------------------------------------------------------

### Record 44: HAAS --- Alarm 650

-   **Brand:** HAAS
-   **Machine type:** CNC Milling
-   **Controller scope:** Haas Mill control
-   **Alarm code:** 650
-   **Alarm message:** DC BUS OVER VOLTAGE
-   **Affected component:** DC bus / REGEN / power supply
-   **Severity:** Electrical fault

**Documented description** The DC bus voltage is above the allowable
operating condition.

**Documented possible causes** Problem with the REGEN load; faulty
power-supply/MMPS condition.

**Documented corrective action / troubleshooting direction** Measure the
resistance across the REGEN load and inspect the power-supply/MMPS
system according to the Haas procedure.

**Source document** Haas REGEN and 320V Power Supply Troubleshooting
Guides

**Source URL**
https://www.haascnc.com/service/troubleshooting-and-how-to/troubleshooting/regen---troubleshooting-guide.html

**Supplementary training example (not a substitute for the source
manual)** - Instruction: Explain Haas CNC milling alarm 650 (DC BUS OVER
VOLTAGE). Give the official description, documented possible causes, and
official troubleshooting direction. Do not invent causes. - Input:
Brand: Haas; Machine type: CNC Milling; Controller scope: Haas Mill
control; Alarm code: 650 - Output: Alarm: 650 - DC BUS OVER VOLTAGE.
Description: The DC bus voltage is above the allowable operating
condition. Possible causes: Problem with the REGEN load; faulty
power-supply/MMPS condition. Official corrective/troubleshooting
direction: Measure the resistance across the REGEN load and inspect the
power-supply/MMPS system according to the Haas procedure.

------------------------------------------------------------------------

### Record 45: HAAS --- Alarm 1.9930

-   **Brand:** HAAS
-   **Machine type:** CNC Milling
-   **Controller scope:** Haas Mill control
-   **Alarm code:** 1.9930
-   **Alarm message:** X SERIAL ENCODER COMMUNICATION FAULT
-   **Affected component:** X-axis serial encoder / feedback system
-   **Severity:** Axis operation affected

**Documented description** An X-axis serial encoder communication fault
has been detected. Haas uses the digits before the decimal point to
identify the axis in this alarm format.

**Documented possible causes** Encoder communication problem in the
X-axis feedback system; exact root cause requires the applicable Haas
axis/encoder troubleshooting procedure.

**Documented corrective action / troubleshooting direction** Use the
Haas alarm/axis troubleshooting documentation to diagnose the X-axis
serial encoder communication path. Do not infer a failed encoder solely
from the alarm number.

**Source document** Haas Alarm Search Help Guide RD0002

**Source URL**
https://www.haascnc.com/service/troubleshooting-and-how-to/reference-documents/alarm-search-help.html

**Supplementary training example (not a substitute for the source
manual)** - Instruction: Explain Haas CNC milling alarm 1.9930 (X SERIAL
ENCODER COMMUNICATION FAULT). Give the official description, documented
possible causes, and official troubleshooting direction. Do not invent
causes. - Input: Brand: Haas; Machine type: CNC Milling; Controller
scope: Haas Mill control; Alarm code: 1.9930 - Output: Alarm: 1.9930 - X
SERIAL ENCODER COMMUNICATION FAULT. Description: An X-axis serial
encoder communication fault has been detected. Haas uses the digits
before the decimal point to identify the axis in this alarm format.
Possible causes: Encoder communication problem in the X-axis feedback
system; exact root cause requires the applicable Haas axis/encoder
troubleshooting procedure. Official corrective/troubleshooting
direction: Use the Haas alarm/axis troubleshooting documentation to
diagnose the X-axis serial encoder communication path. Do not infer a
failed encoder solely from the alarm number.

------------------------------------------------------------------------
