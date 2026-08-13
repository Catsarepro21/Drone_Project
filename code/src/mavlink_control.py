import time
from pymavlink import mavutil

class DroneController:
    def __init__(self, connection_string, baud_rate=921600):
        print(f"[MAVLINK Connection] Connecting to {connection_string} at {baud_rate} baud...")
        self.master = mavutil.mavlink_connection(connection_string, baud=baud_rate)
        self.master.wait_heartbeat()
        print(f"[MAVLINK Connection] Heartbeat received. System {self.master.target_system}")


    def send_landing_target(self, angle_x, angle_y, distance=2.5):
        time_usec = int(time.time() * 1e6)
        self.master.mav.landing_target_send(
            time_usec,
            0,
            mavutil.mavlink.MAV_FRAME_BODY_NED,
            angle_x,
            angle_y,
            distance,
            0, 0,
        )

    def set_mode(self, mode_name):
        if mode_name not in self.master.mode_mapping():
            print(f"[MAVLINK] Unknown mode: {mode_name}")
            return False
        mode_id = self.master.mode_mapping()[mode_name]
        self.master.mav.set_mode_send(
            self.master.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            mode_id,
        )
        return True