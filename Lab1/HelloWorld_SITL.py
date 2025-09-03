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
