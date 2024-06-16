from abc import ABC, abstractmethod
from typing import List

from src.models.example_sentence import ExampleSentence


class ExampleSentenceRepository(ABC):
    @abstractmethod
    def get_example_sentences_by_word(self, key: str, limit: int) -> List[ExampleSentence]:
        pass
