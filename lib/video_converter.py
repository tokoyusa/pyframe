import os
from moviepy import VideoFileClip
from lib.error_handler import validate_file_exists, validate_folder


def video_to_gif(video_path, output_folder='content/gifs', fps=15, resize_width=None):
    validate_file_exists(video_path)
    validate_folder(output_folder, create=True)
    
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(output_folder, f"{video_name}.gif")
    
    print(f"Converting: {video_path}")
    
    clip = VideoFileClip(video_path)
    if resize_width:
        clip = clip.resize(width=resize_width)
    
    clip.write_gif(output_path, fps=fps)
    clip.close()
    
    print(f"Created: {output_path}")
    return output_path


def batch_video_to_gif(video_folder, output_folder='content/gifs', fps=15, resize_width=None):
    validate_folder(video_folder)
    validate_folder(output_folder, create=True)
    
    video_extensions = ('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm')
    video_files = [f for f in os.listdir(video_folder) 
                  if f.lower().endswith(video_extensions)]
    
    if not video_files:
        print(f"No videos found in {video_folder}")
        return []
    
    print(f"Converting {len(video_files)} videos")
    
    gif_paths = []
    for video_file in video_files:
        video_path = os.path.join(video_folder, video_file)
        try:
            gif_path = video_to_gif(video_path, output_folder, fps, resize_width)
            gif_paths.append(gif_path)
        except Exception as e:
            print(f"Failed: {video_file} - {str(e)}")
    
    print(f"Converted {len(gif_paths)}/{len(video_files)} videos")
    return gif_paths
