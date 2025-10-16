import os
from PIL import Image

def convert_jpg_to_png(input_file_path, output_file_path=None):
    """
    Converts a JPG image to a PNG image using the Pillow library.

    Args:
        input_file_path (str): The path to the input .jpg or .jpeg file.
        output_file_path (str, optional): The path for the output .png file. 
                                         If None, it saves in the same directory 
                                         with '_converted.png' appended to the name.
    """
    try:
        # 1. Open the image
        img = Image.open(input_file_path)
        
        # 2. Determine the output path if not specified
        if output_file_path is None:
            # Create a default output filename (e.g., 'photo.jpg' -> 'photo_converted.png')
            base_name, _ = os.path.splitext(input_file_path)
            output_file_path = f"{base_name}_converted.png"

        # 3. Save the image in PNG format
        # Pillow automatically handles the format conversion based on the file extension.
        img.save(output_file_path, 'png')

        print(f"Successfully converted '{input_file_path}' to '{output_file_path}'")

    except FileNotFoundError:
        print(f"Error: The input file was not found at '{input_file_path}'")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")

# --- Example Usage ---
# NOTE: Replace 'your_input_file.jpg' with the actual path to your JPEG file.
# Make sure the file exists in the same directory as this script, or provide the full path.

# To run this script:
# 1. Install Pillow: pip install Pillow
# 2. Make sure you have a file named 'example.jpg'
# 3. Uncomment and run the function call below:

# convert_jpg_to_png('example.jpg')

# Or specify a different output name:
# convert_jpg_to_png('another_image.jpeg', 'output_folder/my_new_image.png')

# Example using a placeholder path for demonstration:
print("\n--- Demonstration (replace with your actual file path) ---\n")
convert_jpg_to_png('resources/image.jpg', 'resources/input.png')
print("\n--- End of Demonstration ---")
