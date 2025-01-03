# core/image_processor.py

import numpy as np
from typing import List
import pydicom

class ImageProcessor:
    def __init__(self, image_array: np.ndarray, dicom_series: List[pydicom.dataset.FileDataset]):
        self.image_array = image_array
        self.dicom_series = dicom_series
        self.window_center = self.get_default_window_center()
        self.window_width = self.get_default_window_width()

    def get_default_window_center(self):
        # Center of the diagnostic window
        return np.mean(self.image_array)

    def get_default_window_width(self):
        # Width of the diagnostic window
        return np.std(self.image_array)

    def apply_windowing(self, image: np.ndarray, center: int, width: int) -> np.ndarray:
        lower = center - (width / 2)
        upper = center + (width / 2)
        windowed_image = np.clip(image, lower, upper)
        windowed_image = ((windowed_image - lower) / width) * 255.0
        windowed_image = windowed_image.astype(np.uint8)
        return windowed_image

    def get_spacing(self):
        # Retrieving pixel space information from DICOM
        ds = self.dicom_series[0]
        try:
            pixel_spacing = ds.PixelSpacing  # [row_spacing, col_spacing]
            slice_thickness = ds.SliceThickness
            return float(pixel_spacing[0]), float(pixel_spacing[1]), float(slice_thickness)
        except AttributeError:
            # Default values
            return 1.0, 1.0, 1.0
