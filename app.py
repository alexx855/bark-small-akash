import gradio as gr
from main import generate_speech
import os

VOICES = {
'Speaker 0 (EN)':'v2/en_speaker_0',
'Speaker 1 (EN)':'v2/en_speaker_1',
'Speaker 2 (EN)':'v2/en_speaker_2',
'Speaker 3 (EN)':'v2/en_speaker_3',
'Speaker 4 (EN)':'v2/en_speaker_4',
'Speaker 5 (EN)':'v2/en_speaker_5',
'Speaker 6 (EN)':'v2/en_speaker_6',
'Speaker 7 (EN)':'v2/en_speaker_7',
'Speaker 8 (EN)':'v2/en_speaker_8',
'Speaker 9 (EN)':'v2/en_speaker_9',
'Speaker 0 (ZH)':'v2/zh_speaker_0',
'Speaker 1 (ZH)':'v2/zh_speaker_1',
'Speaker 2 (ZH)':'v2/zh_speaker_2',
'Speaker 3 (ZH)':'v2/zh_speaker_3',
'Speaker 4 (ZH)':'v2/zh_speaker_4',
'Speaker 5 (ZH)':'v2/zh_speaker_5',
'Speaker 6 (ZH)':'v2/zh_speaker_6',
'Speaker 7 (ZH)':'v2/zh_speaker_7',
'Speaker 8 (ZH)':'v2/zh_speaker_8',
'Speaker 9 (ZH)':'v2/zh_speaker_9',
'Speaker 0 (FR)':'v2/fr_speaker_0',
'Speaker 1 (FR)':'v2/fr_speaker_1',
'Speaker 2 (FR)':'v2/fr_speaker_2',
'Speaker 3 (FR)':'v2/fr_speaker_3',
'Speaker 4 (FR)':'v2/fr_speaker_4',
'Speaker 5 (FR)':'v2/fr_speaker_5',
'Speaker 6 (FR)':'v2/fr_speaker_6',
'Speaker 7 (FR)':'v2/fr_speaker_7',
'Speaker 8 (FR)':'v2/fr_speaker_8',
'Speaker 9 (FR)':'v2/fr_speaker_9',
'Speaker 0 (DE)':'v2/de_speaker_0',
'Speaker 1 (DE)':'v2/de_speaker_1',
'Speaker 2 (DE)':'v2/de_speaker_2',
'Speaker 3 (DE)':'v2/de_speaker_3',
'Speaker 4 (DE)':'v2/de_speaker_4',
'Speaker 5 (DE)':'v2/de_speaker_5',
'Speaker 6 (DE)':'v2/de_speaker_6',
'Speaker 7 (DE)':'v2/de_speaker_7',
'Speaker 8 (DE)':'v2/de_speaker_8',
'Speaker 9 (DE)':'v2/de_speaker_9',
'Speaker 0 (HI)':'v2/hi_speaker_0',
'Speaker 1 (HI)':'v2/hi_speaker_1',
'Speaker 2 (HI)':'v2/hi_speaker_2',
'Speaker 3 (HI)':'v2/hi_speaker_3',
'Speaker 4 (HI)':'v2/hi_speaker_4',
'Speaker 5 (HI)':'v2/hi_speaker_5',
'Speaker 6 (HI)':'v2/hi_speaker_6',
'Speaker 7 (HI)':'v2/hi_speaker_7',
'Speaker 8 (HI)':'v2/hi_speaker_8',
'Speaker 9 (HI)':'v2/hi_speaker_9',
'Speaker 0 (IT)':'v2/it_speaker_0',
'Speaker 1 (IT)':'v2/it_speaker_1',
'Speaker 2 (IT)':'v2/it_speaker_2',
'Speaker 3 (IT)':'v2/it_speaker_3',
'Speaker 4 (IT)':'v2/it_speaker_4',
'Speaker 5 (IT)':'v2/it_speaker_5',
'Speaker 6 (IT)':'v2/it_speaker_6',
'Speaker 7 (IT)':'v2/it_speaker_7',
'Speaker 8 (IT)':'v2/it_speaker_8',
'Speaker 9 (IT)':'v2/it_speaker_9',
'Speaker 0 (JA)':'v2/ja_speaker_0',
'Speaker 1 (JA)':'v2/ja_speaker_1',
'Speaker 2 (JA)':'v2/ja_speaker_2',
'Speaker 3 (JA)':'v2/ja_speaker_3',
'Speaker 4 (JA)':'v2/ja_speaker_4',
'Speaker 5 (JA)':'v2/ja_speaker_5',
'Speaker 6 (JA)':'v2/ja_speaker_6',
'Speaker 7 (JA)':'v2/ja_speaker_7',
'Speaker 8 (JA)':'v2/ja_speaker_8',
'Speaker 9 (JA)':'v2/ja_speaker_9',
'Speaker 0 (KO)':'v2/ko_speaker_0',
'Speaker 1 (KO)':'v2/ko_speaker_1',
'Speaker 2 (KO)':'v2/ko_speaker_2',
'Speaker 3 (KO)':'v2/ko_speaker_3',
'Speaker 4 (KO)':'v2/ko_speaker_4',
'Speaker 5 (KO)':'v2/ko_speaker_5',
'Speaker 6 (KO)':'v2/ko_speaker_6',
'Speaker 7 (KO)':'v2/ko_speaker_7',
'Speaker 8 (KO)':'v2/ko_speaker_8',
'Speaker 9 (KO)':'v2/ko_speaker_9',
'Speaker 0 (PL)':'v2/pl_speaker_0',
'Speaker 1 (PL)':'v2/pl_speaker_1',
'Speaker 2 (PL)':'v2/pl_speaker_2',
'Speaker 3 (PL)':'v2/pl_speaker_3',
'Speaker 4 (PL)':'v2/pl_speaker_4',
'Speaker 5 (PL)':'v2/pl_speaker_5',
'Speaker 6 (PL)':'v2/pl_speaker_6',
'Speaker 7 (PL)':'v2/pl_speaker_7',
'Speaker 8 (PL)':'v2/pl_speaker_8',
'Speaker 9 (PL)':'v2/pl_speaker_9',
'Speaker 0 (PT)':'v2/pt_speaker_0',
'Speaker 1 (PT)':'v2/pt_speaker_1',
'Speaker 2 (PT)':'v2/pt_speaker_2',
'Speaker 3 (PT)':'v2/pt_speaker_3',
'Speaker 4 (PT)':'v2/pt_speaker_4',
'Speaker 5 (PT)':'v2/pt_speaker_5',
'Speaker 6 (PT)':'v2/pt_speaker_6',
'Speaker 7 (PT)':'v2/pt_speaker_7',
'Speaker 8 (PT)':'v2/pt_speaker_8',
'Speaker 9 (PT)':'v2/pt_speaker_9',
'Speaker 0 (RU)':'v2/ru_speaker_0',
'Speaker 1 (RU)':'v2/ru_speaker_1',
'Speaker 2 (RU)':'v2/ru_speaker_2',
'Speaker 3 (RU)':'v2/ru_speaker_3',
'Speaker 4 (RU)':'v2/ru_speaker_4',
'Speaker 5 (RU)':'v2/ru_speaker_5',
'Speaker 6 (RU)':'v2/ru_speaker_6',
'Speaker 7 (RU)':'v2/ru_speaker_7',
'Speaker 8 (RU)':'v2/ru_speaker_8',
'Speaker 9 (RU)':'v2/ru_speaker_9',
'Speaker 0 (ES)':'v2/es_speaker_0',
'Speaker 1 (ES)':'v2/es_speaker_1',
'Speaker 2 (ES)':'v2/es_speaker_2',
'Speaker 3 (ES)':'v2/es_speaker_3',
'Speaker 4 (ES)':'v2/es_speaker_4',
'Speaker 5 (ES)':'v2/es_speaker_5',
'Speaker 6 (ES)':'v2/es_speaker_6',
'Speaker 7 (ES)':'v2/es_speaker_7',
'Speaker 8 (ES)':'v2/es_speaker_8',
'Speaker 9 (ES)':'v2/es_speaker_9',
'Speaker 0 (TR)':'v2/tr_speaker_0',
'Speaker 1 (TR)':'v2/tr_speaker_1',
'Speaker 2 (TR)':'v2/tr_speaker_2',
'Speaker 3 (TR)':'v2/tr_speaker_3',
'Speaker 4 (TR)':'v2/tr_speaker_4',
'Speaker 5 (TR)':'v2/tr_speaker_5',
'Speaker 6 (TR)':'v2/tr_speaker_6',
'Speaker 7 (TR)':'v2/tr_speaker_7',
'Speaker 8 (TR)':'v2/tr_speaker_8',
'Speaker 9 (TR)':'v2/tr_speaker_9',
}

def text_to_speech(text, voice):
    voice_preset = VOICES[voice]
    audio_file = generate_speech(text, voice_preset)
    return audio_file

def text_to_speech_url(text, voice):
    voice_preset = VOICES[voice]
    audio_file = generate_speech(text, voice_preset)
    # Convert local path to URL path
    return f"/file={audio_file}"

# Create Gradio interfaces
# Main interface for audio playback
demo1 = gr.Interface(
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
        ["I love to sing and dance in the rain.", "Speaker 3 (EN)"],
        ["The weather today will be sunny with a high of 75 degrees.", "Speaker 4 (EN)"]
    ]
)

# API interface for getting URL
demo2 = gr.Interface(
    fn=text_to_speech_url,
    inputs=[
        gr.Textbox(label="Text to speak"),
        gr.Dropdown(choices=list(VOICES.keys()), value="Speaker 0 (EN)", label="Voice")
    ],
    outputs=gr.Textbox(label="Audio File URL"),
    title="Text to Speech API",
    description="Get URL for generated speech audio file",
)

# Combine the interfaces
demo = gr.TabbedInterface([demo1, demo2], ["Audio Player", "Get URL"])

if __name__ == "__main__":
    demo.launch(share=True, enable_api=True)
