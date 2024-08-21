import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import PyPDF2
import zipfile
import tempfile

def images_to_pdf(output_pdf, images, progress_var):
    """
    Converts a list of images to a PDF file.

    Parameters:
    output_pdf (str): The file path where the PDF will be saved.
    images (list): List of image file paths to be converted.
    progress_var (tk.IntVar): Variable to update the progress bar.
    """
    if not images:
        messagebox.showinfo("No Images", "No images selected.")
        return

    pdf_canvas = canvas.Canvas(output_pdf, pagesize=letter)
    max_width, max_height = letter

    for i, image_file in enumerate(images):
        with Image.open(image_file) as img:
            img_width, img_height = img.size
            ratio = min(max_width / img_width, max_height / img_height)
            img_width = int(img_width * ratio)
            img_height = int(img_height * ratio)
            x = (max_width - img_width) / 2
            y = (max_height - img_height) / 2
            pdf_canvas.drawImage(image_file, x, y, width=img_width, height=img_height)
            pdf_canvas.showPage()
        
        # Update progress bar
        progress_var.set(int((i + 1) / len(images) * 100))
        root.update_idletasks()

    pdf_canvas.save()

def compress_pdf(input_pdf, output_pdf):
    """
    Compresses a PDF file.

    Parameters:
    input_pdf (str): The original PDF file path.
    output_pdf (str): The file path where the compressed PDF will be saved.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(input_pdf)
        pdf_writer = PyPDF2.PdfWriter()
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        with open(output_pdf, 'wb') as output_file:
            pdf_writer.write(output_file)
    except Exception as e:
        messagebox.showerror("Error", f"Error compressing PDF: {e}")

def zip_pdf(input_pdf, zip_name, pdf_name):
    """
    Zips the PDF file.

    Parameters:
    input_pdf (str): The PDF file path to be zipped.
    zip_name (str): The file path where the ZIP file will be saved.
    pdf_name (str): The name of the PDF file inside the ZIP.
    """
    try:
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(input_pdf, pdf_name)
    except Exception as e:
        messagebox.showerror("Error", f"Error zipping PDF: {e}")

def open_files():
    """
    Opens a file dialog to select image files and displays them in the listbox.
    """
    global image_files
    image_files = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    if image_files:
        file_list.delete(0, tk.END)
        for file in image_files:
            file_list.insert(tk.END, os.path.basename(file))

def select_save_location():
    """
    Opens a directory dialog to select the save location.
    """
    folder_path = filedialog.askdirectory()
    if folder_path:
        save_path.set(folder_path)

def convert_files(zip_option, progress_var):
    """
    Converts selected images to a PDF, optionally compresses the PDF, and zips it if specified.

    Parameters:
    zip_option (tk.BooleanVar): Whether to zip the PDF file.
    progress_var (tk.IntVar): Variable to update the progress bar.
    """
    if not image_files:
        messagebox.showinfo("No Images", "No images selected.")
        return

    if not save_path.get():
        messagebox.showerror("Error", "Please select a save location.")
        return

    if not file_name.get():
        messagebox.showerror("Error", "Please enter a file name.")
        return

    # Set file paths based on user selection and checkbox state
    if zip_option.get():
        output_file_path = os.path.join(save_path.get(), file_name.get() + ".zip")
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
            pdf_path = temp_pdf.name
        pdf_name_in_zip = file_name.get() + ".pdf"
    else:
        output_file_path = os.path.join(save_path.get(), file_name.get() + ".pdf")
        pdf_path = output_file_path

    images_to_pdf(pdf_path, image_files, progress_var)

    if os.path.exists(pdf_path):
        if os.path.getsize(pdf_path) > 10 * 1024 * 1024:
            compressed_pdf = pdf_path.replace(".pdf", "_compressed.pdf")
            compress_pdf(pdf_path, compressed_pdf)
            os.remove(pdf_path)
            pdf_path = compressed_pdf

        if zip_option.get():
            zip_pdf(pdf_path, output_file_path, pdf_name_in_zip)
            os.remove(pdf_path)
            messagebox.showinfo("Success", f"PDF zipped: {output_file_path}")
        else:
            messagebox.showinfo("Success", f"PDF generated: {output_file_path}")

    progress_var.set(0)

def create_gui():
    """
    Creates the main GUI for the Image to PDF Converter application.
    """
    global root, file_list, save_path, file_name, image_files

    root = tk.Tk()
    root.title("Image to PDF Converter")

    image_files = []

    # Set default save location to desktop or home directory
    default_save_location = os.path.expanduser("~/Documents")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # Open Button
    open_button = tk.Button(frame, text="Open", command=open_files)
    open_button.grid(row=0, column=0, padx=5, pady=5)

    # Listbox to display selected files
    file_list = tk.Listbox(frame, height=5, width=50)
    file_list.grid(row=0, column=1, padx=5, pady=5)

    # Save Location Button
    save_path = tk.StringVar(value=default_save_location)  # Set default save location here
    save_location_button = tk.Button(frame, text="Save Location", command=select_save_location)
    save_location_button.grid(row=2, column=0, padx=5, pady=5)

    # Entry to display save location
    save_location_entry = tk.Entry(frame, textvariable=save_path, width=50)
    save_location_entry.grid(row=2, column=1, padx=5, pady=5)

    # File Name Entry
    file_name = tk.StringVar()
    file_name_label = tk.Label(frame, text="File Name:")
    file_name_label.grid(row=3, column=0, padx=5, pady=5)
    file_name_entry = tk.Entry(frame, textvariable=file_name, width=50)
    file_name_entry.grid(row=3, column=1, padx=5, pady=5)

    # Zip Checkbox
    zip_option = tk.BooleanVar()
    zip_checkbox = tk.Checkbutton(frame, text="Zip the PDF file after conversion", variable=zip_option)
    zip_checkbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # Progress Bar
    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate", variable=progress_var)
    progress_bar.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    # Convert Button
    convert_button = tk.Button(frame, text="Convert", command=lambda: convert_files(zip_option, progress_var))
    convert_button.grid(row=6, column=0, padx=5, pady=10)

    # Close Button
    close_button = tk.Button(frame, text="Close", command=root.destroy)
    close_button.grid(row=10, column=2, columnspan=2, padx=5, pady=50)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
