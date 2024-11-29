import gradio as gr
from main import generate_speech
import os

VOICES = {
    # English Speakers
    "English Male (Announcer)": "v2/en_speaker_0",  # Male, Announcer voice
    "English Male (Deep)": "v2/en_speaker_1",       # Male, Deep voice
    "English Female (Young)": "v2/en_speaker_2",    # Female, Young voice
    "English Male (Senior)": "v2/en_speaker_3",     # Male, Older voice
    "English Female (Professional)": "v2/en_speaker_4", # Female, Professional voice
    "English Male (Clear)": "v2/en_speaker_5",      # Male, Clear voice
    "English Male (Narrative)": "v2/en_speaker_6",  # Male, Good for narration
    "English Female (Warm)": "v2/en_speaker_7",     # Female, Warm tone
    "English Male (NPR)": "v2/en_speaker_8",        # Male, NPR style voice
    "English Female (Audiobook)": "v2/en_speaker_9", # Female, Good for audiobooks

    # German Speakers
    "German Male": "v2/de_speaker_0",               # Male, Clear German voice
    "German Female": "v2/de_speaker_1",             # Female, Standard German

    # Spanish Speakers
    "Spanish Male (Clear)": "v2/es_speaker_0",      # Male, Clear Spanish
    "Spanish Female (Warm)": "v2/es_speaker_1",     # Female, Warm tone
    "Spanish Male (Deep)": "v2/es_speaker_2",       # Male, Deep voice
    "Spanish Female (Young)": "v2/es_speaker_3",    # Female, Young voice

    # French Speakers
    "French Male": "v2/fr_speaker_0",               # Male, Standard French
    "French Female": "v2/fr_speaker_1",             # Female, Clear French
    
    # Hindi Speakers
    "Hindi Female": "v2/hi_speaker_0",              # Female, Clear Hindi
    "Hindi Male": "v2/hi_speaker_1",                # Male, Standard Hindi

    # Italian Speakers
    "Italian Male": "v2/it_speaker_0",              # Male, Standard Italian
    "Italian Female": "v2/it_speaker_1",            # Female, Clear Italian

    # Japanese Speakers
    "Japanese Female": "v2/ja_speaker_0",           # Female, Clear Japanese
    "Japanese Male": "v2/ja_speaker_1"              # Male, Standard Japanese
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
