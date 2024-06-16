import json
import time
from typing import Dict, List
from src.models.example_sentence import ExampleSentence
from src.repositories.example_sentence_repository import ExampleSentenceRepository
from src.schemas.tatoeba_query_result import TatoebaQueryResult


class FileExampleSentenceRepository(ExampleSentenceRepository):
    __dictionary: Dict[str, List[TatoebaQueryResult]]

    def __init__(self) -> None:
        start_time = int(time.time() * 1000)
        self.__dictionary = self.__parse_file()
        print(f'Loaded examples in {int(time.time() * 1000) - start_time}ms')

    def get_example_sentences_by_word(self, key: str, limit: int = 10) -> List[ExampleSentence]:
        examples = self.__dictionary.get(key, [])

        return list(
            map(
                lambda example: ExampleSentence(
                    sentence=example.get('sentence'),
                    translation=example.get('translation')
                ),
                examples[:limit]
            )
        )

    def __parse_file(self, path: str = './jap_eng_examples.json') -> Dict[str, List[TatoebaQueryResult]]:
        with open(path, 'rb') as file:
            data = file.read().decode('utf8')

        return json.loads(data)

