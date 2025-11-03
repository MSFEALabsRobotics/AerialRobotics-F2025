# Mission Planner Pre‑Flight Setup (Holybro Quad, ArduCopter)

A printable checklist to run in Mission Planner before first take‑off.

---

## 0) Safety
- [ ] **Props OFF** for all calibrations and motor tests.
- [ ] Battery secured; no loose cables; frame rigid.

---

## 1) Frame & Firmware
- [ ] Connect via USB → **Load ArduCopter** (if needed) → **Connect**.
- [ ] **Configuration → Frame Type**
  - [ ] `FRAME_CLASS = Quad`
  - [ ] `FRAME_TYPE = X` (X direction)
- [ ] Write params / reboot if prompted.

---

## 2) Accelerometer (Level & 6‑Point)
- [ ] **Mandatory Hardware → Accel Calibration**
  - [ ] Click **Calibrate Level** (airframe sitting level).
  - [ ] Click **Calibrate Accelerometer** and place in each orientation until accepted:
    - [ ] Level (straight)
    - [ ] Left side
    - [ ] Right side
    - [ ] Nose down
    - [ ] Nose up
    - [ ] Upside down (on the back, 180°)
- [ ] Confirm success.

---

## 3) Compass
- [ ] **Mandatory Hardware → Compass**
  - [ ] Go **outdoors** for calibration (compass is in the GPS puck).
  - [ ] Perform **Live Calibration**.
  - [ ] **Untick Compass #3** if present/noisy.
  - [ ] Write params.

---

## 4) Radio (RC) Calibration & Throttle Failsafe
- [ ] **Mandatory Hardware → Radio Calibration**
  - [ ] Click **Calibrate Radio**; move **all sticks/switches** through full range.
  - [ ] Click **Done** when bars look correct.
- [ ] **Receiver throttle failsafe** (at RX):
  - [ ] Set throttle output on signal loss to **low PWM (~960 µs)**.
- [ ] **Full Parameter List**:
  - [ ] `FS_THR_ENABLE = 1` (Enabled always)
  - [ ] Verify `RC3_MIN / RC3_MAX` look correct.
  - [ ] Save.

---

## 5) Servo/Motor Outputs & Motor Test
- [ ] **Servo/Motor Output mapping** (quad):
  - [ ] `Channel 1 → Motor 1`
  - [ ] `Channel 2 → Motor 2`
  - [ ] `Channel 3 → Motor 3`
  - [ ] `Channel 4 → Motor 4`
- [ ] **Optional Hardware → Motor Test**
  - [ ] **Press & hold GPS/safety switch** until LED solid (safety off).
  - [ ] Test each motor briefly; verify **numbers & spin directions** match MP diagram (e.g., Motor 1 CCW as shown).
  - [ ] Stop test; safety back on.

---

## 6) Flight Modes & Mode Channel
- [ ] **Mandatory Hardware → Flight Modes**
  - [ ] Set `FLTMODE1 … FLTMODE6` as desired.
- [ ] **Full Parameter List**
  - [ ] `MODE_CH = 6` (use RC channel 6 for mode selection).
  - [ ] **Save** and **Reload** parameters.

---

## 7) Battery Monitor & Failsafe (4S example)
- [ ] **Optional Hardware → Battery Monitor**
  - [ ] **Monitor**: `INA2xx` (Holybro module)
  - [ ] **Sensor**: `Holybro`
  - [ ] `BATT_CAPACITY = 4000` mAh
  - [ ] Verify live voltage reads reasonably (e.g., **~15.19 V** on fresh 4S).
- [ ] **Failsafe thresholds** (adjust for your pack/chemistry):
  - [ ] **Low**: `BATT_FS_LOW_ACT = 2 (RTL)`; `BATT_LOW_VOLT = 14.4` V (≈ 4 × 3.6 V)
  - [ ] **Critical**: `BATT_FS_CRT_ACT = 1 (Land)`; `BATT_CRT_VOLT ≈ 14.0` V
  - [ ] Write params.
- [ ] **Test**: (Props off) Arm, then **turn off TX** to confirm **RTL** (or set action). Disarm immediately after confirming.

---

## 8) Initial Tuning
- [ ] Leave **Initial Tuning** parameters at **defaults** for first hover.
- [ ] Plan to run **Autotune** after a stable maiden hover.

---

## 9) SiK Telemetry Radios (433 MHz)
- [ ] **Optional Hardware → SiK Radio**
  - [ ] `NETID = 40`
  - [ ] **Max Frequency** = `434` MHz
  - [ ] **Save/Write**.
  - [ ] **Repeat the same settings on BOTH radios** (air & ground).

---

## 10) Optional: Servo Pass‑Through (e.g., gimbal/servo)
- [ ] **Servo Output** (example for output 8):
  - [ ] `SERVO8_FUNCTION = 1 (RCPassThru)`
  - [ ] Assign desired **RC channel** (knob/switch) in Radio setup.
  - [ ] Test movement with TX.

---

## 11) Final Pre‑Arm Checks
- [ ] Props correctly installed & tight (do **after** all tests).
- [ ] GPS fix (≥ 8 sats), EKF/compass healthy, home position set.
- [ ] Flight mode switch cycles 1→6 correctly.
- [ ] RTL altitude/action make sense for your field.
- [ ] Takeoff area clear; spotter briefed.

---

**Notes**  
- Your earlier voltage note: `4 × 3.6 V = 14.4 V` is a reasonable **low** threshold for 4S LiPo under light load; adjust per pack sag and mission profile.
- Always re‑verify motor numbering/direction after any ESC or wiring changes.
