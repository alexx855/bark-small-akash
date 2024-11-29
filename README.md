# Bark Text-to-Speech App

[Bark small](https://github.com/suno-ai/bark) transformer-based text-to-audio model created by [Suno](https://suno.com/). Bark can generate highly realistic, multilingual speech as well as other audio - including music, background noise and simple sound effects.

## Quick Start

### Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
python app.py
```

The app will be available at http://localhost:7860

### Running with Docker

1. Build the Docker image:
```bash
docker build -t bark-tts .
```

2. Run the container:
```bash
docker run -p 7860:7860 bark-tts
```

For GPU support, add the `--gpus all` flag:
```bash
docker run --gpus all -p 7860:7860 bark-tts
```

To run in detached mode:
```bash
docker run -d -p 7860:7860 bark-tts
```

Access the app at http://localhost:7860

### Using the API

When you launch the app, Gradio automatically creates a REST API endpoint. The API URL will be displayed in the console output.

The app provides two API endpoints:

1. Audio Generation API (returns audio file):
```python
import requests

API_URL = "http://localhost:7860/api/predict/"

payload = {
    "data": [
        "Hello, this is a test message",  # Text input
        "Speaker 0 (EN)"                  # Voice selection
    ]
}

response = requests.post(API_URL, json=payload)
result = response.json()
print(result)  # Contains audio file data
```

2. URL Generation API (returns audio file URL):
```python
import requests

API_URL = "http://localhost:7860/api/predict/2"  # Note the /2 for second interface

payload = {
    "data": [
        "Hello, this is a test message",
        "Speaker 0 (EN)"
    ]
}

response = requests.post(API_URL, json=payload)
result = response.json()
print(result["data"])  # Contains URL to audio file
```

Example API usage with cURL:
```bash
# For audio file:
curl -X POST http://localhost:7860/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"data": ["Hello, this is a test message", "Speaker 0 (EN)"]}'

# For URL:
curl -X POST http://localhost:7860/api/predict/2 \
  -H "Content-Type: application/json" \
  -d '{"data": ["Hello, this is a test message", "Speaker 0 (EN)"]}'
```

## Features

- Multiple voice options including English and Spanish speakers
- Simple web interface
- API access enabled
- Example prompts included

## Documentation

- [Bark small Hugging Face](https://huggingface.co/suno/bark-small)
- [Available Voices](https://suno-ai.notion.site/8b8e8749ed514b0cbf3f699013548683)


