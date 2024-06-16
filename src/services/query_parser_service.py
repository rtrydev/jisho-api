from typing import List
from collections import OrderedDict
from src.models.word_data import WordData
from src.repositories.entry_repository import EntryRepository

from fugashi import Tagger

from src.repositories.example_sentence_repository import ExampleSentenceRepository


class QueryParserService:
    __entry_repository: EntryRepository
    __example_sentence_repository: ExampleSentenceRepository

    def __init__(self, entry_repository: EntryRepository, example_sentence_repository: ExampleSentenceRepository) -> None:
        self.__entry_repository = entry_repository
        self.__example_sentence_repository = example_sentence_repository

    def parse_and_get_entries(self, query: str) -> List[WordData]:
        tagger = Tagger('-Owakati')
        query_result = tagger(query)

        user_input_matches = {
            word.feature.lemma: str(word)
            for word in query_result
        }

        unique_tags = list(
            OrderedDict.fromkeys(
                word.feature.lemma for word in query_result
            )
        )

        print(f'Got {len(unique_tags)} unique tags')

        entries = [
            self.__entry_repository.get_entry(tag)
            for tag in unique_tags
        ]

        return [
            WordData(
                user_entry=user_input_matches.get(entry.word),
                dictionary_entry=entry,
                example_sentences=self.__example_sentence_repository.get_example_sentences_by_word(entry.word)
            )
            for entry in entries
            if entry is not None
        ]
