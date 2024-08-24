import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import sys
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
    progress_var.set(0)
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

def convert_files(zip_option, progress_var, compression_threshold):
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
        # Compress if the file size is larger than the compression threshold
        if os.path.getsize(pdf_path) > compression_threshold.get() * 1024 * 1024:
            compressed_pdf = pdf_path.replace(".pdf", "_compressed.pdf")
            compress_pdf(pdf_path, compressed_pdf)
            os.remove(pdf_path)
            pdf_path = compressed_pdf

        # Zip the PDF if the option is selected
        if zip_option.get():
            zip_pdf(pdf_path, output_file_path, pdf_name_in_zip)
            os.remove(pdf_path)
            messagebox.showinfo("Success", f"PDF zipped to location: {output_file_path}")
        else:
            messagebox.showinfo("Success", f"PDF generated to location: {output_file_path}")

    # Reset the progress bar
    progress_var.set(0)

def on_enter_button_convert(e):
    """Changes the background and text color when hovering over the Convert button."""
    e.widget['bg'] = '#76c893'  # Light Green
    e.widget['fg'] = 'black'

def on_leave_button_convert(e):
    """Resets the background and text color when leaving the Convert button."""
    e.widget['bg'] = 'green'  # Green
    e.widget['fg'] = 'white'

def on_enter_button_close(e):
    """Changes the background and text color when hovering over the Close button."""
    e.widget['bg'] = '#fa8072'  # Light Coral
    e.widget['fg'] = 'black'

def on_leave_button_close(e):
    """Resets the background and text color when leaving the Close button."""
    e.widget['bg'] = 'red'  # Firebrick (Red)
    e.widget['fg'] = 'white'

def on_enter_button(e):
    """Changes the background and text color when hovering over general buttons."""
    e.widget['bg'] = '#add8e6'  # Light Blue
    e.widget['fg'] = 'black'

def on_leave_button(e):
    """Resets the background and text color when leaving general buttons."""
    e.widget['bg'] = 'blue'  # Steel Blue
    e.widget['fg'] = 'white'

def resource_path(relative_path):
    """ Get absolute path to resource, works for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def show_help():
    """ Display help documentation """
    help_text = (
        "How to Use Image to PDF Converter:\n\n"
        "1. Click 'Select Images' to choose the image files you want to convert.\n"
        "2. Select the location to save the PDF using the 'Save Location' button.\n"
        "3. Enter a file name for the output PDF in the 'File Name' field.\n"
        "4. (Optional) Check the 'Zip the PDF file after conversion' option if you want the PDF file to be compressed and zipped.\n"
        "5. Click 'Convert' to start the conversion process. The progress bar will show the conversion progress.\n"
        "6. Once completed, a success message will be displayed with the location of the generated PDF or ZIP file.\n\n"
        "For more information, visit the official documentation or contact support."
    )
    messagebox.showinfo("Help - Image to PDF Converter", help_text)

def show_about():
    """ Display information about the application """
    about_text = (
        "Image to PDF Converter\n"
        "Version 2.1.0\n\n"
        "Developed by Syed Mahad Ehsan.\n"
        "This application allows you to convert images to PDF files with optional compression and zipping functionality.\n\n"
        "For more information, visit https://github.com/SyedMahad/images-to-pdf."
    )
    messagebox.showinfo("About - Image to PDF Converter", about_text)

def open_settings(compression_threshold):
    """
    Opens a settings window to adjust application settings.
    """
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")

    # # Get the screen width and height
    # screen_width = root.winfo_screenwidth()
    # screen_height = root.winfo_screenheight()

    # # Calculate the x and y coordinates to center the window
    # x_cordinate = int(screen_width / 2)
    # y_cordinate = int(screen_height / 2)

    # # Set the geometry of the window to center it on the screen
    # root.geometry(f"{x_cordinate}+{y_cordinate}")

    tk.Label(settings_window, text="Compression Threshold (MB):").grid(row=0, column=0, padx=5, pady=5)
    threshold_entry = tk.Entry(settings_window, textvariable=compression_threshold)
    threshold_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Button(
        settings_window, text="Save", command=settings_window.destroy, bg="blue", fg="white"
    ).grid(
        row=1, column=0, columnspan=2, pady=10
    ).bind(
        "<Enter>", on_enter_button
    ).bind(
        "<Leave>", on_leave_button
    )

def create_gui():
    """
    Creates the main GUI window and its widgets for the image to PDF converter.
    """
    global root, file_list, save_path, file_name, image_files

    root = tk.Tk()
    root.title("Image to PDF Converter")
    
    # Initialize compression threshold
    compression_threshold = tk.DoubleVar(value=10)  # Default is 10 MB

    # Set the window icon
    logo_image_path = resource_path("logo.png")
    logo_image = tk.PhotoImage(file=logo_image_path)
    root.iconphoto(True, logo_image)

    # Create menu bar
    menu_bar = tk.Menu(root)

    # File menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Settings", command=lambda: open_settings(compression_threshold))
    file_menu.add_command(label="Exit", command=root.destroy)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Help menu
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Help", command=show_help)
    help_menu.add_command(label="About", command=show_about)
    menu_bar.add_cascade(label="Help", menu=help_menu)

    # Add menu bar to the window
    root.config(menu=menu_bar)

    # Calculate the center position of the window
    window_width = 500  # Width of the main window
    window_height = 400  # Height of the main window

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))

    # Set the geometry of the window to center it on the screen
    root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

    # Ensure the window resizes according to the frame size
    root.pack_propagate(False)

    image_files = []

    default_save_location = os.path.expanduser("~\\Documents")

    frame = tk.Frame(root)
    frame.pack(padx=5, pady=5)

    # Button to select images
    select_images_button = tk.Button(frame, text="Select Images", command=open_files,
                                     bg="blue", fg="white")
    select_images_button.grid(row=1, column=0, padx=5, pady=5)

    # Listbox to display selected images
    file_list = tk.Listbox(frame, height=5, width=50)
    file_list.grid(row=1, column=1, padx=5, pady=5)

    # Button to select save location
    save_path = tk.StringVar(value=default_save_location)
    save_location_button = tk.Button(frame, text="Save Location", command=select_save_location,
                                     bg="blue", fg="white")
    save_location_button.grid(row=2, column=0, padx=5, pady=5)

    # Entry to display selected save location
    save_location_entry = tk.Entry(frame, textvariable=save_path, width=50)
    save_location_entry.grid(row=2, column=1, padx=5, pady=5)

    # Entry for the file name
    file_name = tk.StringVar()
    file_name_label = tk.Label(frame, text="File Name:")
    file_name_label.grid(row=3, column=0, padx=5, pady=5)
    file_name_entry = tk.Entry(frame, textvariable=file_name, width=50)
    file_name_entry.grid(row=3, column=1, padx=5, pady=5)

    # Checkbox for zip option
    zip_option = tk.BooleanVar()
    zip_checkbox = tk.Checkbutton(frame, text="Zip the PDF file after conversion", variable=zip_option)
    zip_checkbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # Progress bar
    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate", variable=progress_var)
    progress_bar.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    # Button to start the conversion
    convert_button = tk.Button(frame, text="Convert", command=lambda: convert_files(zip_option, progress_var, compression_threshold),
                               bg="green", fg="white", width=55)
    convert_button.grid(row=6, column=0, columnspan=3, padx=5, pady=10)

    # Button to close the application
    close_button = tk.Button(frame, text="Close", command=root.destroy,
                             width=10, bg="red", fg="white")
    close_button.grid(row=7, column=0, columnspan=3, padx=5, pady=10)

    # Add hover effects
    select_images_button.bind("<Enter>", on_enter_button)
    select_images_button.bind("<Leave>", on_leave_button)
    save_location_button.bind("<Enter>", on_enter_button)
    save_location_button.bind("<Leave>", on_leave_button)
    convert_button.bind("<Enter>", on_enter_button_convert)
    convert_button.bind("<Leave>", on_leave_button_convert)
    close_button.bind("<Enter>", on_enter_button_close)
    close_button.bind("<Leave>", on_leave_button_close)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
