from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap, QAction
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QMenu
import sys

from camera_thread import CameraThread


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.camera_thread = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Camera')
        self.setGeometry(0, 0, 1920, 1080)
        # self.showFullScreen()
        # self.setStyleSheet("background-color: black;")
        self.setStyleSheet("background-color: #313438; font: 30px '宋体'; color: white;")

        # 设置右键菜单策略
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)
        self.setLayout(main_layout)

        info_container = QFrame()
        imageList_container = QFrame()
        status_container = QFrame()

        main_layout.addWidget(info_container)
        main_layout.addWidget(imageList_container)
        main_layout.addWidget(status_container)

        # 第一层控件
        info_container.setStyleSheet("background-color: #313438;")
        up_layout = QHBoxLayout()
        up_layout.setContentsMargins(0, 0, 0, 0)
        up_layout.setSpacing(1)
        self.probability_label = QLabel("AI预测概率：")
        self.preview_label = QLabel("预览：")
        self.suggestion_label = QLabel("提供的建议：")
        self.probability_label.setStyleSheet("background-color: #1e1f22;")
        self.preview_label.setStyleSheet("background-color: #1e1f22;")
        self.suggestion_label.setStyleSheet("background-color: #1e1f22;")

        up_layout.addWidget(self.probability_label)
        up_layout.addWidget(self.preview_label)
        up_layout.addWidget(self.suggestion_label)

        info_container.setLayout(up_layout)

        # 第二层控件
        imageList_container.setStyleSheet("background-color: #1e1f22;")
        middle_layout = QVBoxLayout()
        middle_layout.addWidget(QLabel("图片列表"))
        imageList_container.setLayout(middle_layout)
        imageList_container.setMaximumHeight(200)

        # 第三层控件
        status_container.setStyleSheet("background-color: #1e1f22;")
        down_layout = QHBoxLayout()
        self.signalSource_label = QLabel("信号源：")
        self.imageCount_label = QLabel("图像数量：")
        self.reportCount_label = QLabel("报告数量：")
        down_layout.addWidget(self.signalSource_label)
        down_layout.addWidget(self.imageCount_label)
        down_layout.addWidget(self.reportCount_label)

        status_container.setLayout(down_layout)
        status_container.setMaximumHeight(60)
        main_layout.addWidget(status_container)

        # 创建并启动摄像头线程
        self.camera_thread = CameraThread(self)
        self.camera_thread.image_data.connect(self.update_image)
        self.camera_thread.start()

        # 定时器，用于定期更新图像
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update)
        # self.timer.start(30)  # 每30毫秒更新一次

    def update_image(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        self.camera_thread.stop()
        event.accept()

    def show_context_menu(self, pos):
        context_menu = QMenu(self)
        exit_action = QAction("关闭程序", self)
        exit_action.triggered.connect(self.close)
        context_menu.addAction(exit_action)
        context_menu.exec(self.mapToGlobal(pos))

    def mousePressEvent(self, a0):
        print(a0.pos())
        super().mousePressEvent(a0)
        if a0.button() == Qt.MouseButton.LeftButton:
            print("左键")
        elif a0.button() == Qt.MouseButton.RightButton:
            print("右键")


