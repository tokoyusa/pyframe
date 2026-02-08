from PIL import Image
from transformers import pipeline
import os
from typing import List, Dict, Any
from lib.error_handler import validate_folder


class NSFWDetector:

    def __init__(self, model: str = "AdamCodd/vit-base-nsfw-detector"):
        self.classifier = pipeline("image-classification", model=model)

    def classify_image(self, image_path: str) -> Dict[str, Any]:
        img = Image.open(image_path).convert('RGB')
        results = self.classifier(img)
        img.close()

        nsfw_score = 0.0
        normal_score = 0.0
        for r in results:
            if r['label'] == 'nsfw':
                nsfw_score = r['score'] * 100
            elif r['label'] == 'normal':
                normal_score = r['score'] * 100

        return {
            'image_path': image_path,
            'is_nsfw': nsfw_score > normal_score,
            'nsfw_score': nsfw_score,
            'normal_score': normal_score,
            'raw_results': results
        }

    def classify_folder(self, folder_path: str) -> List[Dict[str, Any]]:
        validate_folder(folder_path)
        results = []

        image_files = sorted([f for f in os.listdir(folder_path)
                              if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

        print(f"\nClassifying {len(image_files)} images in {folder_path}...")

        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            try:
                result = self.classify_image(image_path)
                results.append(result)

                if result['is_nsfw']:
                    print(f"{image_file}: NSFW ({result['nsfw_score']:.2f}%)")
                else:
                    print(f"{image_file}: Clean ({result['normal_score']:.2f}%)")

            except Exception as e:
                print(f"Error processing {image_file}: {str(e)}")

        return results
