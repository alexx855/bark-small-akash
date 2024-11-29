import torch
from transformers import AutoProcessor, AutoModelForTextToWaveform, BarkModel
from scipy.io.wavfile import write as write_wav
import os
import time
from datetime import datetime, timedelta
import numpy as np
from apscheduler.schedulers.background import BackgroundScheduler
import glob

# Environment settings
os.environ["SUNO_OFFLOAD_CPU"] = "True"
os.environ["SUNO_USE_SMALL_MODELS"] = "True"

# Create output directory if it doesn't exist
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "output") 
os.makedirs(OUTPUT_DIR, exist_ok=True)

#create hf directory if it doesn't exist
HF_DIR = os.environ.get("HF_HOME", "hf")

def cleanup_old_files():
    """Remove audio files older than 24 hour"""
    cutoff_time = datetime.now() - timedelta(hours=24)  # Changed from minutes=2 to hours=1
    for file in glob.glob(os.path.join(OUTPUT_DIR, "audio_*.wav")):
        file_time = datetime.fromtimestamp(os.path.getmtime(file))
        if file_time < cutoff_time:
            try:
                os.remove(file)
                print(f"Removed old file: {file}")
            except Exception as e:
                print(f"Error removing file {file}: {e}")

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_old_files, 'interval', hours=1)  # Changed from minutes=1 to hours=1
scheduler.start()

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
        filename = os.path.join(OUTPUT_DIR, f"{prefix}_{timestamp}.wav")
        write_wav(filename, sample_rate, audio_array)
        log_time(start, "Audio saving")
        return filename
    
    except Exception as e:
        print(f"Error saving audio file: {str(e)}")
        raise

def generate_speech(text, voice_preset="v2/en_speaker_6"):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    try:
        audio_array, sample_rate = create_bark_audio(text, voice_preset, device)
        filename = save_audio(audio_array, sample_rate)
        return filename
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    text = "my cat is very cute"
    filename = generate_speech(text)
    print(f"Audio saved as: {filename}")
