
# ISMED2024Z_Zad2_Siemionek_Kwieciński

## Project Topic
**Visualization of computed tomography (CT) data in the form of planar images.**

The program enables users to:
- Load multi-layered and various types of DICOM files.
- Adjust the diagnostic window (window width and center).
- Calculate ROI (Region of Interest) statistics, including:
  - Average value,
  - Standard deviation,
  - ROI size.
- Display the number of gray pixels on a histogram for selected ROIs.

---

## Usage of the Program

### Steps to Run the Program
1. Start the program by running `main.py`:
   ```bash
   python main.py
   ```
2. Select a folder containing DICOM files:
   - Use the **"PLIK"** button located in the upper-left corner of the application.
3. Choose a scan number:
   - Adjust the slider labeled **"Numer skanu:"** to pick the desired scan.
4. Read and process the file:
   - The loaded DICOM file will be displayed.

### Additional Features
- **Adjust Diagnostic Window:**
  - Use the sliders for **window width** and **window center** to modify the image's appearance.
- **Calculate ROI Statistics:**
  - Click the **"Zaznacz ROI"** button to define a region of interest (ROI).
  - View calculated data, including average, standard deviation, and size.
  - A histogram will display the number of gray pixels for the selected ROI.
- **Change the Open Folder:**
  - To load a different folder, start again from step 2.

---

## Required Python Libraries

To use the program, ensure you have the following Python libraries installed:
- `pydicom`
- `numpy`
- `matplotlib`
- `PyQt5`
- `opencv-python`
- `scipy`
- `pillow`

### Installation
To install all required libraries, run:
```bash
pip install -r requirements.txt
```

**If `requirements.txt` is unavailable, you can manually install dependencies:**
```bash
pip install pydicom numpy matplotlib PyQt5 opencv-python scipy pillow
```

---

## Authors
- **Łukasz Siemionek** 
- **Bartłomiej Kwieciński**
---

