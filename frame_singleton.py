from PyQt6.QtCore import QObject, pyqtSignal
import cv2


class Signals(QObject):
    update_image_count = pyqtSignal(int)
    add_photo_to_area = pyqtSignal()
    clear_photo_area = pyqtSignal()


class SingletonMeta(type):
    """
    这是一个使用元类（metaclass）实现的单例类的元类。
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FrameListManager(metaclass=SingletonMeta):
    def __init__(self):
        self.signals = Signals()
        self.frames = []

    def add_frame(self, name, frame, dframe):
        """添加一个新的图像帧到列表，包括名称和帧本身"""
        self.frames.append((name, frame, dframe))
        self.signals.update_image_count.emit(len(self.frames))  # 发射信号
        self.signals.add_photo_to_area.emit()

    def get_frames(self):
        """获取当前所有的图像帧列表，每个元素都是(name, frame)元组"""
        return self.frames

    def clear_frames(self):
        """清除所有图像帧"""
        self.frames.clear()
        self.signals.update_image_count.emit(0)  # 清除后发射信号
        self.signals.clear_photo_area.emit()

    def get_frame_by_index(self, index):
        """根据索引获取图像帧元组 (name, frame)"""
        if 0 <= index < len(self.frames):
            return self.frames[index]
        else:
            return None

    def get_frame_name_by_index(self, index):
        """根据索引获取图像帧名称"""
        if 0 <= index < len(self.frames):
            return self.frames[index][0]
        else:
            return None

    def get_frame_by_name(self, name):
        """根据名称获取图像帧"""
        for frame_info in self.frames:
            if frame_info[0] == name:
                return frame_info
        return None

    def get_last_frame(self):
        """获取最后一个图像帧"""
        if self.frames:
            return self.frames[-1]
        else:
            return None
