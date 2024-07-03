import os
import tkinter as tk
from tkinter import filedialog, messagebox
from rembg import remove
from PIL import Image, ImageDraw, ImageFont

def resize_images(input_directory, output_directory, size):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(input_directory, filename)
            with Image.open(img_path) as img:
                resized_img = img.resize(size, Image.Resampling.LANCZOS)
                resized_img.save(os.path.join(output_directory, filename))

    print(f"All images resized to {size} and saved to {output_directory}.")

def remove_background(input_image_path, background_color=(255, 255, 255)):
    try:
        input_image = Image.open(input_image_path)
        output_image = remove(input_image)
        white_background = Image.new('RGB', output_image.size, background_color)
        white_background.paste(output_image, (0, 0), output_image)
        return white_background
    except Exception as e:
        print(f"Error processing {input_image_path}: {e}")
        return None

def add_text_to_image(image, text, text_position=(10, 10), text_color=(0, 0, 0), font_size=20):
    try:
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            print("TTF font not found. Using default font.")
            font = ImageFont.load_default()
        draw.text(text_position, text, fill=text_color, font=font)
        return image
    except Exception as e:
        print(f"Error adding text to image: {e}")
        return image

def add_logo_to_image(image, logo_path, logo_position=(0, 0)):
    try:
        logo = Image.open(logo_path).convert("RGBA")
        logo_size = (170, 170)
        logo.thumbnail(logo_size, Image.Resampling.LANCZOS)
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        image.paste(logo, logo_position, logo)
        return image
    except Exception as e:
        print(f"Error adding logo to image: {e}")
        return image

def process_and_save_images(image_paths, output_dir, base_text, logo_path, text_position=(10, 10), text_color=(0, 0, 0), font_size=20):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    counter = 25
    
    for image_path in image_paths:
        try:
            image = remove_background(image_path)
            if image is not None:
                image_filename = os.path.basename(image_path)
                text = f"{base_text}{counter} SIZE-10X14 CODE-BGN"
                counter += 1
                image = add_text_to_image(image, text, text_position, text_color, font_size)
                image = add_logo_to_image(image, logo_path)
                output_image_path = os.path.join(output_dir, image_filename)
                image.save(output_image_path)
                print(f"Processed image saved to {output_image_path}")
            else:
                print(f"Skipping image {image_path} due to processing error.")
        except Exception as e:
            print(f"Error processing {image_path}: {e}")

def select_input_directory():
    input_dir = filedialog.askdirectory()
    input_dir_entry.delete(0, tk.END)
    input_dir_entry.insert(0, input_dir)

def select_output_directory():
    output_dir = filedialog.askdirectory()
    output_dir_entry.delete(0, tk.END)
    output_dir_entry.insert(0, output_dir)

def select_logo_file():
    logo_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    logo_path_entry.delete(0, tk.END)
    logo_path_entry.insert(0, logo_path)

def start_processing():
    input_dir = input_dir_entry.get()
    output_dir = output_dir_entry.get()
    logo_path = logo_path_entry.get()
    target_size = (1280, 960)  # Example size, you can make this dynamic by adding more GUI elements
    base_text = "A4P-"
    text_pos = (250, 800)
    text_col = (0, 0, 0)
    font_size = 50

    if not input_dir or not output_dir or not logo_path:
        messagebox.showwarning("Input Error", "Please select all necessary paths.")
        return

    resize_images(input_dir, output_dir, target_size)
    
    image_paths = [os.path.join(output_dir, filename) for filename in os.listdir(output_dir) if filename.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    process_and_save_images(image_paths, output_dir, base_text, logo_path, text_position=text_pos, text_color=text_col, font_size=font_size)
    messagebox.showinfo("Processing Complete", f"All images processed and saved to {output_dir}")

# GUI setup
root = tk.Tk()
root.title("Image Processing App")

# Input directory selection
tk.Label(root, text="Input Directory:").grid(row=0, column=0, padx=5, pady=5)
input_dir_entry = tk.Entry(root, width=50)
input_dir_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=select_input_directory).grid(row=0, column=2, padx=5, pady=5)

# Output directory selection
tk.Label(root, text="Output Directory:").grid(row=1, column=0, padx=5, pady=5)
output_dir_entry = tk.Entry(root, width=50)
output_dir_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=select_output_directory).grid(row=1, column=2, padx=5, pady=5)

# Logo file selection
tk.Label(root, text="Logo File:").grid(row=2, column=0, padx=5, pady=5)
logo_path_entry = tk.Entry(root, width=50)
logo_path_entry.grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=select_logo_file).grid(row=2, column=2, padx=5, pady=5)

# Start processing button
tk.Button(root, text="Start Processing", command=start_processing).grid(row=3, column=0, columnspan=3, pady=20)

root.mainloop()
