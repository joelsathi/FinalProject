from googletrans import Translator, constants
from pprint import pprint


def translate_to_lang(message: str, translate_from: str, translate_to: str):
    translator = Translator()
    translation = translator.translate(message, dest=translate_to, src=translate_from)
    print(translation.text)
    return translation.text
