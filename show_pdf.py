import sys
from PyQt6.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

class PDFViewer(QMainWindow):
    def __init__(self, pdf_path):
        super().__init__()

        self.setWindowTitle('PDF Viewer')
        self.setGeometry(100, 100, 800, 600)  # 设置主窗口的位置和大小

        # 创建一个 QWebEngineView 控件
        self.web_view = QWebEngineView()

        # 加载 PDF 文件
        self.load_pdf(pdf_path)

        # 设置中央部件
        self.setCentralWidget(self.web_view)

    def load_pdf(self, pdf_path):
        # 使用 QUrl 从本地文件系统加载 PDF 文件
        url = QUrl.fromLocalFile(pdf_path)
        self.web_view.load(url)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pdf_path = 'test.pdf'  # 指定 PDF 文件路径
    viewer = PDFViewer(pdf_path)
    viewer.show()
    sys.exit(app.exec())
