import os
from rembg import remove
from PIL import Image, ImageDraw, ImageFont

def remove_background(input_image_path, background_color=(255, 255, 255)):
    try:
        # Open the input image
        input_image = Image.open(input_image_path)
        
        # Remove the background
        output_image = remove(input_image)
        
        # Create a white background image
        white_background = Image.new('RGB', output_image.size, background_color)
        
        # Composite the output image onto the white background
        white_background.paste(output_image, (0, 0), output_image)
        
        return white_background
    except Exception as e:
        print(f"Error processing {input_image_path}: {e}")
        return None

def add_text_to_image(image, text, text_position=(10, 10), text_color=(0, 0, 0), font_size=20):
    try:
        draw = ImageDraw.Draw(image)
        # Attempt to load a TTF font
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            print("TTF font not found. Using default font.")
            font = ImageFont.load_default()
        
        # Draw the text on the image
        draw.text(text_position, text, fill=text_color, font=font)
        return image
    except Exception as e:
        print(f"Error adding text to image: {e}")
        return image

def add_logo_to_image(image, logo_path, logo_position=(0, 0)):
    try:
        # Open the logo image
        logo = Image.open(logo_path).convert("RGBA")
        
        # Resize logo if necessary
        logo_size = (170, 170)  # Example size, adjust as needed
        logo.thumbnail(logo_size, Image.Resampling.LANCZOS)
        
        # Ensure the logo has an alpha channel for transparency
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        
        # Create an alpha composite of the logo and the background image
        image.paste(logo, logo_position, logo)
        
        return image
    except Exception as e:
        print(f"Error adding logo to image: {e}")
        return image

def process_and_save_images(image_paths, output_dir, base_text, logo_path, text_position=(10, 10), text_color=(0, 0, 0), font_size=20):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    counter = 25  # Start the counter from 25
    
    for image_path in image_paths:
        try:
            # Remove the background
            image = remove_background(image_path)
            if image is not None:
                # Generate the text for the current image
                image_filename = os.path.basename(image_path)
                text = f"{base_text}{counter} SIZE-10X14 CODE-BGN"
                counter += 1  # Increment the counter for the next image
                
                # Add text to the image
                image = add_text_to_image(image, text, text_position, text_color, font_size)
                
                # Add logo to the image
                image = add_logo_to_image(image, logo_path)
                
                # Save the processed image
                output_image_path = os.path.join(output_dir, image_filename)
                image.save(output_image_path)
                print(f"Processed image saved to {output_image_path}")
            else:
                print(f"Skipping image {image_path} due to processing error.")
        except Exception as e:
            print(f"Error processing {image_path}: {e}")

if __name__ == "__main__":
    input_dir = r"C:\Users\hp\OneDrive\Desktop\resized_samples"  # Input directory path
    output_dir = r'C:\Users\hp\OneDrive\Desktop\editedimg'  # Output directory path
    logo_path = r'C:\Users\hp\OneDrive\Desktop\VIVON\VIVON logo _page-0001.jpg'  # Path to the logo image
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Base text for each image
    base_text = "A4P-"
    
    # Text parameters
    text_pos = (250, 800)  # Position of the text
    text_col = (0, 0, 0)  # Color of the text (black)
    font_size = 50  # Font size of the text
    
    # Gather all image paths
    image_paths = [os.path.join(input_dir, filename) for filename in os.listdir(input_dir) if filename.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    # Process and save each image individually with respective text
    process_and_save_images(image_paths, output_dir, base_text, logo_path, text_position=text_pos, text_color=text_col, font_size=font_size)
    print(f"All images processed and saved to {output_dir}")
