import os

import cv2
import time
from PyQt6.QtCore import QRunnable, QMetaObject, Q_ARG, Qt, QObject, pyqtSignal


class Signals(QObject):
    signal = pyqtSignal(str)


class FrameHandleCapture(QRunnable):
    def __init__(self, cap=None, parent=None):
        super().__init__()
        self.cap = cap
        self.parent = parent

        self.signals = Signals()
        self.signals.signal.connect(self.parent.update_last_captured_image)

    def run(self):
        self.capture_frame()

    def capture_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # h, w, ch = rgb_image.shape
            # bytes_per_line = ch * w
            # convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            # p = convert_to_qt_format.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
            # cv2.imwrite("captured_image.jpg", frame)

            now = int(time.time())
            timeArray = time.localtime(now)
            nowtime_str = time.strftime("%Y-%m-%d-%H-%M-%S", timeArray)
            year, month, day = nowtime_str.split('-')[:3]

            capture_path = "output/capture"
            dataset_path = "output/dataset"

            if not self.check_path_isexist(capture_path):
                os.makedirs(capture_path)
            if not self.check_path_isexist(dataset_path):
                os.makedirs(dataset_path)

                # 保存完整屏幕照片
                cv2.imwrite(capture_path + "/" + nowtime_str + ".jpg", frame)

                # 裁切中心正方形,计算裁剪区域的左上角坐标
                start_x = (1920 - 1080) // 2 - 40
                start_y = 0

                # 进行裁剪
                crop_img = frame[start_y:start_y + 1080, start_x:start_x + 1080]

                # 保存裁切后的中心画面
                cv2.imwrite(dataset_path + "/" + nowtime_str + ".jpg", crop_img)
                print("save img " + nowtime_str + ".jpg on %s" % capture_path)
                print("save img " + nowtime_str + ".jpg on %s" % dataset_path)

                # 更新最新照片名
                last_capture_pic_name = nowtime_str + ".jpg"
                # self.signals.signal.emit(last_capture_pic_name)

    def check_path_isexist(self, path_s):
        return os.path.isdir(path_s)
