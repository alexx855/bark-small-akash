# Bark Text-to-Speech Akash App

[![Awesome Akash](https://img.shields.io/badge/Awesome-Akash-blue)](https://github.com/akash-network/awesome-akash/tree/master/bark-small)

[Bark small](https://github.com/suno-ai/bark) transformer-based text-to-audio model created by [Suno](https://suno.com/). Bark can generate highly realistic, multilingual speech as well as other audio - including music, background noise and simple sound effects.

**🎉 This project is now featured in the [Awesome Akash collection](https://github.com/akash-network/awesome-akash/tree/master/bark-small)!**

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
docker build -t audio-akash .
```

2. Run the container:

```bash
docker run --gpus all -p 7860:7860 audio-akash
```

Access the app at http://localhost:7860

### Deploying on Akash Network

This project is designed to run on the [Akash Network](https://akash.network), a decentralized cloud computing marketplace.

1. Use the included `SDL.yaml` file for deployment
2. The deployment configuration is optimized for GPU-accelerated inference
3. Follow the [Akash deployment guide](https://akash.network/docs/deployments/akash-cli/overview/) for detailed instructions

For the complete deployment guide and example configurations, visit the [Awesome Akash repository](https://github.com/akash-network/awesome-akash/tree/master/bark-small).

## Features

- Multiple voice options including English and Spanish speakers
- Simple web interface
- Example prompts included

## Documentation

- [Bark small Hugging Face](https://huggingface.co/suno/bark-small)
- [Available Voices](https://suno-ai.notion.site/8b8e8749ed514b0cbf3f699013548683)
- [Akash Network](https://akash.network/docs)


