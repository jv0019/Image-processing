import os
from PIL import Image

def resize_images(input_directory, output_directory, size):
    """
    Resize all images in the input_directory to the specified size and save them to the output_directory.
    
    :param input_directory: Directory containing the images to resize.
    :param output_directory: Directory to save the resized images.
    :param size: Tuple indicating the size (width, height) to resize the images to.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(input_directory, filename)
            with Image.open(img_path) as img:
                resized_img = img.resize(size, Image.Resampling.LANCZOS)
                resized_img.save(os.path.join(output_directory, filename))

    print(f"All images resized to {size} and saved to {output_directory}.")

if __name__ == "__main__":
    input_dir = r"C:\Users\hp\OneDrive\Desktop\samples"
    output_dir = r"C:\Users\hp\OneDrive\Desktop\resized_samples"
    target_size = (1280, 960)  # Replace with desired dimensions

    resize_images(input_dir, output_dir, target_size)
