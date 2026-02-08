import boto3
import os
from typing import List, Dict, Any
from lib.error_handler import validate_folder


class RekognitionModerator:
    
    def __init__(self, region_name: str = 'us-east-1'):
        self.client = boto3.client('rekognition', region_name=region_name)
    
    def moderate_image(self, image_path: str, min_confidence: float = 50.0) -> Dict[str, Any]:
        with open(image_path, 'rb') as image_file:
            image_bytes = image_file.read()
        
        response = self.client.detect_moderation_labels(
            Image={'Bytes': image_bytes},
            MinConfidence=min_confidence
        )
        
        return {
            'image_path': image_path,
            'moderation_labels': response.get('ModerationLabels', []),
            'moderation_model_version': response.get('ModerationModelVersion', 'N/A')
        }
    
    def moderate_folder(self, folder_path: str, min_confidence: float = 50.0) -> List[Dict[str, Any]]:
        validate_folder(folder_path)
        results = []
        
        image_files = [f for f in os.listdir(folder_path) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        print(f"\nModerating {len(image_files)} images in {folder_path}...")
        
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            try:
                result = self.moderate_image(image_path, min_confidence)
                results.append(result)
                
                labels = result['moderation_labels']
                if labels:
                    print(f"{image_file}: {len(labels)} label(s)")
                    for label in labels:
                        print(f"   - {label['Name']} ({label['Confidence']:.2f}%)")
                else:
                    print(f"{image_file}: Clean")
                    
            except Exception as e:
                print(f"Error processing {image_file}: {str(e)}")
        
        return results
    
    def moderate_compressed_gifs(self, compressed_gifs_root: str = 'content/compressed_gifs', 
                                 min_confidence: float = 50.0) -> Dict[str, List[Dict[str, Any]]]:
        validate_folder(compressed_gifs_root)
        all_results = {}
        
        gif_folders = [d for d in os.listdir(compressed_gifs_root) 
                      if os.path.isdir(os.path.join(compressed_gifs_root, d))]
        
        print(f"Found {len(gif_folders)} folders")
        
        for gif_name in gif_folders:
            folder_path = os.path.join(compressed_gifs_root, gif_name)
            print(f"\n{'='*60}")
            print(f"Processing: {gif_name}")
            print(f"{'='*60}")
            
            results = self.moderate_folder(folder_path, min_confidence)
            all_results[gif_name] = results
        
        return all_results
