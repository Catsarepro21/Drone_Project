import cv2
import numpy as np

class VisionTracker:
    def __init__(self, camera_index=0, is_sim=True):
        self.is_sim = is_sim
        if not self.is_sim:
            self.cap = cv2.VideoCapture(camera_index)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.parameters = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.dictionary, self.parameters)

    def process_frame(self, frame=None):
        if not self.is_sim and frame is None:
            ret, frame = self.cap.read()
            if not ret:
                return None, 0.0, 0.0, False

        if frame is None:
            return None, 0.0, 0.0, False

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = self.detector.detectMarkers(gray)

        frame_h, frame_w = frame.shape[:2]
        center_x, center_y = frame_w // 2, frame_h // 2

        angle_x, angle_y = 0.0, 0.0
        target_found = False

        if ids is not None:
            target_found = True
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            m_corners = corners[0][0]
            m_x = int(np.mean(m_corners[:, 0]))
            m_y = int(np.mean(m_corners[:, 1]))

            angle_x = ((m_x - center_x) / center_x) * np.radians(30)
            angle_y = ((m_y - center_y) / center_y) * np.radians(30)

            cv2.line(frame, (center_x, center_y), (m_x, m_y), (0, 0, 255), 2)

        return frame, angle_x, angle_y, target_found

    def release(self):
        if not self.is_sim and hasattr(self, 'cap'):
            self.cap.release()