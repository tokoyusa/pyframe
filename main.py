# from lib.frame_processor import extract_significant_frames
# from lib.rekognition_moderator import RekognitionModerator
# from lib.video_converter import video_to_gif
from lib.pipe import Pipe
from lib.setup import setup_folders

if __name__ == "__main__":
    # Setup for project sturcture
    setup_folders()    
    # Extract significant frames only (compressed)
    # extract_significant_frames("content/gifs/mandiving.gif", max_frames=5)
    
    # Moderate specific compressed gif folder using AWS Rekognition
    # moderator = RekognitionModerator(region_name='us-east-1')
    # moderator.moderate_folder('content/compressed_gifs/mandiving', min_confidence=80.0)


    # Turn video into gif for moderation
    # video_to_gif("content/videos/RSCsJP8agR45f9dCjK.mp4", output_folder='content/gifs', fps=15)

    # Pipeline Command without merge.
    # pipe = Pipe("content/compressed_gifs/mandiving/02_frame_024_score_224361.jpg", max_frames=5, region_name='us-east-1', min_confidence=80.0)
    # results = pipe.run()

    # Pipeline command with a merge to save calls
    pipe = Pipe("ur/path/here.gif", max_frames=5, region_name='us-east-1', min_confidence=80.0, use_merged=True, frames_per_batch=2)
    results = pipe.run()