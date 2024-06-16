import dataclasses
import json

from src.controllers.dictionary_controller import DictionaryController
from src.dtos.dictionary_entry_get_query_dto import DictionaryEntryGetQueryDTO
from src.repositories.file_entry_repository import FileEntryRepository
from src.repositories.file_example_sentence_repository import FileExampleSentenceRepository
from src.services.query_parser_service import QueryParserService


def handler(event, _):
    query_params = event.get('queryStringParameters', {})

    if 'query' not in query_params:
        return {
            'statusCode': 403,
            'body': json.dumps({
                'message': 'You need to provide a query!'
            })
        }

    parameters = DictionaryEntryGetQueryDTO(
        query=query_params.get('query')
    )

    print(f'Received query: {parameters}')

    results = DictionaryController(
        QueryParserService(
            FileEntryRepository(),
            FileExampleSentenceRepository()
        )
    ).query_for_entry(parameters)

    if results is None:
        return {
            'statusCode': 404
        }

    return {
        'statusCode': 200,
        'body': json.dumps({
            'entries': [
                dataclasses.asdict(result)
                for result in results
            ]
        })
    }
