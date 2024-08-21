from PIL import Image
import os

# Define the path to the PNG images
input_folder = os.path.join("..", "assets", "wheelbearing_images_LSODS")

# Create an output folder for the JPG files
output_folder = os.path.join(input_folder, "jpg_files")
os.makedirs(output_folder, exist_ok=True)

# Loop through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".png"):
        # Open an image file
        with Image.open(os.path.join(input_folder, filename)) as img:
            # Convert the image to RGB (PNG can be RGBA)
            rgb_img = img.convert("RGB")

            # Save the image as JPG
            jpg_filename = os.path.splitext(filename)[0] + ".jpg"
            rgb_img.save(os.path.join(output_folder, jpg_filename), "JPEG")

print(f"All PNG files have been converted to JPG and saved in {output_folder}")
