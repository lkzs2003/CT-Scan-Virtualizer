# gui/roi_selector.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

class RoiSelector(QDialog):
    def __init__(self, parent, image):
        super().__init__(parent)
        self.setWindowTitle("Zaznacz ROI")
        self.image = image
        self.roi = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Matplotlib Figure
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.ax.imshow(self.image, cmap='gray')
        self.rect = None
        self.start_pos = None
        self.end_pos = None

        # OK Button
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        # Mouse events
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_move)

    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        self.start_pos = (int(event.xdata), int(event.ydata))
        if self.rect:
            self.rect.remove()
            self.rect = None
        self.rect = patches.Rectangle(
            self.start_pos, 0, 0, linewidth=1, edgecolor='r', facecolor='none'
        )
        self.ax.add_patch(self.rect)
        self.canvas.draw()

    def on_move(self, event):
        if not self.rect or not self.start_pos:
            return
        if event.inaxes != self.ax:
            return
        current_pos = (int(event.xdata), int(event.ydata))
        width = current_pos[0] - self.start_pos[0]
        height = current_pos[1] - self.start_pos[1]
        self.rect.set_width(width)
        self.rect.set_height(height)
        self.canvas.draw()

    def on_release(self, event):
        if not self.rect:
            return
        if event.inaxes != self.ax:
            return
        self.end_pos = (int(event.xdata), int(event.ydata))
        self.accept()

    def get_roi_mask(self):
        if self.start_pos and self.end_pos:
            x1, y1 = self.start_pos
            x2, y2 = self.end_pos
            x_min, x_max = sorted([x1, x2])
            y_min, y_max = sorted([y1, y2])
            mask = np.zeros_like(self.image, dtype=np.uint8)
            mask[y_min:y_max, x_min:x_max] = 1
            return mask
        return None
