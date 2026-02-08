# PyFrame

GIF and Image moderation using [AWS Rekognition.](https://aws.amazon.com/rekognition/content-moderation/)

## About
PyFrame utilizes Temporal Segmentation to optimize moderation. Instead of processing every frame, the system divides the animation into equal time windows ("buckets") and calculates the inter-frame difference for each frame. It then applies motion-based keyframe selection to extract the single most significant frame from each bucket. This guarantees diverse scene coverage and captures peak motion events across the entire GIF, reducing AWS Rekognition costs by over 93% while maintaining high detection accuracy.

### AWS Rekognition Pricing Model
AWS Rekognition charges $1.00 per 1,000 images processed. A typical 5-second GIF (150 frames at 30 FPS) costs $0.15 to moderate when processing every frame, making comprehensive moderation expensive when at scale.

### PyFrame's Bucketed Approach
PyFrame analyzes the same 150 frame GIF using just 10 intelligently selected frames, reducing the cost to $0.01 per GIF a 93% savings while maintaining detection accuracy.

---
## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install AWS CLI (if not already installed):
```bash
brew install awscli
```

3. Configure AWS credentials:
```bash
aws configure
```

## Usage

Extract key frames from a GIF and moderate them:
```python
from lib.pipe import Pipe

pipe = Pipe("content/gifs/your-gif.gif", max_frames=10, min_confidence=80.0)
results = pipe.run()
```

### Options

- `max_frames` - Number of frames to extract (default: 10)
- `min_confidence` - Minimum detection confidence (default: 80.0)
- `use_merged` - Merge frames before moderating (default: False)
- `frames_per_batch` - Frames per merged image (default: 2)

### Run

```bash
source .venv/bin/activate && python main.py
```

## Structure

- `content/` - All input/output files
- `lib/` - Core functionality
  - `pipe.py` - Main pipeline
  - `frame_processor.py` - Frame extraction
  - `rekognition_moderator.py` - AWS moderation
  - `video_converter.py` - Video to GIF conversion

## Table
| Method | Frames Analyzed per GIF | Cost per GIF | GIFs Moderated | Cost Savings |
|--------|-------------------------|--------------|----------------|--------------|
| **Standard Method (All Frames)** | 150 frames | $0.15 | **66 GIFs** | Baseline |
| **PyFrame (10 Buckets)** | 10 frames | $0.01 | **1,000 GIFs** | **93% reduction** |

