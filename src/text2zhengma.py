import os
import json
import kanji_frequency

dict_path = './rime-zhengma/zhengma.dict.yaml'
database_path = './data/zhengma.json'


def load_zhengma_database():
    if not os.path.exists(database_path):
        build_zhengma_database()
    with open(database_path) as f:
        database = json.load(f)
    return database


def build_zhengma_database():
    # the longest code for a kanji
    database_encode_default = {}
    # may have multiple codes for one single kanji
    database_encode = {}
    database_decode = {}
    database = [database_encode_default, database_encode, database_decode]
    frequency_database = kanji_frequency.load_frequency_database()
    with open(dict_path) as f:
        lines = f.readlines()
        for line in lines:
            temp = line.split('\t')
            # lines with no kanji
            if len(temp) == 1:
                continue
            kanji = temp[0].strip()
            # lines with multiple kanji
            if len(kanji) != 1:
                continue
            code = temp[1].strip()
            # ignore 構詞碼
            if len(code) == 0:
                continue
            codes = database_encode.get(kanji, [])
            kanjis = database_decode.get(code, [])
            codes.append(code)
            kanjis.append(kanji)
            kanjis.sort(key=lambda kanji: frequency_database[kanji]
                        if kanji in frequency_database
                        else len(frequency_database))
            database_encode[kanji] = codes
            database_decode[code] = kanjis
    for key, value in database_encode.items():
        database_encode_default[key] = max(value, key=len)
    with open(database_path, 'w') as f:
        json.dump(database, f, indent=4)


database_encode_default, database_encode, database_decode = load_zhengma_database()

def text2code(text):
    return list(database_encode_default.get(char, char) for char in text)

def text2code_mt(text):
    return list(database_encode_default.get(char, '') for char in text)

def code2word(code):
    return database_decode.get(code, [code])
