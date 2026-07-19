from PIL import Image

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
