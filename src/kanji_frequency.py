import pandas
import json
import os

kanji_frequency_path = './data/kanji_frequency.xlsx'
frequency_database_path = './data/frequency.json'

def build_frequency_database():
    kanjis = []
    kanji_header = '漢　字'
    df = pandas.read_excel(kanji_frequency_path, header=None)
    for index, row in df.iterrows():
        order = row[0]
        kanji = row[1]
        if isinstance(order, int) and kanji != kanji_header:
            kanjis.append(kanji[0])
    indices = {kanji: i for i, kanji in enumerate(kanjis)}
    with open(frequency_database_path, 'w') as f:
        json.dump(indices, f, indent=4)

def load_frequency_database():
    if not os.path.exists(frequency_database_path):
        build_frequency_database()
    with open(frequency_database_path) as f:
        database = json.load(f)
    return database


if __name__ == '__main__':
    database = load_frequency_database()