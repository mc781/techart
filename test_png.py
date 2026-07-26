from PIL import Image
from PIL import Image, ImageChops

def subtract_images(img1_path, img2_path, out_path):
    img1 = Image.open(img1_path).convert("RGBA")
    img2 = Image.open(img2_path).convert("RGBA")

    result = ImageChops.subtract(img1, img2)
    result.save(out_path)

subtract_images("player.png", "player_bg.png", "me2.png")

exit()

img = Image.open("cat_icon.png")

print("Mode:", img.mode)

# Convert to RGBA to inspect transparency
rgba = img.convert("RGBA")
alpha = rgba.getchannel("A")
alpha_values = list(alpha.getdata())

if min(alpha_values) == 0:
    print("PNG has fully transparent pixels.")
elif min(alpha_values) < 255:
    print("PNG has partial transparency.")
else:
    print("PNG has NO transparent pixels.")
