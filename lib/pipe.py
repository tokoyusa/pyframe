from lib.frame_processor import extract_significant_frames
from lib.rekognition_moderator import RekognitionModerator
from lib.video_converter import video_to_gif
import os
from PIL import Image
import math


def merge_images_to_grid(image_paths: list, output_path: str, images_per_row: int = 2, target_size: int = 2560):
    if not image_paths:
        raise ValueError("No images to merge")
    
    images = [Image.open(path).convert('RGB') for path in image_paths]
    
    # Resize all images to target size while maintaining aspect ratio
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


class Pipe:
    def __init__(self, input_path: str, max_frames: int = 5, region_name: str = 'us-east-1', min_confidence: float = 80.0, use_merged: bool = False, frames_per_batch: int = 2):
        self.input_path = input_path
        self.max_frames = max_frames
        self.region_name = region_name
        self.min_confidence = min_confidence
        self.use_merged = use_merged
        self.frames_per_batch = frames_per_batch
        
    def run(self):
        file_ext = os.path.splitext(self.input_path)[1].lower()
        
        if file_ext == '.gif':
            print(f"Processing GIF: {self.input_path}")
            extract_significant_frames(self.input_path, max_frames=self.max_frames)
            
            gif_name = os.path.splitext(os.path.basename(self.input_path))[0]
            compressed_folder = f'content/compressed_gifs/{gif_name}'
            
            if self.use_merged:
                image_files = sorted([
                    os.path.join(compressed_folder, f) 
                    for f in os.listdir(compressed_folder) 
                    if f.lower().endswith(('.jpg', '.jpeg', '.png'))
                ])
                
                if not image_files:
                    print("No images found to merge")
                    return []
                self.frames_per_batch
                frames_per_merge = 2
                all_results = []
                moderator = RekognitionModerator(region_name=self.region_name)
                
                for i in range(0, len(image_files), frames_per_merge):
                    batch = image_files[i:i + frames_per_merge]
                    batch_num = (i // frames_per_merge) + 1
                    merged_path = f'content/merged_images/{gif_name}_merged_{batch_num}.jpg'
                    
                    print(f"Merging batch {batch_num} ({len(batch)} images)...")
                    merge_images_to_grid(batch, merged_path)
                    
                    print(f"Moderating merged image: {merged_path}")
                    result = moderator.moderate_image(merged_path, min_confidence=self.min_confidence)
                    
                    labels = result['moderation_labels']
                    if labels:
                        print(f"Found {len(labels)} label(s):")
                        for label in labels:
                            print(f"   - {label['Name']} ({label['Confidence']:.2f}%)")
                    else:
                        print("Clean")
                    
                    all_results.append(result)
                
                return all_results
            else:
                moderator = RekognitionModerator(region_name=self.region_name)
                results = moderator.moderate_folder(compressed_folder, min_confidence=self.min_confidence)
                return results
            
        elif file_ext in ['.png', '.jpg', '.jpeg']:
            print(f"Processing image: {self.input_path}")
            moderator = RekognitionModerator(region_name=self.region_name)
            result = moderator.moderate_image(self.input_path, min_confidence=self.min_confidence)
            
            labels = result['moderation_labels']
            if labels:
                print(f"Found {len(labels)} label(s):")
                for label in labels:
                    print(f"   - {label['Name']} ({label['Confidence']:.2f}%)")
            else:
                print("Clean")
            
            return [result]
        
        else:
            raise ValueError(f"Unsupported file type: {file_ext}. Use .gif, .png, .jpg, or .jpeg")
