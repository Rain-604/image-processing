# Image Processing - RLE Compression & ASCII Art

A Python-based image processing tool that compresses images using Run-Length Encoding (RLE) and converts them into ASCII art. The program includes both encoding and decoding capabilities.

## Features

- **Image Compression**: Convert JPG images to compressed RLE format
- **Image Dithering**: Apply Floyd-Steinberg dithering for better visual quality
- **Grayscale Quantization**: Reduce images to 4 grayscale levels for compression
- **ASCII Art Generation**: Decode compressed images into ASCII art
- **Batch Processing**: Process multiple image files at once

## Project Structure

```
image-processing-main/
├── python_image/
│   └── python_image.py          # Single image encoding (basic version)
├── python_image_processing/
│   ├── python_image.py           # Batch image encoder
│   ├── run_length_decoding.py    # RLE decoder
│   ├── DSC05557.txt              # Encoded image data
│   ├── DSC08918.txt              # Encoded image data
│   └── decoded_output/           # Output folder for decoded ASCII art
│       ├── DSC05557_decoded.txt
│       └── DSC08918_decoded.txt
└── README.md
```

## How It Works

### Encoding Process (python_image.py)
1. Loads JPG images from the current directory
2. Resizes images to 500×500 pixels
3. Converts to grayscale
4. Applies Floyd-Steinberg dithering for better visual representation
5. Quantizes to 4 grayscale levels (0-3)
6. Applies Run-Length Encoding compression
7. Saves compressed data to `.txt` files

**Output Format:**
```
width height num_levels
level count
level count
...
```

### Decoding Process (run_length_decoding.py)
1. Reads RLE-encoded text files
2. Maps grayscale levels to ASCII characters:
   - Level 0 → `#` (darkest)
   - Level 1 → `:` 
   - Level 2 → `.`
   - Level 3 → ` ` (lightest)
3. Reconstructs the image as ASCII art
4. Saves output to `decoded_output/` folder

## Usage

### Encoding Images to RLE Format

1. Place JPG images in the `python_image_processing/` folder
2. Run the encoder:
   ```bash
   cd python_image_processing
   python python_image.py
   ```
3. Encoded files will be saved as `.txt` files in the same directory

### Decoding RLE to ASCII Art

1. Ensure encoded `.txt` files are in the `python_image_processing/` folder
2. Run the decoder:
   ```bash
   cd python_image_processing
   python run_length_decoding.py
   ```
3. Decoded ASCII art will appear in the `decoded_output/` folder

## Requirements

- Python 3.x
- Pillow (PIL)
- NumPy

### Installation

```bash
pip install Pillow numpy
```

## Examples

**Input:** JPG image
```
DSC05557.jpg (original photo)
```

**Encoded Output:** RLE text format
```
500 375 4
3 1500
2 245
1 432
0 18
...
```

**Decoded Output:** ASCII art
```
###########...:::###
#####..  ##::## ##
##   ::  :::##  ##
...
```

## Technologies Used

- **Floyd-Steinberg Dithering**: Advanced image dithering algorithm for better visual quality
- **Run-Length Encoding**: Lossless compression technique
- **ASCII Art**: Visual representation of images using text characters

## Best Practices

- Use clear, well-lit JPG images for best results
- Images will be automatically resized to 500×500 pixels
- The 4-level grayscale quantization provides good compression while maintaining visibility
- For high-quality results, ensure input images have good contrast

## License

Open for educational and personal use.
