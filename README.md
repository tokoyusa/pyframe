# PyFrame

GIF and Image moderation using [AWS Rekognition](https://aws.amazon.com/rekognition/content-moderation/) or local [HuggingFace](https://huggingface.co) models.

## About
PyFrame utilizes Temporal Segmentation to optimize moderation. Instead of processing every frame, the system divides the animation into equal time windows ("buckets") and calculates the inter-frame difference for each frame. It then applies motion-based keyframe selection to extract the single most significant frame from each bucket. This guarantees diverse scene coverage and captures peak motion events across the entire GIF. Supports both AWS Rekognition and local HuggingFace models for classification.

### AWS Rekognition Pricing Model
AWS Rekognition charges $1.00 per 1,000 images processed. A typical 5-second GIF (150 frames at 30 FPS) costs $0.15 to moderate when processing every frame, making comprehensive moderation expensive at scale.

### PyFrame's Bucketed Approach
PyFrame analyzes the same 150 frame GIF using just 10 intelligently selected frames, reducing the cost to $0.01 per GIF a 93% savings while maintaining detection accuracy. Alternatively, run the same frame extraction with a local HuggingFace model for zero cost (less accuracy than AWS) but can utilise a two pass approach optionally.

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
from lib.aws.pipe import Pipe

pipe = Pipe("content/gifs/your-gif.gif", max_frames=10, min_confidence=80.0)
results = pipe.run()
```

### Options

- `max_frames` - Number of frames to extract (default: 10)
- `min_confidence` - Minimum detection confidence (default: 80.0)
- `use_merged` - Merge frames before moderating (default: False)
- `frames_per_batch` - Frames per merged image (default: 2)

## LocalPipe

Bring your own model from HuggingFace instead of using AWS. Runs entirely locally, no API keys or AWS config needed. Defaults to [AdamCodd/vit-base-nsfw-detector](https://huggingface.co/AdamCodd/vit-base-nsfw-detector) but you can pass any HuggingFace image-classification model. Not as accurate as AWS Rekognition but works well as a free alternative, or use both together for a two-pass approach.

```python
from lib.local.local_pipe import LocalPipe

# default model
pipe = LocalPipe("content/gifs/your-gif.gif", max_frames=10)
results = pipe.run()

# custom model
pipe = LocalPipe("content/gifs/your-gif.gif", max_frames=10, model="Falconsai/nsfw_image_detection")
results = pipe.run()
```

### Options

- `max_frames` - Number of frames to extract (default: 5)
- `model` - HuggingFace model ID (default: `AdamCodd/vit-base-nsfw-detector`)
- `use_merged` - Merge frames before classifying (default: False)
- `frames_per_batch` - Frames per merged image (default: 2)

Requires `transformers` and `torch`:
```bash
pip install transformers torch
```

### Run

```bash
source .venv/bin/activate && python main.py
```

## Structure

- `content/` - All input/output files
- `lib/` - Core functionality
  - `aws/` - AWS Rekognition pipeline
    - `pipe.py` - Rekognition pipe
    - `rekognition_moderator.py` - Rekognition API wrapper
  - `local/` - Local HuggingFace pipeline
    - `local_pipe.py` - Local pipe
    - `local_detector.py` - HuggingFace model wrapper
  - `frame_processor.py` - Frame extraction
  - `image_utils.py` - Shared image helpers
  - `video_converter.py` - Video to GIF conversion

## Table
| Method | Frames Analyzed per GIF | Cost per GIF | GIFs Moderated | Cost Savings |
|--------|-------------------------|--------------|----------------|--------------|
| **Standard Method (All Frames)** | 150 frames | $0.15 | **66 GIFs** | Baseline |
| **PyFrame (10 Buckets)** | 10 frames | $0.01 | **1,000 GIFs** | **93% reduction** |

