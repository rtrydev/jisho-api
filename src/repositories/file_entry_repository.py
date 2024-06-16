import json
import time
from typing import Optional, Dict

from src.models.dictionary_entry import DictionaryEntry
from src.repositories.entry_repository import EntryRepository
from src.schemas.jmdict_query_result import JMdictQueryResult


class FileEntryRepository(EntryRepository):
    __dictionary: Dict[str, JMdictQueryResult]

    def __init__(self):
        start_time = int(time.time() * 1000)
        self.__dictionary = self.__parse_file()
        print(f'Loaded dictionary entries in {int(time.time() * 1000) - start_time}ms')

    def get_entry(self, key: str) -> Optional[DictionaryEntry]:
        dict_entry = self.__dictionary.get(key)

        if dict_entry is None:
            return None

        return DictionaryEntry(
            word=key,
            reading=', '.join(dict_entry.get('reading')),
            translation=', '.join(dict_entry.get('glossary'))
        )

    def __parse_file(self, path: str = './jap_eng_dict.json') -> Dict[str, JMdictQueryResult]:
        with open(path, 'rb') as file:
            data = file.read().decode('utf8')

        return json.loads(data)
