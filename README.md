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

Example API usage with Python:
```python
import requests

API_URL = "http://localhost:7860/api/predict"

# Prepare the payload
payload = {
    "data": [
        "Hello, this is a test message",  # Text input
        "Speaker 0 (EN)"                  # Voice selection
    ]
}

# Make the API request
response = requests.post(API_URL, json=payload)
result = response.json()

# The result will contain the path to the generated audio file
print(result)
```

Example API usage with cURL:
```bash
curl -X POST http://localhost:7860/api/predict \
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


