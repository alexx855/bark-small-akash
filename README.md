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

Access the app at http://localhost:7860

## Features

- Multiple voice options including English and Spanish speakers
- Simple web interface
- API access enabled
- Example prompts included

## Documentation

- [Bark small Hugging Face](https://huggingface.co/suno/bark-small)
- [Available Voices](https://suno-ai.notion.site/8b8e8749ed514b0cbf3f699013548683)


