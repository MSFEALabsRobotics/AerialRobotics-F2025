# Tutorial: Latitude, Longitude, and Conversions

This tutorial introduces **latitude** and **longitude**, how they are used in GPS, and how we can work with them in Python using `pymavlink`.

---



<img width="650" height="333" alt="image" src="https://github.com/user-attachments/assets/6f0287a1-a407-40c3-9a43-4de01654cff4" />

## 🌍 What are Latitude and Longitude?

- **Latitude (lat)** measures how far north or south a point is from the equator, expressed in degrees (−90° to +90°).  
- **Longitude (lon)** measures how far east or west a point is from the Prime Meridian, expressed in degrees (−180° to +180°).  
- Together, `(lat, lon)` specifies a position anywhere on Earth.  
- GPS systems also provide **altitude** above sea level.

---

## 📡 Reading Latitude & Longitude from SITL

Example using `GLOBAL_POSITION_INT` messages:

```python
# Global position (GPS + altitude)
gps = read_message("GLOBAL_POSITION_INT")
if gps:
    lat = gps['lat'] / 1e7    # degrees
    lon = gps['lon'] / 1e7    # degrees
    alt = gps['alt'] / 1000.0 # AMSL (m)
    rel_alt = gps['relative_alt'] / 1000.0 # relative to home (m)

    # Set home position once
    if home_lat is None:
        home_lat, home_lon = lat, lon
        print(f"[Home] lat={home_lat:.7f}, lon={home_lon:.7f}")

    print(f"[GPS] lat={lat:.7f}, lon={lon:.7f}, alt={alt:.2f} m, rel_alt={rel_alt:.2f} m")
```

---

## 🔄 Converting Between GPS and Local X/Y

To convert GPS `(lat, lon)` into local Cartesian coordinates `(x, y)` relative to a home position:

```python
import math

def gps_to_local(lat, lon, lat0, lon0):
    R = 6378137.0  # Earth radius (m)
    dLat = math.radians(lat - lat0)
    dLon = math.radians(lon - lon0)
    x = dLon * R * math.cos(math.radians(lat0))  # east direction
    y = dLat * R                                # north direction
    return x, y
```

To convert back from local `(x, y)` to `(lat, lon)`:

```python
def local_to_gps(x, y, lat0, lon0):
    R = 6378137.0
    dLat = y / R
    dLon = x / (R * math.cos(math.radians(lat0)))
    lat = lat0 + math.degrees(dLat)
    lon = lon0 + math.degrees(dLon)
    return lat, lon
```

---

## 🚁 Running SITL with Two UDP Outputs

If you want SITL to stream MAVLink data to **two different UDP ports**, run:

```bash
~/ardupilot/Tools/autotest/sim_vehicle.py -v ArduCopter -f airsim-copter --console --map \
  -A "--sim-address=172.29.160.1 --sim-port-in=9002 --sim-port-out=9003"   --out udp:127.0.0.1:14550 --out=udp:127.0.0.1:14551
```

This sends MAVLink messages to **port 14550** and **port 14551** simultaneously.

---

## 🖥️ Mission Planner Installation

You can install Mission Planner following the official guide:  

👉 [Mission Planner Installation Guide](https://ardupilot.org/planner/docs/mission-planner-installation.html)

---
