from typing import List, Optional

from src.dtos.dictionary_entry_get_query_dto import DictionaryEntryGetQueryDTO
from src.dtos.dictionary_entry_read_dto import DictionaryEntryReadDTO
from src.dtos.example_sentence_read_dto import ExampleSentenceReadDTO
from src.services.query_parser_service import QueryParserService


class DictionaryController:
    __query_parser_service: QueryParserService

    def __init__(self, query_parser_service: QueryParserService):
        self.__query_parser_service = query_parser_service

    def query_for_entry(self, parameters: DictionaryEntryGetQueryDTO) -> Optional[List[DictionaryEntryReadDTO]]:
        results = self.__query_parser_service.parse_and_get_entries(parameters.query)

        if len(results) == 0:
            return None

        return list(map(lambda result: DictionaryEntryReadDTO(
            word=result.dictionary_entry.word + (f' [Matched from: {result.user_entry}]' if result.user_entry != result.dictionary_entry.word else ''),
            reading=result.dictionary_entry.reading,
            translation=result.dictionary_entry.translation,
            example_sentences=list(map(lambda example: ExampleSentenceReadDTO(
                sentence=example.sentence,
                translation=example.translation
            ), result.example_sentences))
        ), results))
