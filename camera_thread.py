import cv2
import time
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QThreadPool, QRunnable
from PyQt6.QtGui import QImage

from frame_handle import FrameHandle


class CameraThread(QThread):
    image_data = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cap = cv2.VideoCapture(0)  # 打开默认摄像头
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            start_time = time.time()  # 记录开始时间
            ret, frame = self.cap.read()
            if ret:

                QThreadPool.globalInstance().tryStart(FrameHandle(frame, self))
                print(QThreadPool.globalInstance().activeThreadCount())

                # cv2.imshow("Camera", frame)
                # cv2.waitKey(1)
                #
                # rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # h, w, ch = rgb_image.shape
                # print(h, w, ch)
                # bytes_per_line = ch * w
                # convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                # p = convert_to_qt_format.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
                # self.image_data.emit(p)
                # end_time = time.time()  # 记录结束时间
                # elapsed_time_ms = (end_time - start_time) * 1000  # 计算耗时并转换为毫秒
                # print(f"本轮循环耗时: {elapsed_time_ms:.2f} ms")  # 输出耗时
            else:
                break

    def stop(self):
        self.running = False
        self.cap.release()
        self.quit()
