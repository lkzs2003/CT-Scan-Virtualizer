# core/dicom_loader.py

import pydicom
import os
from typing import List
import numpy as np


class DicomLoader:
    def __init__(self, directory: str):
        self.directory = directory
        self.series = self.load_dicom_series()

    def load_dicom_series(self) -> List[pydicom.dataset.FileDataset]:
        # Pobranie wszystkich plików z rozszerzeniem .dcm lub innych rozszerzeń DICOM
        dicom_files = [
            os.path.join(self.directory, f)
            for f in os.listdir(self.directory)
            if f.lower().endswith('.dcm') or self.is_dicom(os.path.join(self.directory, f))
        ]
        if not dicom_files:
            raise ValueError("Nie znaleziono plików DICOM w wybranym katalogu.")

        dicom_series = [pydicom.dcmread(f) for f in dicom_files]

        # Sortowanie według InstanceNumber lub ImagePositionPatient
        if all(hasattr(ds, 'InstanceNumber') for ds in dicom_series):
            dicom_series.sort(key=lambda x: str(x.InstanceNumber))
        elif all(hasattr(ds, 'ImagePositionPatient') for ds in dicom_series):
            dicom_series.sort(key=lambda x: float(x.ImagePositionPatient[2]))
        else:
            dicom_series.sort(key=lambda x: 0)  # Brak sortowania

        return dicom_series

    def is_dicom(self, filepath: str) -> bool:
        """Sprawdza, czy plik jest plikiem DICOM."""
        try:
            with open(filepath, 'rb') as f:
                preamble = f.read(132)
                prefix = f.read(4)
                return prefix == b'DICM'
        except:
            return False

    def get_image_array(self) -> np.ndarray:
        images_file = [ds.pixel_array for ds in self.series]
        images = []

        for x in range(len(images_file)):
            if len(np.shape(images_file[x]))>=3:
                for i in range(len(images_file[x])):
                    images.append(images_file[x][i])
            else:
                images.append(images_file[x])
                
        image_array = np.stack(images, axis=0)
        print(image_array)
        print("spacja\n")
        return image_array
