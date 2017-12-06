import requests


def translate_it(text, source_lang, dest_lang):
    """
    YANDEX translation plugin

    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/

    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    :param text: <str> text for translation.
    :return: <str> translated text.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'

    params = {
        'key': key,
        'lang': ''.join((source_lang, '-', dest_lang)),
        'text': text,
    }
    response = requests.get(url, params=params).json()
    return ' '.join(response.get('text', []))


def translate_file(source_file, dest_file, source_lang, dest_lang='ru'):
    with open(source_file) as sf:
        source_text = sf.read()
    dest_text = translate_it(source_text, source_lang, dest_lang)
    with open(dest_file, 'w') as df:
        df.write(dest_text)


translate_file('DE.txt', 'DE-RU.txt', 'de')
translate_file('ES.txt', 'ES-RU.txt', 'es')
translate_file('FR.txt', 'FR-RU.txt', 'fr')
