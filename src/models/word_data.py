from dataclasses import dataclass
from typing import List

from src.models.dictionary_entry import DictionaryEntry
from src.models.example_sentence import ExampleSentence


@dataclass
class WordData:
    dictionary_entry: DictionaryEntry
    example_sentences: List[ExampleSentence]
    