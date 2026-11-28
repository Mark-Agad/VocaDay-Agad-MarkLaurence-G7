from urllib.parse import quote

import requests

API_URL = 'https://api.dictionaryapi.dev/api/v2/entries/en/'


class WordNotFound(Exception):
    """The API has no definition for this word."""


class DictionaryUnavailable(Exception):
    """The API could not be reached or returned an error."""


def lookup_word(word):
    try:
        response = requests.get(API_URL + quote(word), timeout=5)
    except requests.RequestException:
        raise DictionaryUnavailable()

    if response.status_code == 404:
        raise WordNotFound()
    if response.status_code != 200:
        raise DictionaryUnavailable()

    try:
        entries = response.json()
    except ValueError:
        raise DictionaryUnavailable()

    phonetic = ''
    audio = ''
    meanings = []

    for entry in entries:
        if not phonetic:
            phonetic = entry.get('phonetic') or ''
        for item in entry.get('phonetics', []):
            if not phonetic and item.get('text'):
                phonetic = item['text']
            if not audio and item.get('audio'):
                audio = item['audio']
        for meaning in entry.get('meanings', []):
            definitions = []
            for d in meaning.get('definitions', []):
                definitions.append({
                    'definition': d.get('definition', ''),
                    'example': d.get('example', ''),
                })
            meanings.append({
                'part_of_speech': meaning.get('partOfSpeech', ''),
                'definitions': definitions,
            })

    if audio.startswith('//'):
        audio = 'https:' + audio

    return {
        'word': entries[0].get('word', word),
        'phonetic': phonetic,
        'audio': audio,
        'meanings': meanings,
    }