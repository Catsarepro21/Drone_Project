import time
from pymavlink import mavutil

class DroneController:
    def __init__(self, connection_string, baud_rate=921600):
        print(f"[MAVLINK] Connecting to {connection_string} at {baud_rate} baud...")
        try:
            self.master = mavutil.mavlink_connection(connection_string, baud=baud_rate)
            self.master.wait_heartbeat(timeout=10)
            print(f"[MAVLINK] Heartbeat received! System ID: {self.master.target_system}")
        except Exception as e:
            print(f"[MAVLINK ERROR] Failed to establish connection: {e}")
            raise e

    def send_landing_target(self, angle_x, angle_y, distance=2.5):
        """Sends vision target vector offsets to ArduPilot Kalman filter."""
        try:
            time_usec = int(time.time() * 1e6)
            self.master.mav.landing_target_send(
                time_usec,
                0,
                mavutil.mavlink.MAV_FRAME_BODY_NED,
                angle_x,
                angle_y,
                distance,
                0.0, 0.0,
                0.0, 0.0, 0.0,
                (1.0, 0.0, 0.0, 0.0),
                mavutil.mavlink.MAV_LANDING_TARGET_TYPE_VISION_FIDUCIAL,
                1
            )
        except Exception as e:
            print(f"[MAVLINK WARN] Failed to send landing target packet: {e}")

    def set_mode(self, mode_name):
        """Changes ArduPilot flight mode (e.g., 'GUIDED', 'RTL', 'LAND')."""
        if mode_name not in self.master.mode_mapping():
            print(f"[MAVLINK ERROR] Unknown mode requested: {mode_name}")
            return False
        
        mode_id = self.master.mode_mapping()[mode_name]
        self.master.mav.set_mode_send(
            self.master.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            mode_id,
        )
        print(f"[MAVLINK] Flight mode request sent: {mode_name}")
        return True