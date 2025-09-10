import glob
import os

# Map grayscale levels to ASCII characters
pattern = ['#', ':', '.', ' ']

def decode(img, pos, level, length):
    """Fill 'length' pixels starting at 'pos' in the 1D img array with the character for 'level'."""
    cc = pattern[level]
    for i in range(length):
        img[pos + i] = cc

def decode_rle_file(file_path):
    """Decode a single RLE file into an ASCII image."""
    with open(file_path, 'r') as f:
        # Read width, height, grey levels
        first_line = f.readline()
        width, height, grey_levels = map(int, first_line.split())

        total_pixels = width * height
        img = [' '] * total_pixels

        pos = 0
        # Read RLE data
        for line in f:
            level, length = map(int, line.split())
            decode(img, pos, level, length)
            pos += length

        # Build the 2D image as a list of strings
        ascii_image = [''.join(img[i*width : (i+1)*width]) for i in range(height)]
        return ascii_image

def main():
    # Set folder path containing RLE text files
    folder_path = os.getcwd()  # or specify a folder: r"C:\path\to\folder"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))

    if not txt_files:
        print(f"No .txt files found in {folder_path}")
        return
    
    output_folder = os.path.join(folder_path, "decoded_output")
    os.makedirs(output_folder, exist_ok=True)
    
    for file_path in txt_files:
        ascii_image = decode_rle_file(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file = os.path.join(output_folder, f"{base_name}_decoded.txt")

        with open(output_file, 'w') as f:
            for row in ascii_image:
                f.write(row + '\n')

        print(f"Decoded '{file_path}' → '{output_file}'")

if __name__ == "__main__":
    main()
