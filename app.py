import gradio as gr
from main import generate_speech
import os

VOICES = {
    "English Speaker 0": "v2/en_speaker_0",
    "English Speaker 1": "v2/en_speaker_1",
    "English Speaker 2": "v2/en_speaker_2",
    "English Speaker 3": "v2/en_speaker_3",
    "English Speaker 4": "v2/en_speaker_4",
    "English Speaker 5": "v2/en_speaker_5",
    "English Speaker 6": "v2/en_speaker_6",
    "English Speaker 7": "v2/en_speaker_7",
    "English Speaker 8": "v2/en_speaker_8",
    "English Speaker 9": "v2/en_speaker_9",
    "French Speaker 0": "v2/fr_speaker_0",
    "French Speaker 1": "v2/fr_speaker_1",
    "French Speaker 2": "v2/fr_speaker_2",
    "French Speaker 3": "v2/fr_speaker_3",
    "French Speaker 4": "v2/fr_speaker_4",
    "French Speaker 5": "v2/fr_speaker_5",
    "Chinese Speaker 0": "v2/zh_speaker_0",
    "Chinese Speaker 1": "v2/zh_speaker_1",
    "Chinese Speaker 2": "v2/zh_speaker_2",
    "Chinese Speaker 3": "v2/zh_speaker_3",
    "Chinese Speaker 4": "v2/zh_speaker_4",
    "Chinese Speaker 5": "v2/zh_speaker_5",
    "Chinese Speaker 6": "v2/zh_speaker_6",
    "Chinese Speaker 7": "v2/zh_speaker_7",
    "Chinese Speaker 8": "v2/zh_speaker_8",
    "Chinese Speaker 9": "v2/zh_speaker_9"
}

def text_to_speech(text, voice):
    voice_preset = VOICES[voice]
    audio_file = generate_speech(text, voice_preset)
    return audio_file

# Create Gradio interface
demo = gr.Interface(
    fn=text_to_speech,
    inputs=[
        gr.Textbox(label="Text to speak", placeholder="Enter text here..."),
        gr.Dropdown(choices=list(VOICES.keys()), value="English Male", label="Voice")
    ],
    outputs=gr.Audio(label="Generated Speech"),
    title="Text to Speech with Bark",
    description="Generate realistic speech from text using the Bark model",
    allow_flagging="never",
    examples=[
        ["Welcome to the news. Today's top story...", "English Male (NPR)"],
        ["Once upon a time in a magical forest...", "English Female (Audiobook)"],
        ["¡Hola! ¿Cómo estás? El día está hermoso.", "Spanish Female (Warm)"],
        ["Guten Tag! Wie geht es Ihnen?", "German Female"],
        ["Bonjour! Comment allez-vous aujourd'hui?", "French Female"],
        ["नमस्ते! आप कैसे हैं?", "Hindi Female"],
        ["Ciao! Come stai oggi?", "Italian Male"],
        ["こんにちは！お元気ですか？", "Japanese Female"]
    ]
)

if __name__ == "__main__":
    demo.launch(share=True)
