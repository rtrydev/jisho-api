from typing import List, Optional

from src.dtos.dictionary_entry_get_query_dto import DictionaryEntryGetQueryDTO
from src.dtos.dictionary_entry_read_dto import DictionaryEntryReadDTO
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
            word=result.dictionary_entry.word,
            reading=result.dictionary_entry.reading,
            translation=result.dictionary_entry.translation,
            example_sentences=result.example_sentences
        ), results))
