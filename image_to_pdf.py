from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import PyPDF2


def images_to_pdf(output_pdf):
    # Get a list of image files in the current directory
    image_files = [f for f in os.listdir('.') if f.endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif'))]
    image_files.sort()  # Sort the images to maintain order

    # Create a canvas for the PDF
    pdf_canvas = canvas.Canvas(output_pdf, pagesize=letter)
    
    for image_file in image_files:
        img = Image.open(image_file)
        img_width, img_height = img.size
        
        # Resize image if it is larger than the PDF size
        max_width, max_height = letter
        if img_width > max_width or img_height > max_height:
            ratio = min(max_width/img_width, max_height/img_height)
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

def compress_pdf(input_pdf, output_pdf):
    # Read the existing PDF
    pdf_reader = PyPDF2.PdfReader(input_pdf)
    pdf_writer = PyPDF2.PdfWriter()
    
    # Copy pages to the new PDF with compression
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_writer.add_page(page)
    
    # Write the compressed PDF
    with open(output_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)

# Example usage
output_pdf = 'output.pdf'
images_to_pdf(output_pdf)

# Check the size of the generated PDF and compress if necessary
if os.path.getsize(output_pdf) > 10 * 1024 * 1024:  # 10 MB in bytes
    compressed_pdf = 'compressed_output.pdf'
    compress_pdf(output_pdf, compressed_pdf)
    os.remove(output_pdf)  # Optionally remove the original large PDF
    os.rename(compressed_pdf, output_pdf)
