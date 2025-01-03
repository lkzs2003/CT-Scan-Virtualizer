# gui/main_window.py

from PyQt5.QtWidgets import (
    QMainWindow, QAction, QFileDialog, QLabel, QSlider, QVBoxLayout,
    QWidget, QHBoxLayout, QPushButton, QGridLayout
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QImage
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from core.dicom_loader import DicomLoader
from core.image_processor import ImageProcessor
from core.stats_calculator import StatsCalculator
from gui.roi_selector import RoiSelector

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CT Viewer")
        self.resize(1200, 800)

        # Inicjalizacja zmiennych
        self.dicom_loader = None
        self.image_processor = None
        self.stats_calculator = None
        self.current_slice = 0
        self.roi_mask = None

        # Inicjalizacja GUI
        self.init_ui()

    def init_ui(self):
        # Menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Plik')
        load_action = QAction('Ładuj DICOM', self)
        load_action.triggered.connect(self.load_dicom)
        file_menu.addAction(load_action)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # CT Image
        self.image_label = QLabel("Brak obrazu")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(QSize(600, 600))
        main_layout.addWidget(self.image_label)

        # Side panels with controls
        side_panel = QVBoxLayout()
        main_layout.addLayout(side_panel)

        # Navigate between scans
        self.slice_slider = QSlider(Qt.Horizontal)
        self.slice_slider.setMinimum(0)
        self.slice_slider.setMaximum(0)
        self.slice_slider.setValue(0)
        self.slice_slider.setTickPosition(QSlider.TicksBelow)
        self.slice_slider.setTickInterval(1)
        self.slice_slider.valueChanged.connect(self.change_slice)
        side_panel.addWidget(QLabel("Numer skanu:"))
        side_panel.addWidget(self.slice_slider)

        # Regulation diagnostic window
        self.window_center_slider = QSlider(Qt.Horizontal)
        self.window_center_slider.setMinimum(-1000)
        self.window_center_slider.setMaximum(3000)
        self.window_center_slider.setValue(0)
        self.window_center_slider.setTickPosition(QSlider.TicksBelow)
        self.window_center_slider.setTickInterval(100)
        self.window_center_slider.valueChanged.connect(self.update_windowing)
        side_panel.addWidget(QLabel("Window Center:"))
        side_panel.addWidget(self.window_center_slider)

        self.window_width_slider = QSlider(Qt.Horizontal)
        self.window_width_slider.setMinimum(1)
        self.window_width_slider.setMaximum(2000)
        self.window_width_slider.setValue(400)
        self.window_width_slider.setTickPosition(QSlider.TicksBelow)
        self.window_width_slider.setTickInterval(100)
        self.window_width_slider.valueChanged.connect(self.update_windowing)
        side_panel.addWidget(QLabel("Window Width:"))
        side_panel.addWidget(self.window_width_slider)

        # Button to select ROI
        self.roi_button = QPushButton("Zaznacz ROI")
        self.roi_button.clicked.connect(self.select_roi)
        side_panel.addWidget(self.roi_button)

        # ROI Stats
        self.stats_label = QLabel("Statystyki ROI:")
        side_panel.addWidget(self.stats_label)

        # Histogram
        self.figure, self.ax = plt.subplots(figsize=(4,3))
        self.canvas_plot = FigureCanvas(self.figure)
        side_panel.addWidget(self.canvas_plot)

    def load_dicom(self):
        directory = QFileDialog.getExistingDirectory(self, "Wybierz katalog z DICOM")
        if directory:
            try:
                self.dicom_loader = DicomLoader(directory)
                image_array = self.dicom_loader.get_image_array()
                self.image_processor = ImageProcessor(image_array, self.dicom_loader.series)
                spacing = self.image_processor.get_spacing()
                self.stats_calculator = StatsCalculator(spacing)

                self.slice_slider.setMaximum(image_array.shape[0] - 1)
                self.slice_slider.setValue(0)
                self.current_slice = 0
                self.update_window_center_width()
                self.display_image()
            except Exception as e:
                self.show_error(f"Nie udało się załadować plików DICOM:\n{e}")

    def update_window_center_width(self):
        if self.image_processor:
            self.window_center_slider.setValue(int(self.image_processor.get_default_window_center()))
            self.window_width_slider.setValue(int(self.image_processor.get_default_window_width()))

    def display_image(self):
        if self.image_processor:
            image = self.image_processor.image_array[self.current_slice]
            center = self.window_center_slider.value()
            width = self.window_width_slider.value()
            windowed = self.image_processor.apply_windowing(image, center, width)

            # convert to QImage
            height, width_img = windowed.shape
            bytes_per_line = width_img
            q_image = QImage(windowed.data, width_img, height, bytes_per_line, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))

            # If ROI is selected, display image with ROI
            if self.roi_mask is not None:
                self.display_image_with_roi()

    def resizeEvent(self, event):
        self.display_image()

    def change_slice(self, value):
        self.current_slice = value
        self.display_image()

    def update_windowing(self):
        self.display_image()

    def select_roi(self):
        if not self.image_processor:
            self.show_error("Najpierw załaduj pliki DICOM.")
            return
        image = self.image_processor.image_array[self.current_slice]
        selector = RoiSelector(self, image)
        if selector.exec_():
            self.roi_mask = selector.get_roi_mask()
            self.display_image_with_roi()
            self.calculate_and_display_stats()

    def display_image_with_roi(self):
        if self.image_processor and self.roi_mask is not None:
            image = self.image_processor.image_array[self.current_slice]
            center = self.window_center_slider.value()
            width = self.window_width_slider.value()
            windowed = self.image_processor.apply_windowing(image, center, width)

            # Convert to RGB
            rgb_image = np.stack([windowed]*3, axis=-1)

            # Applying a ROI mask in red
            rgb_image[self.roi_mask == 1] = [255, 0, 0]

            height, width_img, _ = rgb_image.shape
            q_image = QImage(rgb_image.data, width_img, height, 3*width_img, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))

    def calculate_and_display_stats(self):
        if self.stats_calculator and self.roi_mask is not None:
            stats = self.stats_calculator.calculate_roi_stats(
                self.roi_mask, self.image_processor.image_array[self.current_slice]
            )
            stats_text = (
                f"Średnia: {stats['mean']:.2f}\n"
                f"Odch. std: {stats['std']:.2f}\n"
                f"Rozmiar (mm²): {stats['size_mm2']:.2f}"
            )
            self.stats_label.setText(f"Statystyki ROI:\n{stats_text}")

            # Adding histogram of ROI pixels
            self.ax.clear()
            roi_pixels = self.image_processor.image_array[self.current_slice][self.roi_mask == 1]
            self.ax.hist(roi_pixels.flatten(), bins=50, color='blue', alpha=0.7)
            self.ax.set_title("Histogram pikseli ROI")
            self.ax.set_xlabel("Intensywność")
            self.ax.set_ylabel("Liczba pikseli")
            self.canvas_plot.draw()

    def show_error(self, message):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Błąd", message)
