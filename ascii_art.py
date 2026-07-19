from PIL import Image
from io import BytesIO
from urllib.request import urlopen
import ssl, certifi

# Need to get PIL with this command: pip install pillow

# ASCII characters from dark to light
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def resize_image(image, new_width=85):
    """
    Resize image based on ascii character height-to-width ratio (Courier New 8pt)
    """
    width, height = image.size
    char_ratio = 2.0
    new_height = int((height / width) * new_width / char_ratio)
    return image.resize((new_width, new_height))

def rgb_to_gray(image):
    """
    Convert image to grayscale.
    """
    return image.convert("L")   # RGB color to luminance

def pixels_to_ascii(image):
    """
    Map grayscale pixels to ASCII characters.
    """
    ascii_chars = []
    BUCKET_SIZE = 25  # 256 / 10 ≈ 25

    pixels = image.getdata()
    for gray_value in pixels:
        ascii_chars.append(ASCII_CHARS[gray_value // BUCKET_SIZE])
    empty_separator = ""
    ascii_str = empty_separator.join(ascii_chars)

    return ascii_str

def build_ascii_image(ascii_str, new_width):
    """
    Break up a long ascii string into rows of specified width
    """
    pixel_count = len(ascii_str)
    lines = []
    # break up into multiple lines
    for i in range(0, pixel_count, new_width):
        lines.append(ascii_str[i:i+new_width])

    # join each line with the newline character
    newline_separator = "\n"
    return newline_separator.join(lines)

def read_image(path):
    """
    Read in an image from a file or a url path.
    """
    try:
        if path.startswith("http"):
            # Setup ssl context to use certifi's CA bundle, potentially more forgiving
            ctx = ssl.create_default_context(cafile=certifi.where())
            # read from the web
            with urlopen(path, context=ctx) as image_stream:
                image = Image.open(BytesIO(image_stream.read()))
        else:
            # read from a file
            image = Image.open(path)
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    return image

def image_to_ascii(path, new_width, output_file):
    """
    Convert image to ASCII art and save to file.
    """
    image = read_image(path)
    image = resize_image(image, new_width)
    image = rgb_to_gray(image)
    ascii_str = pixels_to_ascii(image)
    ascii_image = build_ascii_image(ascii_str, new_width)

    # Print to console
    print(ascii_image)

    # Save to file too
    with open(output_file, "w") as file:
        file.write(ascii_image)

# 🔧 Example usage
if __name__ == "__main__":
    # Replace with your image file or web url
    image_path = "https://static.wikia.nocookie.net/demon-slayer-opinion/images/3/3c/Tanjiro_Kamado_Full_Body_29.webp"

    image_to_ascii(image_path, new_width=80, output_file="ascii_output.txt")