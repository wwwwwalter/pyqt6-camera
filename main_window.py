from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
import sys

from camera_thread import CameraThread


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Camera Feed')
        self.setGeometry(300, 300, 800, 600)

        # 创建一个标签用于显示图像
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # 创建并启动摄像头线程
        self.camera_thread = CameraThread(self)
        self.camera_thread.image_data.connect(self.update_image)
        self.camera_thread.start()

        # 定时器，用于定期更新图像
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(30)  # 每30毫秒更新一次

    def update_image(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        self.camera_thread.stop()
        event.accept()
