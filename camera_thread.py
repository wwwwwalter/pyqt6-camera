import json

import cv2
import time
import platform
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QThreadPool, QRunnable, QEvent, QDir, pyqtSlot
from PyQt6.QtGui import QImage

from frame_handle_capture import FrameHandleCapture
# from frame_handle_pdf import FrameHandlePdf
from frame_handle_ai import FrameHandleAI
from frame_singleton import FrameListManager
from report_singleton import ReportListManager


class CameraThread(QThread):
    update_ai_result = pyqtSignal(dict)
    clear_screen = pyqtSignal()
    update_signal_source = pyqtSignal(bool)
    update_ai_switch = pyqtSignal(bool)

    def __init__(self, parent=None, model=None):
        super().__init__(parent)
        self.last_capture_pic_name = None
        self.report_count = 0
        self.image_count = 0
        self.main_window = parent
        self.model = model

        self.running = True
        self.camera_flag = False
        self.ai_flag = True

        self.frame_list_manager = FrameListManager()
        self.report_list_manager = ReportListManager()

    def initialize_camera(self):
        try:
            # 尝试打开默认摄像头
            if platform.system() == 'Windows':
                self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            elif platform.system() == 'Linux':
                self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

            # 检查摄像头是否成功打开
            if not self.cap.isOpened():
                raise IOError("Cannot open webcam")

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

            self.camera_flag = True
            self.update_signal_source.emit(True)

        except IOError as e:
            # 记录错误信息
            print(f"Error opening camera: {e}")
            # 提供可能的解决方案
            print("Please check if the camera is available and not used by another application.")
            self.update_signal_source.emit(False)
            # 可以考虑在这里添加更详细的错误处理逻辑，如重试机制
            if self.running:
                time.sleep(2)
                self.initialize_camera()

    def run(self):
        # 初始化相机
        self.initialize_camera()

        frame_count = 0
        while self.running:
            start_time = time.time()  # 记录开始时间
            ret, frame = self.cap.read()
            if ret:
                if self.ai_flag:  # AI打开状态
                    frame_count += 1
                    if frame_count == 30:
                        frame_count = 0
                        QThreadPool.globalInstance().tryStart(FrameHandleAI(frame, self.model, self.main_window))
            else:
                # 清屏
                self.clear_screen.emit()
                # 再次初始化相机
                self.initialize_camera()
        print("break")
        self.cap.release()
        print("cap release")

    def stop(self):
        self.running = False
        self.quit()
        print("quit")
        self.wait()
        print("wait")

    def on_controller_signal(self, signal):
        if signal == 49:  # 开关AI
            self.ai_flag = not self.ai_flag
            self.update_ai_switch.emit(self.ai_flag)
            if not self.ai_flag:
                self.clear_screen.emit()
        elif signal == 50:  # 保存照片
            QThreadPool.globalInstance().tryStart(FrameHandleCapture(self.cap))
        elif signal == 51:  # 生成报告
            # QThreadPool.globalInstance().tryStart(FrameHandlePdf(self.cap, self.model))
            pass
        elif signal == 52:  # 保存视频
            print("保存视频")
            pass
        elif signal == 48:  # 清零
            self.frame_list_manager.clear_frames()
            self.report_list_manager.clear_reports()
            pass

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
