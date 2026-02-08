from PIL import Image
import os
import math


def merge_images_to_grid(image_paths: list, output_path: str, images_per_row: int = 2, target_size: int = 2560):
    if not image_paths:
        raise ValueError("No images to merge")

    images = [Image.open(path).convert('RGB') for path in image_paths]
    
    resized_images = []
    for img in images:
        img.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)
        resized_images.append(img)

    widths, heights = zip(*(img.size for img in resized_images))
    max_width = max(widths)
    max_height = max(heights)

    num_images = len(resized_images)
    num_rows = math.ceil(num_images / images_per_row)

    grid_width = images_per_row * max_width
    grid_height = num_rows * max_height

    grid_image = Image.new('RGB', (grid_width, grid_height), color='black')

    for idx, img in enumerate(resized_images):
        row = idx // images_per_row
        col = idx % images_per_row
        x = col * max_width
        y = row * max_height
        grid_image.paste(img, (x, y))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    grid_image.save(output_path, quality=95)

    for img in images + resized_images:
        img.close()

    return output_path
