from PyQt6.QtCore import QObject, pyqtSignal


class Signals(QObject):
    show_progress_dialog = pyqtSignal()
    update_progress_value = pyqtSignal(int)
    cancel_progress_dialog = pyqtSignal()


class SingletonMeta(type):
    """
    这是一个使用元类（metaclass）实现的单例类的元类。
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ProgressValueManager(metaclass=SingletonMeta):
    def __init__(self):
        self.signals = Signals()
        self.value = 0

    def show_progress_dialog(self):
        self.signals.show_progress_dialog.emit()

    def set_progress_value(self, value):
        self.value = value
        self.signals.update_progress_value.emit(value)

    def cancel_progress_dialog(self):
        self.signals.cancel_progress_dialog.emit()
