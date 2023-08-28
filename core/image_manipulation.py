from pathlib import Path
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from colorama import Fore


def resize_and_compress_image(image, max_size, quality, output):
    img = Image.open(image)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    width, height = img.size
    aspect_ratio = width / height

    if width > height:
        new_width = max_size
        new_height = int(max_size / aspect_ratio)
    else:
        new_height = max_size
        new_width = int(max_size * aspect_ratio)

    resized_image = img.resize((new_width, new_height), Image.LANCZOS)
    
    buffer = BytesIO()
    resized_image.save(buffer, 'WEBP', quality=quality)
    compressed_image = InMemoryUploadedFile(buffer, 'ImageField', f"{output}.webp", 'image/webp', len(buffer.getvalue()), None)
    return compressed_image
        

