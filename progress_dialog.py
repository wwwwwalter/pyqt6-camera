import time

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QApplication
from PyQt6.QtCore import Qt


class CustomProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("生成报告")
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # 移除标题栏
        self.setFixedWidth(600)  # 设置宽度为600像素
        self.setFixedHeight(150) # 设置高度为100像素

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        self.label = QLabel("正在生成报告...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.setAutoClose(True)
        self.setAutoReset(True)

    def setAutoClose(self, auto_close):
        self.auto_close = auto_close

    def setAutoReset(self, auto_reset):
        self.auto_reset = auto_reset

    def closeEvent(self, event):
        if self.auto_close:
            # 当关闭对话框时，可以在这里执行一些操作
            # print("自动关闭对话框")
            event.accept()
        else:
            event.ignore()

    def resetProgress(self):
        if self.auto_reset:
            self.progress_bar.reset()
            self.progress_bar.setValue(0)

    def setValue(self, value):
        self.progress_bar.setValue(value)
        if value == 100:
            self.close()
