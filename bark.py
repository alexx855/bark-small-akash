import os
import torch
import numpy as np
from datetime import datetime, timedelta
from transformers import AutoProcessor, BarkModel
from scipy.io.wavfile import write as write_wav
from apscheduler.schedulers.background import BackgroundScheduler
import glob

os.environ["SUNO_OFFLOAD_CPU"] = "True"
os.environ["SUNO_USE_SMALL_MODELS"] = "True"

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class AudioFileManager:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.cleanup_expired_files, 'interval', hours=1)
        self.scheduler.start()

    def cleanup_expired_files(self):
        expiration_time = datetime.now() - timedelta(hours=24)
        for file in glob.glob(os.path.join(self.output_dir, "audio_*.wav")):
            if datetime.fromtimestamp(os.path.getmtime(file)) < expiration_time:
                try:
                    os.remove(file)
                except Exception as e:
                    print(f"Failed to remove {file}: {e}")

    def save_audio(self, audio_array: np.ndarray, sample_rate: int) -> str:
        audio_array = np.clip(audio_array.astype(np.float32), -1, 1)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"audio_{timestamp}.wav")
        write_wav(filename, sample_rate, audio_array)
        return filename

class BarkTTS:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = AutoProcessor.from_pretrained("suno/bark-small")
        self.model = self._initialize_model()
        self.file_manager = AudioFileManager(OUTPUT_DIR)

    def _initialize_model(self):
        model = BarkModel.from_pretrained(
            "suno/bark-small",
            torch_dtype=torch.float16
        ).to(self.device)
        model = model.to_bettertransformer()
        model.enable_cpu_offload()
        return model

    def generate_speech(self, text: str, voice_preset: str = "v2/en_speaker_6") -> str:
        inputs = self.processor(text, voice_preset=voice_preset)
        inputs = {k: v.to(self.device) if hasattr(v, 'to') else v for k, v in inputs.items()}
        
        audio_array = self.model.generate(**inputs)
        audio_array = audio_array.cpu().numpy().squeeze()
        
        return self.file_manager.save_audio(
            audio_array,
            self.model.generation_config.sample_rate
        )

def generate_speech(text: str, voice_preset: str = "v2/en_speaker_6") -> str:
    tts = BarkTTS()
    return tts.generate_speech(text, voice_preset)

if __name__ == "__main__":
    output_file = generate_speech("Testing the text to speech system")
    print(f"Audio saved as: {output_file}")
