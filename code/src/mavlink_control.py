import time
import threading
from pymavlink import mavutil


class DroneController:
    def __init__(self, connection_string="/dev/ttyAMA0", baud_rate=921600):
        try:
            self.master = mavutil.mavlink_connection(connection_string, baud=baud_rate)
            self.master.wait_heartbeat(timeout=10)
        except Exception as e:
            print(f"[MAVLINK ERROR] Failed to establish connection: {e}")
            raise e

        self.target_system = self.master.target_system
        self.target_component = self.master.target_component

        self._lock = threading.Lock()
        self.armed = False
        self.current_mode = None
        self.local_position = None
        self.rangefinder_alt_m = None
        self._telemetry_stop = threading.Event()
        self._telemetry_thread = None

    def start_telemetry(self):
        self._request_message_interval(mavutil.mavlink.MAVLINK_MSG_ID_LOCAL_POSITION_NED, 10)
        self._request_message_interval(mavutil.mavlink.MAVLINK_MSG_ID_HEARTBEAT, 2)
        self._request_message_interval(mavutil.mavlink.MAVLINK_MSG_ID_DISTANCE_SENSOR, 10)

        self._telemetry_thread = threading.Thread(target=self._telemetry_loop, daemon=True)
        self._telemetry_thread.start()

    def stop_telemetry(self):
        self._telemetry_stop.set()
        if self._telemetry_thread is not None:
            self._telemetry_thread.join(timeout=2)

    def _request_message_interval(self, message_id, rate_hz):
        self.master.mav.command_long_send(
            self.target_system, self.target_component,
            mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
            0,
            message_id,
            int(1e6 / rate_hz),
            0, 0, 0, 0, 0,
        )

    def _telemetry_loop(self):
        while not self._telemetry_stop.is_set():
            msg = self.master.recv_match(blocking=True, timeout=0.5)
            if msg is None:
                continue
            msg_type = msg.get_type()

            if msg_type == "HEARTBEAT":
                with self._lock:
                    self.armed = bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
                    try:
                        self.current_mode = mavutil.mode_string_v10(msg)
                    except Exception:
                        self.current_mode = msg.custom_mode

            elif msg_type == "LOCAL_POSITION_NED":
                with self._lock:
                    self.local_position = (msg.x, msg.y, msg.z, msg.vx, msg.vy, msg.vz)

            elif msg_type == "DISTANCE SENSOR":
                with self._lock:
                    self.rangefinder_alt_m = msg.current_distance / 100.0

    def set_mode(self, mode_name):
        mode_mapping = self.master.mode_mapping()
        if mode_name not in mode_mapping:
            print(f"[MAVLINK ERROR] Unknown mode requested: {mode_name}")
            return False
 
        mode_id = mode_mapping[mode_name]
        self.master.mav.set_mode_send(
            self.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            mode_id,
        )
        return True
 
    def arm(self, wait_armed_timeout=10):
        self.master.mav.command_long_send(
            self.target_system, self.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            1, 0, 0, 0, 0, 0, 0,
        )
 
        deadline = time.time() + wait_armed_timeout
        while time.time() < deadline:
            with self._lock:
                if self.armed:
                    return True
            time.sleep(0.2)
        return False
 
    def auto_takeoff(self, target_altitude_m, wait_for_altitude=True, timeout=30):
        if not self.set_mode("GUIDED"):
            return False
        time.sleep(1)
 
        with self._lock:
            already_armed = self.armed
        if not already_armed and not self.arm():
            return False
 
        self.master.mav.command_long_send(
            self.target_system, self.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0, 0, 0, 0, 0, 0,
            target_altitude_m,
        )
 
        if not wait_for_altitude:
            return True
 
        deadline = time.time() + timeout
        while time.time() < deadline:
            with self._lock:
                pos = self.local_position
            if pos is not None:
                alt_m = -pos[2]
                if alt_m >= target_altitude_m * 0.95:
                    return True
            time.sleep(0.2)
        return False
 
    def send_landing_target(self, angle_x, angle_y, distance=2.5):
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
                1,
            )
        except Exception as e:
            print(f"[MAVLINK WARN] Failed to send landing target packet: {e}")
 
    def get_position_hold_feedback(self, vel_tolerance_ms=0.15):
        with self._lock:
            pos = self.local_position
            alt_rf = self.rangefinder_alt_m
 
        if pos is None:
            return {"valid": False}
 
        x, y, z, vx, vy, vz = pos
        horizontal_speed = (vx ** 2 + vy ** 2) ** 0.5
        stable = horizontal_speed <= vel_tolerance_ms
 
        return {
            "valid": True,
            "stable": stable,
            "horizontal_speed_ms": horizontal_speed,
            "vertical_speed_ms": vz,
            "altitude_m": -z,
            "rangefinder_altitude_m": alt_rf,
        }
 
    def land_here(self):
        return self.set_mode("LAND")
 
 
if __name__ == "__main__":
    import argparse
    from vision import VisionTracker, MODE_LOCAL, MODE_REMOTE
 
    parser = argparse.ArgumentParser()
    parser.add_argument("--connection", default="/dev/ttyAMA0")
    parser.add_argument("--baud", type=int, default=921600)
    parser.add_argument("--vision-mode", choices=[MODE_LOCAL, MODE_REMOTE], default=MODE_LOCAL)
    parser.add_argument("--takeoff-alt", type=float, default=5.0)
    args = parser.parse_args()
 
    drone = DroneController(args.connection, args.baud)
    drone.start_telemetry()
 
    vision = VisionTracker(mode=args.vision_mode)
 
    try:
        drone.auto_takeoff(args.takeoff_alt)
 
        landed = False
        while not landed:
            _frame, angle_x, angle_y, distance, found = vision.process_frame()
 
            if found:
                drone.send_landing_target(angle_x, angle_y, distance or 2.5)
 
                feedback = drone.get_position_hold_feedback()
                if feedback["valid"] and feedback["stable"] and feedback["altitude_m"] < 1.0:
                    drone.land_here()
                    landed = True
 
            time.sleep(0.05)
 
    except KeyboardInterrupt:
        pass
    finally:
        vision.release()
        drone.stop_telemetry()
