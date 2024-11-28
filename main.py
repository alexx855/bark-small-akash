import torch
from transformers import AutoProcessor, AutoModelForTextToWaveform, BarkModel
from scipy.io.wavfile import write as write_wav
import os
import time
from datetime import datetime
import numpy as np

# Environment settings
os.environ["SUNO_OFFLOAD_CPU"] = "True"
os.environ["SUNO_USE_SMALL_MODELS"] = "True"

def log_time(start_time, step_name):
    elapsed = time.time() - start_time
    print(f"{step_name}: {elapsed:.2f} seconds")
    return time.time()

def create_bark_audio(text, voice_preset, device):
    try:
        # Initialize model and processor
        start = time.time()
        processor = AutoProcessor.from_pretrained("suno/bark-small")
        model = BarkModel.from_pretrained("suno/bark-small", torch_dtype=torch.float16).to(device)
        model =  model.to_bettertransformer()
        model.enable_cpu_offload()
        start = log_time(start, "Model loading")

        # Process input text
        start = time.time()
        inputs = processor(
            text,
            voice_preset=voice_preset,
        )
        # Move inputs to device
        inputs = {k: v.to(device) if hasattr(v, 'to') else v for k, v in inputs.items()}
        start = log_time(start, "Input processing")

        # Generate audio
        start = time.time()
        audio_array = model.generate(**inputs)
        audio_array = audio_array.cpu().numpy().squeeze()

        start = log_time(start, "Audio generation")

        return audio_array, model.generation_config.sample_rate
    
    except Exception as e:
        print(f"Error during audio generation: {str(e)}")
        raise

def save_audio(audio_array, sample_rate, prefix="audio"):
    try:
        start = time.time()
        # Convert to float32 and normalize
        audio_array = audio_array.astype(np.float32)
        # Ensure audio is in the range [-1, 1]
        audio_array = np.clip(audio_array, -1, 1)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.wav"
        write_wav(filename, sample_rate, audio_array)
        log_time(start, "Audio saving")
        return filename
    
    except Exception as e:
        print(f"Error saving audio file: {str(e)}")
        raise

def main():
    total_start = time.time()

    # Device setup with optimizations
    torch.backends.cudnn.benchmark = True
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    try:
        # Voice settings
        # voice_preset = "v2/en_speaker_6"
        # voice_preset = "v2/es_speaker_0"
        voice_preset = "v2/es_speaker_2"
        text = "pinta esa patagonia amigo?"

        # Generate and save audio
        audio_array, sample_rate = create_bark_audio(text, voice_preset, device)
        filename = save_audio(audio_array, sample_rate)
        print(f"Audio saved as: {filename}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 1

    finally:
        log_time(total_start, "Total execution")
        
    return 0

if __name__ == "__main__":
    exit(main())