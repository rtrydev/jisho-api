import json
import time
from typing import Dict, List, Optional
from src.models.example_sentence import ExampleSentence
from src.repositories.example_sentence_repository import ExampleSentenceRepository
from src.schemas.tatoeba_query_result import TatoebaQueryResult

from fugashi import Tagger


class FileExampleSentenceRepository(ExampleSentenceRepository):
    __dictionary: Dict[str, List[TatoebaQueryResult]]

    def __init__(self) -> None:
        start_time = int(time.time() * 1000)
        self.__dictionary = self.__parse_file()
        print(f'Loaded examples in {int(time.time() * 1000) - start_time}ms')

    def get_example_sentences_by_word(self, key: str, limit: int = 10) -> List[ExampleSentence]:
        examples = self.__dictionary.get(key, [])

        tagger = Tagger('-Owakati')

        return list(
            map(
                lambda example: ExampleSentence(
                    sentence=example.get('sentence'),
                    reading_hints=self.__get_unique_dicts([{
                        'word': str(entry),
                        'reading': self.__convert_katakana_to_hiragana(entry.feature.pron)
                    } for entry in tagger(example.get('sentence'))
                    if bool(entry.feature.pron)
                    and not self.__is_hiragana_only(str(entry))]),
                    translation=example.get('translation')
                ),
                examples[:limit]
            )
        )

    def __parse_file(self, path: str = './jap_eng_examples.json') -> Dict[str, List[TatoebaQueryResult]]:
        with open(path, 'rb') as file:
            data = file.read().decode('utf8')

        return json.loads(data)

    def __get_unique_dicts(self, hints):
        seen = set()
        unique_data = []

        for hint in hints:
            if hint['word'] in seen:
                continue

            seen.add(hint['word'])
            unique_data.append(hint)

        return unique_data

    def __is_hiragana_only(self, input: str) -> bool:
        return all('\u3040' <= char <= '\u309F' for char in input)

    def __convert_katakana_to_hiragana(self, input: str) -> Optional[str]:
        if input is None:
            return None

        katakana_to_hiragana = {
            'ア': 'あ', 'イ': 'い', 'ウ': 'う', 'エ': 'え', 'オ': 'お',
            'カ': 'か', 'キ': 'き', 'ク': 'く', 'ケ': 'け', 'コ': 'こ',
            'サ': 'さ', 'シ': 'し', 'ス': 'す', 'セ': 'せ', 'ソ': 'そ',
            'タ': 'た', 'チ': 'ち', 'ツ': 'つ', 'テ': 'て', 'ト': 'と',
            'ナ': 'な', 'ニ': 'に', 'ヌ': 'ぬ', 'ネ': 'ね', 'ノ': 'の',
            'ハ': 'は', 'ヒ': 'ひ', 'フ': 'ふ', 'ヘ': 'へ', 'ホ': 'ほ',
            'マ': 'ま', 'ミ': 'み', 'ム': 'む', 'メ': 'め', 'モ': 'も',
            'ヤ': 'や', 'ユ': 'ゆ', 'ヨ': 'よ',
            'ラ': 'ら', 'リ': 'り', 'ル': 'る', 'レ': 'れ', 'ロ': 'ろ',
            'ワ': 'わ', 'ヲ': 'を', 'ン': 'ん',
            'ガ': 'が', 'ギ': 'ぎ', 'グ': 'ぐ', 'ゲ': 'げ', 'ゴ': 'ご',
            'ザ': 'ざ', 'ジ': 'じ', 'ズ': 'ず', 'ゼ': 'ぜ', 'ゾ': 'ぞ',
            'ダ': 'だ', 'ヂ': 'ぢ', 'ヅ': 'づ', 'デ': 'で', 'ド': 'ど',
            'バ': 'ば', 'ビ': 'び', 'ブ': 'ぶ', 'ベ': 'べ', 'ボ': 'ぼ',
            'パ': 'ぱ', 'ピ': 'ぴ', 'プ': 'ぷ', 'ペ': 'ぺ', 'ポ': 'ぽ',
            'ァ': 'ぁ', 'ィ': 'ぃ', 'ゥ': 'ぅ', 'ェ': 'ぇ', 'ォ': 'ぉ',
            'ャ': 'ゃ', 'ュ': 'ゅ', 'ョ': 'ょ', 'ッ': 'っ'
        }

        return ''.join([
            katakana_to_hiragana.get(char, char)
            for char in input
        ])

