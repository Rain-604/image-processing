from PIL import Image
import numpy as np
import glob
import os

def rle_encode(data):
    """Run-Length Encode a 1D array"""
    encoded = []
    prev_pixel = data[0]
    count = 1

    for pixel in data[1:]:
        if pixel == prev_pixel:
            count += 1
        else:
            encoded.append((prev_pixel, count))
            prev_pixel = pixel
            count = 1
    encoded.append((prev_pixel, count))
    return encoded

def floyd_steinberg_dither(image):
    """Apply Floyd–Steinberg dithering"""
    img = np.array(image.convert("L"), dtype=np.float32)
    height, width = img.shape

    for y in range(height):
        for x in range(width):
            old_pixel = img[y, x]
            new_pixel = 255 if old_pixel > 127 else 0
            img[y, x] = new_pixel
            error = old_pixel - new_pixel

            if x + 1 < width:
                img[y, x + 1] += error * 7 / 16
            if y + 1 < height:
                if x > 0:
                    img[y + 1, x - 1] += error * 3 / 16
                img[y + 1, x] += error * 5 / 16
                if x + 1 < width:
                    img[y + 1, x + 1] += error * 1 / 16

    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))

# Get all JPG files in the current folder
folder_path = os.getcwd()
jpg_files = glob.glob(os.path.join(folder_path, '*.jpg'))

print("Current working directory:", folder_path)


if not jpg_files:
    raise FileNotFoundError("No .jpg files found in the current directory.")

# Process each JPG file
for image_path in jpg_files:
    # Load image
    image = Image.open(image_path)
    image.thumbnail((500, 500))  # Resize
    image = image.convert("L")   # Grayscale

    # Apply dithering
    image = floyd_steinberg_dither(image)

    # Convert to numpy array and quantize to 4 levels
    imageArr = np.array(image)
    quantised_image = np.floor(imageArr / 64).astype(np.uint8)

    # Flatten and encode
    pixels = quantised_image.flatten()
    compressed_data = rle_encode(pixels)

    # Save RLE to file with same base filename
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_file = f"{base_name}.txt"
    height, width = quantised_image.shape
    with open(output_file, "w") as file:
        file.write(f"{width} {height} 4\n")
        for value, count in compressed_data:
            file.write(f"{value} {count}\n")

    print(f"Processed '{image_path}' → '{output_file}'")

print("All images processed successfully!")
