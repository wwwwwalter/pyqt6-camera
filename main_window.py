import glob
import json
import os

from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QDir, pyqtSlot
from PyQt6.QtGui import QImage, QPixmap, QAction
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QMenu, QSpacerItem, \
    QSizePolicy, QProgressDialog
import sys

from camera_thread import CameraThread
from model import LightNet
from frame_singleton import FrameListManager
from report_singleton import ReportListManager
from progress_singleton import ProgressValueManager


class MainWindow(QWidget):
    # 定义信号
    controller_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.camera_thread = None
        self.init_ui()

        # 加载病例
        self.load_case()

        # 加载模型
        self.model = LightNet(self.disease_category_num)

        # 创建单例列表
        self.frame_list_manager = FrameListManager()
        self.report_list_manager = ReportListManager()
        self.progress_value_manager = ProgressValueManager()
        self.frame_list_manager.signals.update_image_count.connect(self.on_update_image_count)
        self.report_list_manager.signals.update_report_count.connect(self.on_update_report_count)
        self.progress_value_manager.signals.show_progress_dialog.connect(self.on_show_progress_dialog)
        self.progress_value_manager.signals.update_progress_value.connect(self.on_update_progress_value)
        self.progress_value_manager.signals.cancel_progress_dialog.connect(self.on_cancel_progress_dialog)

        # progress dialog
        self.progress_dialog = QProgressDialog("正在生成报告...", "取消", 0, 100, self)
        self.progress_dialog.setWindowTitle("生成报告")
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # 移除标题栏
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setValue(0)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setAutoReset(True)
        self.progress_dialog.setFixedWidth(600)  # 设置宽度为600像素
        self.progress_dialog.close()

        # 创建并启动摄像头线程
        self.camera_thread = CameraThread(self, self.model)
        self.controller_signal.connect(self.camera_thread.on_controller_signal)
        self.camera_thread.clear_screen.connect(self.on_clear_screen)
        self.camera_thread.update_signal_source.connect(self.on_update_signal_source)
        self.camera_thread.update_ai_switch.connect(self.on_update_ai_switch)
        self.camera_thread.start()

    def init_ui(self):
        self.setWindowTitle('Camera')
        self.setGeometry(0, 0, 1920, 720)
        # self.showFullScreen()
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
        self.preview_label = QLabel()
        self.suggestion_label = QLabel("建议：")

        self.probability_label.setContentsMargins(20, 20, 20, 20)
        self.probability_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.suggestion_label.setContentsMargins(20, 20, 20, 20)
        self.suggestion_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.suggestion_label.setWordWrap(True)
        self.probability_label.setStyleSheet("background-color: #1e1f22;max-width: 400px;min-width: 400px;")
        self.preview_label.setStyleSheet("background-color: #1e1f22;")
        self.suggestion_label.setStyleSheet("background-color: #1e1f22")

        up_layout.addWidget(self.probability_label)
        # up_layout.addWidget(self.preview_label)
        up_layout.addWidget(self.suggestion_label)

        info_container.setLayout(up_layout)

        # 第二层控件
        imageList_container.setStyleSheet("background-color: #1e1f22;")
        middle_layout = QVBoxLayout()
        middle_layout.addWidget(QLabel("图片列表"))
        imageList_container.setLayout(middle_layout)
        imageList_container.setMaximumHeight(200)
        imageList_container.setMinimumHeight(200)

        # 第三层控件
        status_container.setStyleSheet("background-color: #1e1f22;")
        down_layout = QHBoxLayout()
        self.signalSource_label = QLabel("信号源：正在初始化...")
        self.ai_switch_label = QLabel("AI开关：开")
        self.imageCount_label = QLabel("图像数量：0")
        self.reportCount_label = QLabel("报告数量：0")
        down_layout.addWidget(self.signalSource_label)
        down_layout.addWidget(self.ai_switch_label)
        down_layout.addWidget(self.imageCount_label)
        down_layout.addWidget(self.reportCount_label)

        status_container.setLayout(down_layout)
        status_container.setMaximumHeight(60)
        main_layout.addWidget(status_container)

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

    def keyPressEvent(self, a0):
        super().keyPressEvent(a0)
        if a0.key() == Qt.Key.Key_Escape:
            print("Esc")
            self.close()
        else:
            self.controller_signal.emit(a0.key())

    @pyqtSlot(dict)
    def on_update_ai_result(self, result):

        disease_probability = result['disease_probability']
        disease_probability_index = result['disease_probability_index']

        disease_probability_info = ""
        for i in disease_probability_index:
            # 将概率转换为百分比形式并保留两位小数
            formatted_percentage = f"{disease_probability[i] * 100:.2f}%"

            # 确保疾病名称占位 4 个汉字的宽度
            formatted_disease_name = self.disease_category_name[i]
            if len(formatted_disease_name) < 4:
                formatted_disease_name += "  " * (4 - len(formatted_disease_name))

            # 添加到 disease_probability_info
            disease_probability_info += formatted_disease_name + "\t" + formatted_percentage + "\n"

        self.probability_label.setText(f"AI预测概率：\n{disease_probability_info}")

        name = self.disease_category_name[disease_probability_index[0]]
        report_simplified_info = self.all_case_info_dict[name][0]['简化版结果']
        treatment_simplified_info = self.all_case_info_dict[name][0]['简化版建议']
        self.suggestion_label.setText(f"建议：\n{report_simplified_info}\n\n{treatment_simplified_info}")

    def on_update_signal_source(self, status):
        if status:
            self.signalSource_label.setText(f"信号源：USB")
        else:
            self.signalSource_label.setText(f"信号源：无信号源")

    def on_update_ai_switch(self, status):
        if status:
            self.ai_switch_label.setText(f"AI开关：开")
        else:
            self.ai_switch_label.setText(f"AI开关：关")

    def on_update_image_count(self, count):
        self.imageCount_label.setText(f"图像数量：{count}")

    def on_update_report_count(self, count):
        self.reportCount_label.setText(f"报告数量：{count}")

    def on_clear_screen(self):
        self.probability_label.setText("AI预测概率：")
        self.suggestion_label.setText("建议：")
        # self.signalSource_label.setText("信号源：USB")
        # self.imageCount_label.setText(f"图像数量：0")
        # self.reportCount_label.setText(f"报告数量：0")

    def load_case(self):
        self.all_case_info_dict = {}
        self.disease_category_name = []
        self.disease_category_num = 0

        # 使用 Qt 的方式来遍历目录
        dir_path = QDir('case')
        entries = dir_path.entryInfoList(['*.json'], QDir.Filter.Files)

        for entry in entries:
            # 读取json文件
            filename = entry.absoluteFilePath()
            with open(filename, 'r', encoding='utf-8') as file:
                try:
                    case = json.load(file)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                else:
                    keys = case.keys()
                    name = list(keys)[0]
                    self.all_case_info_dict[name] = case[name]

        # 所有病例名称列表
        self.disease_category_name = list(self.all_case_info_dict.keys())
        # 病例名称种类个数
        self.disease_category_num = len(self.disease_category_name)

    def on_show_progress_dialog(self):

        self.progress_dialog.show()
        # self.progress_dialog.open()
        # self.progress_dialog.canceled.connect(self.on_cancel_progress_dialog)
        # self.progress_dialog.setValue(100)
        # self.progress_dialog.close()
        # self.progress_dialog.deleteLater()

    def on_update_progress_value(self, value):
        self.progress_dialog.setValue(value)

    def on_cancel_progress_dialog(self):
        self.progress_dialog.close()
