import gradio as gr
from main import generate_speech
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

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

def text_to_speech_with_url(text, voice):
    voice_preset = VOICES[voice]
    audio_file = generate_speech(text, voice_preset)
    filename = os.path.basename(audio_file)
    base_url = os.environ.get("PUBLIC_URL", "http://localhost:7860")
    url = f"{base_url}/generated/{filename}"
    return audio_file, url

# Create single Gradio interface with both outputs
demo = gr.Interface(
    fn=text_to_speech_with_url,
    inputs=[
        gr.Textbox(label="Text to audio", placeholder="Enter text here...", show_copy_button=True, show_label=True),
        gr.Dropdown(choices=list(VOICES.keys()), value="Speaker 0 (EN)", label="Voice")
    ],
    outputs=[
        gr.Audio(label="Generated Speech"),
        gr.Textbox(
            label="Public URL", 
            interactive=False,
            show_copy_button=True,
            show_label=True
        )
    ],
    title="Audio Akash 🎵 AI Audio Generator",
    description="""
    Transform text into natural-sounding speech using the Bark AI model. 
    Features support for multiple languages and voice styles.
    
    **How to use:**
    1. Enter your text in any supported language
    2. Select a voice preset
    3. Click submit to generate speech
    4. Get the public URL to share/download the generated audio (it will expire in 24 hours)
    """,
    article="Powered by Bark-small model from Suno AI",
    allow_flagging="never",
    examples=[
        # English examples
        ["Welcome to the news. Today's top story...", "Speaker 0 (EN)"],
        ["The quick brown fox jumps over the lazy dog.", "Speaker 1 (EN)"],
        # Chinese examples
        ["你好，今天天气真不错。", "Speaker 0 (ZH)"],
        # French examples
        ["Bonjour, comment allez-vous aujourd'hui?", "Speaker 0 (FR)"],
        ["J'aime beaucoup voyager en France.", "Speaker 1 (FR)"],
        # German examples
        ["Guten Tag, wie geht es Ihnen?", "Speaker 0 (DE)"],
        ["Das Wetter ist heute sehr schön.", "Speaker 1 (DE)"],
        # Hindi examples
        ["नमस्ते, आप कैसे हैं?", "Speaker 0 (HI)"],
        ["मौसम बहुत सुहावना है।", "Speaker 1 (HI)"],
        # Italian examples
        ["Buongiorno, come stai oggi?", "Speaker 0 (IT)"],
        ["Mi piace molto viaggiare in Italia.", "Speaker 1 (IT)"],
        # Japanese examples
        ["こんにちは、お元気ですか？", "Speaker 0 (JA)"],
        ["今日はとても良い天気ですね。", "Speaker 1 (JA)"],
        # Korean examples
        ["안녕하세요, 오늘 기분이 어떠신가요?", "Speaker 0 (KO)"],
        ["날씨가 정말 좋네요.", "Speaker 1 (KO)"],
        # Polish examples
        ["Dzień dobry, jak się masz?", "Speaker 0 (PL)"],
        ["Dzisiaj jest bardzo ładna pogoda.", "Speaker 1 (PL)"],
        # Portuguese examples
        ["Olá, como está você hoje?", "Speaker 0 (PT)"],
        ["O tempo está muito bonito hoje.", "Speaker 1 (PT)"],
        # Russian examples
        ["Здравствуйте, как ваши дела?", "Speaker 0 (RU)"],
        ["Сегодня прекрасная погода.", "Speaker 1 (RU)"],
        # Spanish examples
        ["Hola, ¿cómo estás hoy?", "Speaker 0 (ES)"],
        ["El tiempo está muy bonito hoy.", "Speaker 1 (ES)"],
        # Turkish examples
        ["Merhaba, bugün nasılsınız?", "Speaker 0 (TR)"],
        ["Bugün hava çok güzel.", "Speaker 1 (TR)"]
    ]
)

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "output") 
os.makedirs(OUTPUT_DIR, exist_ok=True)

if __name__ == "__main__":
    app = FastAPI()
    app.mount("/generated", StaticFiles(directory=OUTPUT_DIR), name="generated")
    gradio_app = gr.mount_gradio_app(app, demo, path="/", favicon_path="favicon.ico")
    uvicorn.run(app, host="0.0.0.0", port=7860)