# ismed2024Z_zad2_Siemionek_Kwieciński



## Project Topic

Visualization of computed tomography (CT) data in the form of planar images.
Program allows to load muli layered and multiple type of DICOM files. It allows to regulate the diagnostic window and calculates ROI with all it's statistics (average, standard deviation and size).

### Usage of the program

1. Start the program using main.py
2. Choose a folder with DICOM files, with the "PLIK" button in the upper left corner
3. Choose the scan number with "Numer skanu:" slider
4. Read the file
    - adjust the window width and center with appropriate sliders
    - Using ROI selection under "Zaznacz ROI" button, calculate all nessesary data and show number of grey pixels on the histogram
5. To change current open folder, start from point 2

# Required python libraries

- pydicom
- numpy
- matplotlib
- PyQt5
- opencv-python
- scipy
- pillow