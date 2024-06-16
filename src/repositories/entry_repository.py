from abc import ABC, abstractmethod
from typing import Optional

from src.models.dictionary_entry import DictionaryEntry


class EntryRepository(ABC):
    @abstractmethod
    def get_entry(self, query: str) -> Optional[DictionaryEntry]:
        pass
