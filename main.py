import gradio
import whisper
from translate import Translator
from gtts import gTTS
import os
import atexit

def cleanup():
    if os.path.exists("output.mp3"):
        os.remove("output.mp3")

atexit.register(cleanup)

languages = {
    "English": "en",
    "French": "fr",
    "Portuguese": "pt",
}

def translate(audio_file, target_language):

    if audio_file is None:
        raise gradio.Error("No audio file was provided.")

    #* Speech to Text
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_file, language = "Spanish" , fp16=False)
        transcription = result["text"]
    except Exception as e:
        raise gradio.Error(f"An error occurred: {e}")

    #* Translate text
    try:
        translator = Translator(from_lang="es", to_lang=languages[target_language])
        translation = translator.translate(transcription)
    except Exception as e:
        raise gradio.Error(f"An error occurred: {e}")

    #* Text to Speech
    try:
        tts = gTTS(text=translation, lang=languages[target_language], slow=False)
        tts.save("output.mp3")
    except Exception as e:
        raise gradio.Error(f"An error occurred: {e}")

    return "output.mp3"

interface = gradio.Interface(
    fn =translate,
    inputs= [
        gradio.Audio(
        sources=["microphone", "upload"],
        type="filepath",
        label="Spanish",
        ),
        gradio.Dropdown(
            choices=list(languages.keys()),
            label="Select the target language.",
            value="English"
        )
    ],
    outputs=[gradio.Audio(label="Translation")],
    title="Speech to Text Translator",
    description="Translate your speech to text in any language",
    theme="soft",
    allow_flagging="never",
)

interface.launch()