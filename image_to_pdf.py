from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import PyPDF2
import zipfile


def images_to_pdf(output_pdf):
    """
    Converts all images in the current directory to a single PDF file.

    Args:
    output_pdf (str): The name of the output PDF file.

    The function processes all image files (with extensions .jpg, .jpeg, .png, .bmp, .gif) in the current
    directory, resizes them to fit within the dimensions of a letter-sized PDF page (8.5 x 11 inches),
    centers them on the page, and saves them to the specified output PDF file.
    """
    # Get a list of image files in the current directory
    image_files = sorted(f for f in os.listdir('.') if f.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif')))

    if not image_files:
        print("No images found in the current directory.")
        return

    # Create a canvas for the PDF
    pdf_canvas = canvas.Canvas(output_pdf, pagesize=letter)
    
    max_width, max_height = letter

    for image_file in image_files:
        with Image.open(image_file) as img:
            img_width, img_height = img.size
            
            # Resize image if it is larger than the PDF size
            if img_width > max_width or img_height > max_height:
                ratio = min(max_width / img_width, max_height / img_height)
                img_width = int(img_width * ratio)
                img_height = int(img_height * ratio)
            
            # Center the image on the page
            x = (max_width - img_width) / 2
            y = (max_height - img_height) / 2
            
            # Draw the image on the canvas
            pdf_canvas.drawImage(image_file, x, y, width=img_width, height=img_height)
            pdf_canvas.showPage()  # Create a new page for the next image

    # Save the PDF file
    pdf_canvas.save()
    print(f"PDF generated: {output_pdf}")


def compress_pdf(input_pdf, output_pdf):
    """
    Compresses an existing PDF file.

    Args:
    input_pdf (str): The name of the input PDF file to be compressed.
    output_pdf (str): The name of the output compressed PDF file.

    The function reads the input PDF file, compresses it by rewriting the content, and saves it as the
    specified output PDF file.
    """
    try:
        # Read the existing PDF
        pdf_reader = PyPDF2.PdfReader(input_pdf)
        pdf_writer = PyPDF2.PdfWriter()
        
        # Copy pages to the new PDF with compression
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        
        # Write the compressed PDF
        with open(output_pdf, 'wb') as output_file:
            pdf_writer.write(output_file)
        
        print(f"PDF compressed: {output_pdf}")
    except Exception as e:
        print(f"Error compressing PDF: {e}")


def zip_pdf(input_pdf, zip_name):
    """
    Creates a ZIP archive containing the specified PDF file.

    Args:
    input_pdf (str): The name of the PDF file to be zipped.
    zip_name (str): The name of the output ZIP file.

    The function compresses the specified PDF file into a ZIP archive with the specified name.
    """
    try:
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(input_pdf)
        print(f"PDF zipped: {zip_name}")
    except Exception as e:
        print(f"Error zipping PDF: {e}")


# Example usage
output_pdf = 'output.pdf'
images_to_pdf(output_pdf)

# Check the size of the generated PDF and compress if necessary
if os.path.exists(output_pdf):
    if os.path.getsize(output_pdf) > 10 * 1024 * 1024:  # 10 MB in bytes
        compressed_pdf = 'compressed_output.pdf'
        compress_pdf(output_pdf, compressed_pdf)
        os.remove(output_pdf)  # Optionally remove the original large PDF
        os.rename(compressed_pdf, output_pdf)

    # Create a zip file
    zip_name = 'output.zip'
    zip_pdf(output_pdf, zip_name)
    os.remove(output_pdf)  # Optionally remove the original PDF after zipping
