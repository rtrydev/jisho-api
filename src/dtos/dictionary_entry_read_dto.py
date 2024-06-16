from dataclasses import dataclass
from typing import List, Optional

from src.dtos.example_sentence_read_dto import ExampleSentenceReadDTO


@dataclass
class DictionaryEntryReadDTO:
    word: str
    translation: str
    reading: str
    example_sentences: Optional[List[ExampleSentenceReadDTO]]
