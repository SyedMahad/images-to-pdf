# Image to PDF Converter

## Overview

**Image to PDF Converter** is a simple and efficient desktop application built with Python and Tkinter that allows you to convert a list of image files into a single PDF document. It also provides optional features like compressing the PDF and zipping the final output.

## Features

- **Convert Images to PDF:** Select multiple image files (JPG, PNG, BMP, GIF, etc.) and convert them into a single PDF document.
- **Optional Compression:** Automatically compress the PDF if the file size exceeds 10MB.
- **Zip the PDF:** Optionally, zip the PDF file after conversion.
- **Progress Tracking:** Visual progress bar to track the conversion process.
- **Help and About Sections:** Includes in-app help documentation and an about section with details about the application.

## Download and Installation

### Download

You can download the latest version of the application from the [Releases](https://github.com/SyedMahad/images-to-pdf/releases) page.

### Installation

![Python](https://img.shields.io/badge/python-3.12.5-blue.svg)
![tkinter](https://img.shields.io/badge/tkinter-8.6.14-green.svg)
![Pillow](https://img.shields.io/badge/pillow-10.4.0-green.svg)
![reportlab](https://img.shields.io/badge/reportlab-4.2.2-red.svg)
![PyPDF2](https://img.shields.io/badge/PyPDF2-3.0.1-purple.svg)

1. **Windows Users**:
   - Download the `ImageToPDFConverter.exe` file from the latest release.
   - No installation is required—simply double-click the executable file to run the application.

2. **Running the Application from Source**:
   - If you prefer to run the application from the source code, ensure you have Python 3.x installed.
   - Clone the repository or download the project files.
   - Install the required libraries using `pip`:
        ```bash
        pip install tkinter pillow reportlab pypdf2
        ```
    - Run the Python script:
        ```bash
        python image_to_pdf.py
        ```

### Packaging the Application (Optional)

To distribute the application as an executable:
1. Ensure you have PyInstaller installed:
    ```bash
    pip install pyinstaller
    ```
1. Create the executable:
    ```bash
    pyinstaller --onefile --windowed --icon=logo.ico --add-data "logo.png;." image_to_pdf.py
    ```
This will generate an executable in the dist directory.

## Usage

### Step-by-Step Guide

1. **Launch the Application:** Run the ImageToPDFConverter.exe file or start the Python script.
1. **Select Images:** Click on the "Select Images" button to choose the images you want to convert.
1. **Set Save Location:** Click "Save Location" to choose where the output PDF will be saved.
1. **Enter File Name:** Provide a name for the output PDF file.
1. **Optional:** Check the "Zip the PDF file after conversion" option if you want to compress and zip the output.
1. **Convert:** Click the "Convert" button to start the conversion process. The progress bar will indicate the progress.
1. **Success:** Upon successful conversion, a message box will show the location of the generated file.

### Help and About

- **Help:** Access usage instructions from the Help menu.
- **About:** View information about the application, including version number and developer details.

## Customization

- **Icons and Branding:** Customize the logo.ico and logo.png files to match your branding.
- **Adding More Features:** Extend the functionality by editing the provided Python code.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request with your enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details

## Contact

For any questions or suggestions, please open an issue in the repository.
