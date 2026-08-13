import sys
import cv2
from vision import VisionTracker
from mavlink_control import DroneController
import numpy as np

SIMULATION_MODE = True 

if SIMULATION_MODE:
    CONNECTION_STRING = 'udp:127.0.0.1:14550'
    BAUD_RATE = 115200
else:
    CONNECTION_STRING = '/dev/ttyUSB0'
    BAUD_RATE = 921600

def main():
    drone = DroneController(CONNECTION_STRING, BAUD_RATE)
    tracker = VisionTracker(is_sim=SIMULATION_MODE)

    print("[System] Starting main loop. Press 'q' to exit.")
    dummy_frame = 225 * np.ones((480, 640, 3), dtype=np.uint8)

    while True:
        if SIMULATION_MODE:
            frame, offsets, found = tracker.process_frame(dummy_frame)
        else:
            frame, offsets, found = tracker.process_frame()
        if frame is None:
            continue
        if found:
            angle_x, angle_y = offsets
            drone.send_landing_target(angle_x, angle_y)
        cv2.imshow("Computer Vision Feed", frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    tracker.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
        