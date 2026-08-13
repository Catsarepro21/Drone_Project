import cv2
import numpy as np
from vision import VisionTracker

def run_test():
    tracker = VisionTracker(is_sim=True)
    dummy_frame = 225 * np.ones((480, 640, 3), dtype=np.uint8)

    cv2.circle(dummy_frame, (320, 240), 5, (0, 0, 0), -1)

    print("[Test] Running vision tracker test with dummy frame...")
    frame, angle_x, angle_y, found = tracker.process_frame(dummy_frame)

    print(f"[Test] Target found: {found} | Angle X: {angle_x:.4f} rad | Angle Y: {angle_y:.4f} rad")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_test()