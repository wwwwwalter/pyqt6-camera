import cv2
import time
import platform
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QThreadPool, QRunnable
from PyQt6.QtGui import QImage

from frame_handle import FrameHandle


class CameraThread(QThread):
    image_data = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = False
        self.initialize_camera()

        cv2.namedWindow("image", cv2.WINDOW_FREERATIO)
        cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def initialize_camera(self):
        try:
            # 尝试打开默认摄像头
            if platform.system() == 'Windows':
                self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            elif platform.system() == 'Linux':
                self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            self.cap.set(cv2.CAP_PROP_FPS, 30.0)
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))

            # 获取FourCC
            fourcc = int(self.cap.get(cv2.CAP_PROP_FOURCC))
            # 将FourCC转换为对应的字符
            fourcc_char = chr((fourcc >> 0) & 0xFF) + chr((fourcc >> 8) & 0xFF) + chr((fourcc >> 16) & 0xFF) + chr(
                (fourcc >> 24) & 0xFF)
            print(f"Current FourCC: {fourcc_char}")

            # 检查摄像头是否成功打开
            if not self.cap.isOpened():
                raise IOError("Cannot open webcam")

            # 如果摄像头成功打开，可以继续初始化其他操作


        except IOError as e:
            # 记录错误信息
            print(f"Error opening camera: {e}")
            # 提供可能的解决方案
            print("Please check if the camera is available and not used by another application.")
            # 可以考虑在这里添加更详细的错误处理逻辑，如重试机制

    def run(self):
        self.running = True
        while self.running:
            start_time = time.time()  # 记录开始时间
            ret, frame = self.cap.read()
            if ret:

                QThreadPool.globalInstance().tryStart(FrameHandle(frame, self))
                # print(QThreadPool.globalInstance().activeThreadCount())

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
                # 运行中拔掉相机
                break
        print("break")
        self.cap.release()
        print("cap release")
        cv2.destroyAllWindows()
        print("cv2 destroyAllWindows")

    def stop(self):
        self.running = False
        self.quit()
        print("quit")
        self.wait()
        print("wait")
