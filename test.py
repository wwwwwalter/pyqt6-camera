import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QPushButton, QVBoxLayout, QWidget, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt6.QtWidgets import QInputDialog, QListWidgetItem


class ImageListApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图片列表")
        self.resize(800, 600)

        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        self.list_widget = QListWidget(self)
        layout.addWidget(self.list_widget)

        button_layout = QVBoxLayout()
        add_button = QPushButton("添加图片")
        add_button.clicked.connect(self.add_image)
        button_layout.addWidget(add_button)

        remove_button = QPushButton("删除图片")
        remove_button.clicked.connect(self.remove_image)
        button_layout.addWidget(remove_button)

        edit_button = QPushButton("编辑图片")
        edit_button.clicked.connect(self.edit_image)
        button_layout.addWidget(edit_button)

        query_button = QPushButton("查询图片")
        query_button.clicked.connect(self.query_image)
        button_layout.addWidget(query_button)

        layout.addLayout(button_layout)

        self.setCentralWidget(central_widget)

    def add_image(self):
        file_names, _ = QFileDialog.getOpenFileNames(self, "选择图片文件", "", "Images (*.png *.jpg *.jpeg)")
        for file_name in file_names:
            item = QListWidgetItem(file_name)
            item.setIcon(self.create_icon(file_name))
            self.list_widget.addItem(item)

    def create_icon(self, file_name):
        pixmap = QPixmap(file_name)
        return pixmap.scaledToHeight(64, Qt.SmoothTransformation)

    def remove_image(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "请选择要删除的图片")
            return

        for item in selected_items:
            self.list_widget.takeItem(self.list_widget.row(item))

    def edit_image(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "请选择要编辑的图片")
            return

        file_name, _ = QFileDialog.getOpenFileName(self, "选择图片文件", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            for item in selected_items:
                item.setText(file_name)
                item.setIcon(self.create_icon(file_name))

    def query_image(self):
        text, ok = QInputDialog.getText(self, "查询图片", "请输入图片名称:")
        if ok:
            items = self.list_widget.findItems(text, Qt.MatchContains)
            if not items:
                QMessageBox.warning(self, "警告", "未找到匹配的图片")
            else:
                self.list_widget.setCurrentItem(items[0])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageListApp()
    window.show()
    sys.exit(app.exec_())
