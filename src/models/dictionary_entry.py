from dataclasses import dataclass

from src.models.example_sentence import ExampleSentence


@dataclass
class DictionaryEntry:
    word: str
    translation: str
    reading: str
