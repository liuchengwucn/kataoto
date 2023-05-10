import pykakasi
kks = pykakasi.kakasi()


def text2hiragana(text):
    result = kks.convert(text)
    hiragana = ''.join(item['hira'] if len(item['hira']) != 0
                       else item['orig'] for item in result)
    return hiragana


def text2katakana(text):
    result = kks.convert(text)
    katakana = ''.join(item['kana'] if len(item['kana']) != 0
                       else item['orig'] for item in result)
    return katakana


def text2romaji(text):
    result = kks.convert(text)
    romaji = ''.join(item['kunrei'] if len(item['kunrei']) != 0
                     else item['orig'] for item in result)
    return romaji


def text2pairs(text):
    result = kks.convert(text)
    pairs = []
    for item in result:
        word = item['hira']
        if item['orig'] == item['hira']:
            word = ''
        elif item['orig'] == item['kana']:
            word = ''
        pairs.append((item['orig'], word))
    return pairs

