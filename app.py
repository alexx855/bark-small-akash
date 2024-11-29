import gradio as gr
from main import generate_speech
import os

VOICES = {
    "Speaker 0 (EN)": "v2/en_speaker_0",
    "Speaker 1 (EN)": "v2/en_speaker_1",
    "Speaker 2 (EN)": "v2/en_speaker_2",
    "Speaker 3 (EN)": "v2/en_speaker_3"
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
        gr.Dropdown(choices=list(VOICES.keys()), value="Speaker 0 (EN)", label="Voice")
    ],
    outputs=gr.Audio(label="Generated Speech"),
    title="Text to Speech with Bark",
    description="Generate realistic speech from text using the Bark model",
    allow_flagging="never",
    examples=[
        ["Welcome to the news. Today's top story...", "Speaker 0 (EN)"],
        ["Once upon a time in a magical forest...", "Speaker 1 (EN)"],
        ["The quick brown fox jumps over the lazy dog.", "Speaker 2 (EN)"],
        ["I love to sing and dance in the rain.", "Speaker 3 (EN)"]
    ]
)

if __name__ == "__main__":
    demo.launch(share=True)
