# core/stats_calculator.py

import numpy as np

class StatsCalculator:
    def __init__(self, spacing: tuple):
        self.spacing = spacing  # (row_spacing, col_spacing, slice_thickness)

    def calculate_roi_stats(self, roi_mask: np.ndarray, image_array: np.ndarray) -> dict:
        """
        Calculates ROI statistics: mean, standard deviation and size in mm².

        Args:
            roi_mask (e.g.ndarray): ROI mask (1 - ROI, 0 - outside ROI).
            image_array (e.g.ndarray): Original CT image.

        Returns:
            dict: Dictionary with keys 'mean', 'std', 'size_mm2'.
        """

        roi_pixels = image_array[roi_mask == 1]
        mean_val = np.mean(roi_pixels)
        std_val = np.std(roi_pixels)
        # Calculating size in mm²
        row_spacing, col_spacing, _ = self.spacing
        num_pixels = np.sum(roi_mask)
        size_mm2 = num_pixels * row_spacing * col_spacing
        return {
            'mean': mean_val,
            'std': std_val,
            'size_mm2': size_mm2
        }
