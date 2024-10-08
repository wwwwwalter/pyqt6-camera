import cv2
import time
from PyQt6.QtCore import QRunnable, QMetaObject, Q_ARG, Qt, QObject


class FrameHandle(QRunnable,QObject):
    def __init__(self, shared_image, parent=None):
        super().__init__()
        self.shared_image = shared_image
        self.main_window = parent

    def run(self):
        # 处理逻辑
        cv2.imshow("image", self.shared_image)
        # cv2.waitKey(100)
        time.sleep(0.1)  # 500ms
        pass


