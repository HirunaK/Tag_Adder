from PIL import Image
import pillow_heif  # Enables HEIC support in Pillow
import os

# Function to convert HEIC to PNG (if needed)
def convert_heic_to_png(heic_path, output_folder):
    heif_image = pillow_heif.open_heif(heic_path)  # Open HEIC image
    image = Image.frombytes(
        heif_image.mode, heif_image.size, heif_image.data, "raw", heif_image.mode, 0, 1
    )
    
    # Save as PNG to preserve quality
    png_path = os.path.join(output_folder, os.path.splitext(os.path.basename(heic_path))[0] + ".png")
    image.save(png_path, format="PNG")
    print(f"Converted HEIC to PNG: {png_path}")
    return png_path  # Return path of converted image

# Function to overlay a scaled PNG tag onto an image
def add_scaled_png_tag(image_path, tag_path, distance_from_bottom, output_folder):
    # Open image (converted to PNG if necessary)
    image = Image.open(image_path).convert("RGBA")
    img_width, img_height = image.size

    # Open tag image (PNG)
    tag = Image.open(tag_path).convert("RGBA")

    # Scale tag width to match the image width while keeping aspect ratio
    tag_aspect_ratio = tag.height / tag.width
    new_tag_width = img_width  # Make tag the same width as the photo
    new_tag_height = int(new_tag_width * tag_aspect_ratio)

    # Resize using LANCZOS
    tag = tag.resize((new_tag_width, new_tag_height), Image.LANCZOS)

    # Position the tag at the bottom
    x_position = 0  # Left-aligned since width matches image
    y_position = img_height - distance_from_bottom - new_tag_height

    # Ensure the tag does not go out of bounds
    if y_position < 0:
        y_position = 0  

    # Paste the tag onto the image
    image.paste(tag, (x_position, y_position), tag)

    # Save final image
    output_path = os.path.join(output_folder, os.path.basename(image_path))
    image.save(output_path, format="PNG")
    print(f"Saved: {output_path}")

# Folder containing JPG images
image_directory = r"FileLocation\Folder"
# Path to the PNG tag
tag_image_path = r"FileLocation\file.png"
# Output folder for processed images
output_folder = r"FileLocation\Folder"
os.makedirs(output_folder, exist_ok=True)

# Distance from the bottom (in pixels)
distance_from_bottom = 50

# Process each image in the directory
for filename in os.listdir(image_directory):
    if filename.lower().endswith((".jpg", ".jpeg", ".png", ".heic")):
        image_path = os.path.join(image_directory, filename)

        # Convert HEIC files to PNG before processing
        if filename.lower().endswith(".heic"):
            image_path = convert_heic_to_png(image_path, output_folder)

        add_scaled_png_tag(image_path, tag_image_path, distance_from_bottom, output_folder)

print("All images processed successfully.")
