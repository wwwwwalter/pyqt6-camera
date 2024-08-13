from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class PhotoGallery(QWidget):
    def __init__(self, photos, parent=None):
        super().__init__(parent)
        self.photos = photos
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        # 创建一个水平布局来放置图片
        photo_layout = QHBoxLayout()
        photo_layout.setContentsMargins(0, 0, 0, 0)  # 设置外边距为0
        photo_layout.setSpacing(10)  # 设置间距

        # 添加图片到布局中
        for photo_path in self.photos:
            pixmap = QPixmap(photo_path)
            label = QLabel(self)
            label.setPixmap(pixmap.scaledToWidth(200))  # 调整图片大小
            photo_layout.addWidget(label)

        # 创建一个可滚动的区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(QWidget())  # 创建一个空的 QWidget 作为容器
        scroll_area.widget().setLayout(photo_layout)  # 将图片布局设置为容器的布局
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)  # 显示水平滚动条

        main_layout.addWidget(scroll_area)

if __name__ == '__main__':
    app = QApplication([])

    # 示例图片路径列表
    photo_paths = [
        "test.png",
        "test.png",
        "test.png",
        "test.png",
        "test.png",
        "test.png",
        "test.png",
        "test.png"
    ]

    gallery = PhotoGallery(photo_paths)
    gallery.show()

    app.exec()
