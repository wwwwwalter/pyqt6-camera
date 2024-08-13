from PyQt6.QtCore import QObject, pyqtSignal


class Signals(QObject):
    update_report_count = pyqtSignal(int)


class SingletonMeta(type):
    """
    这是一个使用元类（metaclass）实现的单例类的元类。
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ReportListManager(metaclass=SingletonMeta):
    def __init__(self):
        self.signals = Signals()
        self.reports = []

    def add_report(self, name):
        self.reports.append(name)
        self.signals.update_report_count.emit(len(self.reports))  # 发射信号

    def clear_reports(self):
        self.reports.clear()
        self.signals.update_report_count.emit(0)  # 清除后发射信号

    def get_report_name_by_index(self, index):
        """根据索引获取图像帧名称"""
        if 0 <= index < len(self.reports):
            return self.reports[index]
        else:
            return None
