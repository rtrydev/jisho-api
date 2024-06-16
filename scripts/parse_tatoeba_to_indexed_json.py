import json
from fugashi import Tagger

def generate_jap_eng_dict():
    result = {}

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

            if len(result[word]) == 10:
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