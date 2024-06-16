import json
from typing import Dict, List
from fugashi import Tagger

def get_similarity_index(sentence1, sentence2) -> float:
    character_overlap = 0
    characters = len(sentence1) + len(sentence2)

    for character in sentence1:
        if character in sentence2:
            character_overlap += 1

    for character in sentence2:
        if character in sentence1:
            character_overlap += 1

    return character_overlap / characters

def generate_jap_eng_dict():
    result: Dict[str, List[Dict[str, str]]] = {}

    with open('./tatoeba-jap-eng.tsv', 'rb') as file:
        lines = list(map(lambda line: line.decode('utf8'), file.readlines()))

    tagger = Tagger('-Owakati')

    for line in lines:
        splits = line.replace('\r\n', '').split('\t')

        japanese_sentence = splits[1]
        english_sentence = splits[3]

        words = tagger(japanese_sentence)
        word_indexes = list(
            filter(
                lambda word_idx: word_idx is not None and word_idx not in ['。', '！', '？', '、', '「', '」'],
                map(lambda word: word.feature.lemma, words)
            )
        )

        for word in word_indexes:
            if word not in result:
                result[word] = []

            if len(result[word]) == 10 or any(
                get_similarity_index(entry['sentence'], japanese_sentence) > 0.8
                for entry in result[word]
            ):
                continue

            result[word].append({
                'sentence': japanese_sentence,
                'translation': english_sentence
            })

    with open('./jap_eng_examples.json', 'wb') as file:
        dict_dump = json.dumps(result)

        file.write(dict_dump.encode('utf8'))

if __name__ == '__main__':
    generate_jap_eng_dict()