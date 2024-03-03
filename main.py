from PIL import Image, ImageOps
import numpy as np
import os.path
import re

ASCII = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
ASCII_LIST = [*ASCII]
BRIGHTNESS = [0, 0.0751, 0.0829, 0.0848, 0.1227, 0.1403, 0.1559, 0.185, 0.2183, 0.2417, 0.2571, 0.2852, 0.2902, 0.2919, 0.3099, 0.3192, 0.3232, 0.3294, 0.3384, 0.3609, 0.3619, 0.3667, 0.3737, 0.3747, 0.3838, 0.3921, 0.396, 0.3984, 0.3993, 0.4075, 0.4091, 0.4101, 0.42, 0.423, 0.4247, 0.4274, 0.4293, 0.4328, 0.4382, 0.4385, 0.442, 0.4473, 0.4477, 0.4503, 0.4562, 0.458, 0.461, 0.4638, 0.4667, 0.4686, 0.4693, 0.4703, 0.4833, 0.4881, 0.4944, 0.4953, 0.4992, 0.5509, 0.5567, 0.5569, 0.5591, 0.5602, 0.5602, 0.565, 0.5776, 0.5777, 0.5818, 0.587, 0.5972, 0.5999, 0.6043, 0.6049, 0.6093, 0.6099, 0.6465, 0.6561, 0.6595, 0.6631, 0.6714, 0.6759, 0.6809, 0.6816, 0.6925, 0.7039, 0.7086, 0.7235, 0.7302, 0.7332, 0.7602, 0.7834, 0.8037, 0.9999]
BRIGHTNESS = [round(i * 255) for i in BRIGHTNESS]

# creates character ASCII mapping
ASCII_INTENSITY = {}
for i in range(len(ASCII_LIST)):
    ASCII_INTENSITY[BRIGHTNESS[i]] = ASCII_LIST[i]

# main method running program
def main():
    print("Hello! This program turns your .jpg images into ASCII images (image composed of many characters).")
    input("First save your .jpg image to this project folder. Press enter to continue.")
    imageInput = input("What is the image file's name (example: crazygojo.jpg):\n")
    if not os.path.isfile(f"./{imageInput}"):
        imageInput = input("That image file name might have been incorrect. Please try again.\n")
    imageWidth = input("What would you like the width to be (the smaller the width, the more devices the image will be viewable in - too large images ruin spacing):\n")
    asciiConvert(imageInput, int(imageWidth))

# convertes images to ascii
def asciiConvert(imageFile, max_width):
    # open, scale, grayscale the image file
    filename = imageFile
    with Image.open(filename) as img:
        if img.width > max_width:
            aspect_ratio = img.height / img.width
            new_height = int(aspect_ratio * max_width)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        img = ImageOps.grayscale(img)
        px = img.load()

    width, height = img.size

    # create 2d array of pixel's brightnesses
    imagePixels = []
    for i in range(height):
        pixelRow = []
        for j in range(width):
            pixelRow.append(px[j, i])
        imagePixels.append(pixelRow)
    
    imagePixels = np.array(imagePixels)

    # creates a 2d array with ASCII characters for each pixel
    imageAscii = []
    for i in imagePixels:
        asciiRow = []
        for j in i:
            closest_key = min(ASCII_INTENSITY.keys(), key=lambda k: abs(k - j))
            asciiRow.append(ASCII_INTENSITY[closest_key])
        imageAscii.append(asciiRow)
    imageAscii = np.array(imageAscii)

    # creates a new file and prints the ASCII character array
    imgName = re.sub(r'\.jpg', '', imageFile, flags=re.IGNORECASE)
    newFile = imgName + ".txt"
    with open(newFile, 'w') as f:
        for row in imageAscii:
            print("".join(row), file=f)

    return newFile

main()
