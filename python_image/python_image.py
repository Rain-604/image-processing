from PIL import Image
import numpy as np
import glob
import os

def rle_encode(data):
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

# Get the current directory and find all JPG files
folder_path = os.getcwd()
jpg_files = glob.glob(os.path.join(folder_path, '*.jpg'))


# Check if any JPG files found
if not jpg_files:
    raise FileNotFoundError("No .jpg files found in the current directory.")

# Load the first JPG image
image_path = jpg_files[0]
image = Image.open(image_path)

# Resize to manageable size
image.thumbnail((500, 500))

# Convert to greyscale
image = image.convert("L")

# Convert to numpy array
imageArr = np.array(image)

# Get image dimensions
height, width = imageArr.shape
print("Height:", height)
print("Width:", width)

def floyd_steinberg_dither(image):
    img = np.array(image.convert("L"), dtype=np.float32)  # Convert to grayscale
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

image = floyd_steinberg_dither(image)

# Convert dithered image to array
imageArr = np.array(image)
# Reduce greyscale levels to 4
quantised_image = np.floor(imageArr / 64).astype(np.uint8)

# Flatten image into 1D array
pixels = quantised_image.flatten()

# Apply RLE
compressed_data = rle_encode(pixels)

# Save to file
with open("output1.txt", "w") as file:
    file.write(f"{width} {height} 4\n")
    for value, count in compressed_data:
        file.write(f"{value} {count}\n")

print("Conversion complete! Output saved to 'output.txt'.")
