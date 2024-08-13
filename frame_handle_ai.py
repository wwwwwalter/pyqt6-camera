import cv2
import time
import torch.nn as nn
import torch
import numpy as np
from PyQt6.QtCore import QRunnable, pyqtSignal, Qt, QObject, QMetaObject, Q_ARG


class Signals(QObject):
    signal = pyqtSignal(dict)



class FrameHandleAI(QRunnable):

    def __init__(self, frame, model=None, parent=None):
        super().__init__()
        self.setAutoDelete(True)
        self.frame = frame
        self.model = model
        self.main_window = parent
        self.signals = Signals()
        self.signals.signal.connect(self.main_window.on_update_ai_result)

    def run(self):
        self.classify_disease()

    def classify_disease(self):
        self.frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_NEAREST)
        target_img = torch.from_numpy(cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY).astype(np.float32).reshape((1, 1, 270, 480)))
        with torch.no_grad():
            self.model.eval()
            output = self.model(target_img)

            disease_probability = output.numpy()[0]
            disease_probability_index = np.argsort(disease_probability)[::-1]

            disease_probability = disease_probability.astype(float).tolist()




            disease_probability_info = {
                "disease_probability": disease_probability,
                "disease_probability_index": disease_probability_index
            }

            self.signals.signal.emit(disease_probability_info)
