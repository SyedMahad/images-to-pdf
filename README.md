# Images to PDF Converter

A Python script that converts multiple images in the current directory into a single PDF file. If the generated PDF file size exceeds 10 MB, the script compresses it to reduce the size.

## Features

- Converts all images in the current directory to a single PDF.
- Supports popular image formats: JPG, JPEG, PNG, BMP, GIF.
- Automatically compresses the PDF if the file size is greater than 10 MB.

## Requirements
![Python](https://img.shields.io/badge/python-3.12.5-blue.svg)
![Pillow](https://img.shields.io/badge/pillow-10.4.0-green.svg)
![reportlab](https://img.shields.io/badge/reportlab-4.2.2-red.svg)
![PyPDF2](https://img.shields.io/badge/PyPDF2-3.0.1-purple.svg)

- Python 3.x
- `Pillow` for image processing
- `reportlab` for PDF generation
- `PyPDF2` for PDF compression

You can install the required libraries using pip:

```bash
pip install -r requirements.txt
```

## Usage
1. Place all the images you want to convert into the same directory as the script.
1. Run the script:
    ```bash
    python images_to_pdf.py
    ```
1. The script will generate `output.pdf` in the same directory. If the file size exceeds 10 MB, it will automatically compress the PDF

## Converting to an Executable
![pyinstaller](https://img.shields.io/badge/pyinstaller-6.10.0-orange.svg)  
To create a standalone `.exe` file, use `PyInstaller`:
```bash
pip install pyinstaller
pyinstaller --onefile images_to_pdf.py
```
The `.exe` file will be located in the `dist` folder.

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue to discuss changes.

## Contact
For any questions or suggestions, please open an issue in the repository.
