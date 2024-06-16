import json
import re


def generate_jap_eng_dict():
    result = {}

    with open('./JMdict', 'rb') as file:
        lines = file.readlines()
        current_data = {
            'entries': [],
            'glossary': [],
            'reading': []
        }

        lines = [
            line.decode('utf8')
            for line in lines
        ]

        for line in lines:
            if line == '</entry>\n':
                if len(current_data['entries']) > 0:
                    for entry in current_data['entries']:
                        result[entry] = {
                            'entries': result.get(entry, {}).get('entries', []) + current_data['entries'],
                            'glossary': result.get(entry, {}).get('glossary', []) + current_data['glossary'],
                            'reading': result.get(entry, {}).get('reading', []) + current_data['reading']
                        }
                elif current_data['reading']:
                    for reading in current_data['reading']:
                        result[reading] = {
                                'glossary': result.get(reading, {}).get('glossary', []) + current_data['glossary'],
                                'reading': result.get(reading, {}).get('reading', []) + current_data['reading']
                            }

                current_data = {
                    'entries': [],
                    'glossary': [],
                    'reading': []
                }
                continue

            keb_match = re.match(r'<keb>(.*)</keb>', line)

            if keb_match is not None:
                current_data['entries'].append(keb_match.group(1))
                continue

            reb_match = re.match(r'<reb>(.*)</reb>', line)

            if reb_match is not None:
                current_data['reading'].append(reb_match.group(1))
                continue

            glossary_match = re.match(r'<gloss>(.*)</gloss>', line)

            if glossary_match is not None:
                current_data['glossary'].append(glossary_match.group(1))
                continue

    with open('./jap_eng_dict.json', 'wb') as file:
        dict_dump = json.dumps(result)

        file.write(dict_dump.encode('utf8'))


if __name__ == '__main__':
    generate_jap_eng_dict()
