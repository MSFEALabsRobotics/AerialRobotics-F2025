# SITL Control Tutorial with Python (pymavlink)

This tutorial shows how to connect to ArduPilot SITL (Software In The Loop) and control the drone using Python with **pymavlink**.

---

## 1. Importing & Connecting

```python
import time
from pymavlink import mavutil

# Connect to SITL
master = mavutil.mavlink_connection('udp:127.0.0.1:14550')
master.wait_heartbeat()
print(f"Connected: system {master.target_system}, component {master.target_component}")
```

---

## 2. Setting Guided Mode, Arming, Takeoff, Landing

```python
# ---- Set mode to GUIDED ----
mode = 'GUIDED'
mode_id = master.mode_mapping()[mode]
master.mav.set_mode_send(
    master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    mode_id
)
time.sleep(1)

# ---- Arm ----
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0, 1, 0, 0, 0, 0, 0, 0
)
print("Arming...")
time.sleep(2)

# ---- Takeoff ----
target_altitude = 5  # meters
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    0, 0, 0, 0, 0, 0, 0, target_altitude
)
print(f"Taking off to {target_altitude}m...")
time.sleep(8)  # wait until we climb
```

---

<img width="701" height="475" alt="image" src="https://github.com/user-attachments/assets/b72abae0-bcbf-468e-b5b2-bdd1a0ad8057" />


## 3. Controlling Drone with Velocity Commands (non-blocking)

```python
import time
import math
from pymavlink import mavutil

# ---- Connect to SITL ----
master = mavutil.mavlink_connection('udp:127.0.0.1:14550')
master.wait_heartbeat()
print(f"Connected: system {master.target_system}, component {master.target_component}")

# ---- Helper: send local waypoint + yaw ----
def goto_position_target_local_ned_with_yaw(x, y, z, yaw_deg):
    """
    Move vehicle to a target position (x,y,z) in LOCAL_NED frame
    and face a given yaw angle (absolute).
    NED frame:
      x → forward (north)
      y → right (east)
      z → down (positive down, negative up)
    yaw_deg → heading in degrees (0 = North, 90 = East, etc.)
    """
    yaw_rad = math.radians(yaw_deg)
    master.mav.set_position_target_local_ned_send(
        0,  # time_boot_ms
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111111000,  # position + yaw
        x, y, z,             # target position (meters)
        0, 0, 0,             # velocity (not used)
        0, 0, 0,             # acceleration (not used)
        yaw_rad, 0           # yaw (rad), yaw_rate
    )

#
# ---- Main Mission ----
if __name__ == "__main__":
#arm_and_takeoff(5)

    # Define waypoints (x, y, z, yaw_deg)
    waypoints = [
        (5, 0, -5,   90),   # forward 5m, face East
        (5, 5, -5, 180),   # right 5m, face South
        (0, 5, -5, -90),   # back 5m, face West
        (0, 0, -5,   0)    # return home, face North
    ]

    # Fly through waypoints with yaw
    for (x, y, z, yaw) in waypoints:
        print(f"Going to waypoint: x={x}, y={y}, z={z}, yaw={yaw}°")
        goto_position_target_local_ned_with_yaw(x, y, z, yaw)
        time.sleep(10)

    print("Mission complete!")

```


### Creating A loop for instant control per frequency

```python

  for _ in range(int(duration * 10)):  # send at 10 Hz
        master.mav.send(msg)
        time.sleep(0.1)


```
  
        
### Exercise: Keyboard Control

```python


print("Control Your Drone With Some Input Commands")

while True:
    key = input("Press a key: ").lower().strip()

    if key == "takeoff":
        print("Taking Off")
    elif key == "land":
        print("Landing")
    elif key == "esc":
        print("Exiting...")
        break
    else:
        print("Unknown key:", key)
```

---

## 4. Relative Position Commands (blocking)

```python
import math

def goto_position_target_local_ned_with_yaw(x, y, z, yaw_deg):
    """
    Move vehicle to a target position (x,y,z) in LOCAL_NED frame
    and face a given yaw angle (absolute).
    NED frame:
      x → forward (north)
      y → right (east)
      z → down (positive down, negative up)
    yaw_deg → heading in degrees (0 = North, 90 = East, etc.)
    """
    yaw_rad = math.radians(yaw_deg)
    master.mav.set_position_target_local_ned_send(
        0,
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111111000,  # position + yaw
        x, y, z,
        0, 0, 0,
        0, 0, 0,
        yaw_rad, 0
    )
```

---

## 5. Commanding Drone with Latitude/Longitude

```python
def goto_position_target_global_int(lat, lon, alt, yaw_deg=None):
    """
    Fly to GPS waypoint (lat, lon in degrees, alt in meters above home).
    Optionally set yaw (absolute heading in degrees).
    """
    yaw_rad = math.radians(yaw_deg) if yaw_deg is not None else 0.0

    master.mav.set_position_target_global_int_send(
        0,
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
        0b0000111111111000,  # position + yaw
        int(lat * 1e7),
        int(lon * 1e7),
        alt,
        0, 0, 0,
        0, 0, 0,
        yaw_rad, 0
    )
```

---

## 6. Reading Telemetry (Sensors)

```python
import time
import math
from pymavlink import mavutil

# ---- Connect to SITL ----
master = mavutil.mavlink_connection('udp:127.0.0.1:14550')
master.wait_heartbeat()
print(f"Connected: system {master.target_system}, component {master.target_component}")

# ---- Helper: wait for a message ----
def read_message(msg_name, blocking=False, timeout=1):
    msg = master.recv_match(type=msg_name, blocking=blocking, timeout=timeout)
    if msg:
        return msg.to_dict()
    return None

# ---- GPS → Local conversion ----
def gps_to_local(lat, lon, lat0, lon0):
    R = 6378137.0  # Earth radius (m)
    dLat = math.radians(lat - lat0)
    dLon = math.radians(lon - lon0)
    x = dLon * R * math.cos(math.radians(lat0))  # east
    y = dLat * R                                # north
    return x, y

# ---- Store home position (first GPS fix) ----
home_lat, home_lon = None, None

# ---- Main loop ----
while True:
    gps = read_message("GLOBAL_POSITION_INT")
    if gps:
        lat = gps['lat'] / 1e7
        lon = gps['lon'] / 1e7
        alt = gps['alt'] / 1000.0
        rel_alt = gps['relative_alt'] / 1000.0

        if home_lat is None:
            home_lat, home_lon = lat, lon
            print(f"[Home] lat={home_lat:.7f}, lon={home_lon:.7f}")

        print(f"[GPS] lat={lat:.7f}, lon={lon:.7f}, alt={alt:.2f} m, rel_alt={rel_alt:.2f} m")

    att = read_message("ATTITUDE")
    if att:
        roll = att['roll']
        pitch = att['pitch']
        yaw = att['yaw']
        print(f"[Attitude] roll={roll:.2f}, pitch={pitch:.2f}, yaw={yaw:.2f}")

    imu = read_message("RAW_IMU")
    if imu:
        ax = imu['xacc'] / 1000.0
        ay = imu['yacc'] / 1000.0
        az = imu['zacc'] / 1000.0
        gx = imu['xgyro'] / 1000.0
        gy = imu['ygyro'] / 1000.0
        gz = imu['zgyro'] / 1000.0
        mx, my, mz = imu['xmag'], imu['ymag'], imu['zmag']
        print(f"[IMU] Accel=({ax:.2f},{ay:.2f},{az:.2f}) m/s² | "
              f"Gyro=({gx:.2f},{gy:.2f},{gz:.2f}) rad/s | "
              f"Mag=({mx},{my},{mz})")

    if gps and att and home_lat is not None:
        x, y = gps_to_local(lat, lon, home_lat, home_lon)
        z = rel_alt
        print(f"[Local Pose] x={x:.2f} m, y={y:.2f} m, z={z:.2f} m | yaw={yaw:.2f} rad")

    ned = read_message("LOCAL_POSITION_NED")
    if ned:
        print(f"[LOCAL_NED] x={ned['x']:.2f} m (North), "
              f"y={ned['y']:.2f} m (East), "
              f"z={ned['z']:.2f} m (Down)")

    print("-" * 60)
    time.sleep(1)
```

---
