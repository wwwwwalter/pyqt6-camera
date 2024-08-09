# import cv2
#
# def main():
#     # 打开默认摄像头
#     cap = cv2.VideoCapture(0)
#
#     # 检查摄像头是否成功打开
#     if not cap.isOpened():
#         print("无法打开摄像头")
#         exit()
#
#     while True:
#         # 读取一帧图像
#         ret, frame = cap.read()
#
#         # 如果读取成功，则 ret 为 True
#         if not ret:
#             print("无法获取帧")
#             break
#
#         # 显示图像
#         cv2.imshow('Video', frame)
#
#         # 按 'q' 键退出循环
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     # 释放摄像头资源
#     cap.release()
#     cv2.destroyAllWindows()
#
# if __name__ == "__main__":
#     main()


from PyQt6.QtWidgets import QApplication
from main_window import MainWindow
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
