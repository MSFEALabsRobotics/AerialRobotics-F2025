from pymavlink import mavutil

# Connect to SITL (default port 14550)
master = mavutil.mavlink_connection('udp:127.0.0.1:14550')


# Wait for a heartbeat before sending commands
print("Waiting for heartbeat...")
master.wait_heartbeat()
print(f"Heartbeat from system {master.target_system} component {master.target_component}")




# Arm
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0, 1, 0, 0, 0, 0, 0, 0)
print("Arming...")



while True:
    # Get the next message (blocking)
    msg = master.recv_match(blocking=True)
    if not msg:
        continue

    msg_type = msg.get_type()
    if msg_type == "ATTITUDE":
        print(f"Roll: {msg.roll:.2f}, Pitch: {msg.pitch:.2f}, Yaw: {msg.yaw:.2f}")
    elif msg_type == "GLOBAL_POSITION_INT":
        lat = msg.lat / 1e7
        lon = msg.lon / 1e7
        alt = msg.relative_alt / 1000.0  # in meters
        print(f"Lat: {lat:.6f}, Lon: {lon:.6f}, Alt: {alt:.2f} m")
