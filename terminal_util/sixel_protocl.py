from PIL import Image
import sixel

def image_to_sixel(image_path, width=300):
    img = Image.open(image_path)
    img.thumbnail((width, width))
    sixel_data = sixel.from_image(img)
    return sixel_data

def encode_sixel(image_path, width=300):
    return f'\ePq{image_to_sixel(image_path, width)}\033\\'