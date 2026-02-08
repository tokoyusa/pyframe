import cv2
import numpy as np
import os
import shutil
from lib.error_handler import validate_file_exists, ProcessingError

def extract_significant_frames(gif_path, max_frames=10):
    validate_file_exists(gif_path)
    
    gif_name = os.path.splitext(os.path.basename(gif_path))[0]
    output_folder = os.path.join(os.path.dirname(__file__), '../content/compressed_gifs', gif_name)
    
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    cap = cv2.VideoCapture(gif_path)
    if not cap.isOpened():
        raise ProcessingError(f"Could not open {gif_path}")

    frames_buffer = []
    prev_gray = None
    frame_index = 0

    print(f"Processing: {gif_path}")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        small = cv2.resize(frame, (64, 64))
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

        if prev_gray is None:
            score = 0.0
        else:
            diff = cv2.absdiff(gray, prev_gray)
            score = np.sum(diff)

        frames_buffer.append({
            'id': frame_index,
            'score': score,
            'image': frame.copy()
        })

        prev_gray = gray
        frame_index += 1

    cap.release()

    total_frames = len(frames_buffer)
    if total_frames == 0:
        return []

    selected_frames = []
    
    if total_frames <= max_frames:
        selected_frames = frames_buffer
    else:
        chunk_size = total_frames / max_frames

        for i in range(max_frames):
            start_idx = int(i * chunk_size)
            end_idx = int((i + 1) * chunk_size)
        
            if i == max_frames - 1:
                end_idx = total_frames
            bucket_frames = frames_buffer[start_idx:end_idx]
            
            if bucket_frames:
                best_in_bucket = max(bucket_frames, key=lambda x: x['score'])
                selected_frames.append(best_in_bucket)

    print(f"Exporting {len(selected_frames)} frames to {output_folder}")
    saved_paths = []

    for i, item in enumerate(selected_frames):
        filename = f"{i:02d}_frame_{item['id']:03d}_score_{int(item['score'])}.jpg"
        save_path = os.path.join(output_folder, filename)
        cv2.imwrite(save_path, item['image'])
        saved_paths.append(save_path)

    print(f"Saved {len(selected_frames)} frames")
    return saved_paths