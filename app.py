import gradio as gr
from main import generate_speech
import os

VOICES = {
    "English Male": "v2/en_speaker_6",
    "English Female": "v2/en_speaker_7", 
    "Spanish Male": "v2/es_speaker_0",
    "Spanish Female": "v2/es_speaker_1"
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
        ["Hello, how are you today?", "English Male"],
        ["The weather is beautiful!", "English Female"],
        ["¡Hola! ¿Cómo estás?", "Spanish Male"]
    ]
)

if __name__ == "__main__":
    demo.launch(share=True)
