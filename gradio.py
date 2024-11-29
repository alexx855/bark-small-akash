import os
import gradio as gr
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from bark import generate_speech

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class VoicePresets:
    VOICES = {
        'English 1': 'v2/en_speaker_0',
        'English 2': 'v2/en_speaker_1',
        'English 3': 'v2/en_speaker_2',
        'Chinese 1': 'v2/zh_speaker_0',
        'Chinese 2': 'v2/zh_speaker_1',
        'French 1': 'v2/fr_speaker_0',
        'French 2': 'v2/fr_speaker_1',
        'German 1': 'v2/de_speaker_0',
        'German 2': 'v2/de_speaker_1',
        'Hindi 1': 'v2/hi_speaker_0',
        'Hindi 2': 'v2/hi_speaker_1',
        'Italian 1': 'v2/it_speaker_0',
        'Italian 2': 'v2/it_speaker_1',
        'Japanese 1': 'v2/ja_speaker_0',
        'Japanese 2': 'v2/ja_speaker_1',
        'Korean 1': 'v2/ko_speaker_0',
        'Korean 2': 'v2/ko_speaker_1',
        'Polish 1': 'v2/pl_speaker_0',
        'Polish 2': 'v2/pl_speaker_1',
        'Portuguese 1': 'v2/pt_speaker_0',
        'Portuguese 2': 'v2/pt_speaker_1',
        'Russian 1': 'v2/ru_speaker_0',
        'Russian 2': 'v2/ru_speaker_1',
        'Spanish 1': 'v2/es_speaker_0',
        'Spanish 2': 'v2/es_speaker_1',
        'Turkish 1': 'v2/tr_speaker_0',
        'Turkish 2': 'v2/tr_speaker_1',
    }

class AudioGenerator:
    def __init__(self):
        self.base_url = os.environ.get("PUBLIC_URL", "http://localhost:7860")

    def generate(self, text: str, voice: str):
        audio_file = generate_speech(text, VoicePresets.VOICES[voice])
        filename = os.path.basename(audio_file)
        url = f"{self.base_url}/generated/{filename}"
        return audio_file, url

class GradioInterface:
    def __init__(self):
        self.generator = AudioGenerator()
        self.interface = self._create_interface()

    def _create_interface(self):
        return gr.Interface(
            fn=self.generator.generate,
            inputs=[
                gr.Textbox(
                    label="Text to convert",
                    placeholder="Enter text here...",
                    show_copy_button=True
                ),
                gr.Dropdown(
                    choices=list(VoicePresets.VOICES.keys()),
                    value="English 1",
                    label="Voice Selection"
                )
            ],
            outputs=[
                gr.Audio(label="Generated Audio"),
                gr.Textbox(
                    label="Download URL",
                    interactive=False,
                    show_copy_button=True
                )
            ],
            title="AI Voice Generator 🎵",
            description="Transform text into natural-sounding speech in multiple languages",
            examples=[
                ["Hello, how are you today?", "English 1"],
                ["Bonjour, comment allez-vous?", "French 1"],
                ["Hola, ¿cómo estás?", "Spanish 1"],
                ["こんにちは、お元気ですか？", "Japanese 1"],
                ["你好，今天天气真好。", "Chinese 1"]
            ],
            allow_flagging="never"
        )

def create_app():
    app = FastAPI()
    app.mount("/generated", StaticFiles(directory=OUTPUT_DIR), name="generated")
    interface = GradioInterface()
    return gr.mount_gradio_app(app, interface.interface, path="/")

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=7860)
