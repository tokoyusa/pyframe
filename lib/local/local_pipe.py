from lib.frame_processor import extract_significant_frames
from lib.local.local_detector import NSFWDetector
from lib.image_utils import merge_images_to_grid
import os


class LocalPipe:
    # Can also use: "Falconsai/nsfw_image_detection"
    def __init__(self, input_path: str, max_frames: int = 5, model: str = "AdamCodd/vit-base-nsfw-detector", use_merged: bool = False, frames_per_batch: int = 2):
        self.input_path = input_path
        self.max_frames = max_frames
        self.model = model
        self.use_merged = use_merged
        self.frames_per_batch = frames_per_batch

    def run(self):
        file_ext = os.path.splitext(self.input_path)[1].lower()

        detector = NSFWDetector(model=self.model)

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

                frames_per_merge = self.frames_per_batch
                all_results = []

                for i in range(0, len(image_files), frames_per_merge):
                    batch = image_files[i:i + frames_per_merge]
                    batch_num = (i // frames_per_merge) + 1
                    merged_path = f'content/merged_images/{gif_name}_merged_{batch_num}.jpg'

                    print(f"Merging batch {batch_num} ({len(batch)} images)...")
                    merge_images_to_grid(batch, merged_path)

                    print(f"Classifying merged image: {merged_path}")
                    result = detector.classify_image(merged_path)

                    if result['is_nsfw']:
                        print(f"NSFW ({result['nsfw_score']:.2f}%)")
                    else:
                        print(f"Clean ({result['normal_score']:.2f}%)")

                    all_results.append(result)

                return all_results
            else:
                results = detector.classify_folder(compressed_folder)
                return results

        elif file_ext in ['.png', '.jpg', '.jpeg']:
            print(f"Processing image: {self.input_path}")
            result = detector.classify_image(self.input_path)

            if result['is_nsfw']:
                print(f"NSFW ({result['nsfw_score']:.2f}%)")
            else:
                print(f"Clean ({result['normal_score']:.2f}%)")

            return [result]

        else:
            raise ValueError(f"Unsupported file type: {file_ext}. Use .gif, .png, .jpg, or .jpeg")
