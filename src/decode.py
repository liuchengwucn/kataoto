import text2zhengma
import json
import os
import xml.etree.ElementTree as ET
import opencc
import itertools
import wanakana
import mozcpy

kanjidic2_path = './data/kanjidic2.xml'
yomikata_database_path = './data/yomikata.json'
dict_path = './data/jukujikun.txt'
jukujikun_database_path = './data/jukujikun.json'


def load_yomikata_database():
    if not os.path.exists(yomikata_database_path):
        build_yomikata_database()
    with open(yomikata_database_path) as f:
        database = json.load(f)
    return database


def build_yomikata_database():
    converter = opencc.OpenCC('t2jp.json')

    dakuon_dict = {
        'か': 'が', 'き': 'ぎ', 'く': 'ぐ', 'け': 'げ', 'こ': 'ご',
        'さ': 'ざ', 'し': 'じ', 'す': 'ず', 'せ': 'ぜ', 'そ': 'ぞ',
        'た': 'だ', 'ち': 'ぢ', 'つ': 'づ', 'て': 'で', 'と': 'ど',
        'は': 'ば', 'ひ': 'び', 'ふ': 'ぶ', 'へ': 'べ', 'ほ': 'ぼ'
    }

    handakuon_dict = {
        'は': 'ぱ', 'ひ': 'ぴ', 'ふ': 'ぷ', 'へ': 'ぺ', 'ほ': 'ぽ'
    }

    sokuon_set = {'き', 'ち', 'り', 'ひ', 'い' 'く', 'つ', 'る', 'ふ', 'う'}

    def convert(yomikatas):
        # convert katakana to hiragana, remove all '.'
        # add support for 促音便, 連濁 and 半濁音化
        origin = [wanakana.to_hiragana(yomikata.replace('-', ''))
                  for yomikata in itertools.accumulate(yomikatas.split('.'))]
        added = []

        for yomikata in origin:
            if yomikata[0] in dakuon_dict:
                added.append(dakuon_dict[yomikata[0]] + yomikata[1:])
            if yomikata[0] in handakuon_dict:
                added.append(handakuon_dict[yomikata[0]] + yomikata[1:])
            if yomikata[-1] in sokuon_set:
                added.append(yomikata[:-1] + 'っ')

        return origin + added

    database = {}
    tree = ET.parse(kanjidic2_path)
    for character in tree.getroot():
        if character.tag != 'character':
            continue
        pronunciation = []
        literal = character.find('literal').text
        literal = converter.convert(literal)
        reading_meaning = character.find('reading_meaning')
        if reading_meaning is None:
            continue
        rmgroup = reading_meaning.find('rmgroup')
        readings = rmgroup.findall('reading')
        for reading in readings:
            r_type = reading.get('r_type')
            if r_type != 'ja_on' and r_type != 'ja_kun':
                continue
            pronunciation.extend(convert(reading.text))
        nanoris = reading_meaning.findall('nanori')
        for nanori in nanoris:
            pronunciation.extend(convert(nanori.text))
        if literal in database:
            database[literal] = list(set(database[literal] + pronunciation))
        else:
            database[literal] = list(set(pronunciation))

    # let kanji in 常用漢字表 appear in

    with open(yomikata_database_path, 'w') as f:
        json.dump(database, f, indent=4)


def load_jukujikun_database():
    if not os.path.exists(jukujikun_database_path):
        build_jukujikun_database()
    with open(jukujikun_database_path) as f:
        database = json.load(f)
    return database


def build_jukujikun_database():
    converter = opencc.OpenCC('t2jp.json')
    database = {}
    with open(dict_path) as f:
        lines = f.readlines()
    for line in lines:
        kanji, yomikatas = line.strip().split('\t')
        kanji = converter.convert(kanji)
        if '&' in yomikatas:
            yomikatas = list(itertools.accumulate(yomikatas.split('&')))
        else:
            yomikatas = [yomikatas]
        for yomikata in yomikatas:
            kanjis = database.get(yomikata, [])
            kanjis.append(kanji)
            database[yomikata] = kanjis
    with open(jukujikun_database_path, 'w') as f:
        json.dump(database, f, indent=4)


jukujikun_database = load_jukujikun_database()
yomikata_database = load_yomikata_database()


def text2text_list(text, begin='#', sep='<', end='>'):
    lb = len(begin)
    ls = len(sep)
    le = len(end)
    text_list = []
    buffer = []
    state = 0

    def clear_buffer():
        if len(buffer) != 0:
            if state == 2:
                text_list.extend(''.join(buffer).split())
            else:
                text_list.append(''.join(buffer))
            buffer.clear()
    i = 0
    while i < len(text):
        if text[i:i+lb] == begin:
            clear_buffer()
            state = 1
            i += lb
            text_list.append(begin)
        elif text[i:i+ls] == sep:
            clear_buffer()
            state = 2
            i += ls
            text_list.append(sep)
        elif text[i:i+le] == end:
            clear_buffer()
            state = 0
            i += le
            text_list.append(end)
        else:
            buffer.append(text[i])
            i += 1
    clear_buffer()
    return text_list


def decode(text, begin='#', sep='<', end='>'):
    text_list = text2text_list(text, begin, sep, end)
    return ''.join(decode_list(text_list, begin, sep, end))


def decode_list(text_list, begin='#', sep='<', end='>'):
    state = 0
    result = []
    candidate_buffer = []
    pronunciation = []
    pronunciation_string = str()

    def check_jukujikun(candidate_buffer, pronunciation_string):
        if pronunciation_string not in jukujikun_database:
            return None
        jukujikuns = jukujikun_database[pronunciation_string]
        for jukujikun in jukujikuns:
            for kanjis in itertools.product(*candidate_buffer):
                if ''.join(kanjis) == jukujikun:
                    return jukujikun
        return None

    def check_candidate(candidate_buffer, pronunciation_string):
        converter = mozcpy.Converter()
        outputs = converter.convert(pronunciation_string, 10)
        for output in outputs:
            for kanjis in itertools.product(*candidate_buffer):
                if ''.join(kanjis) == output:
                    return output
        return None

    def check_yomikata(candidate_buffer, pronunciation_string):
        for kanjis in itertools.product(*candidate_buffer):
            for pronunciations in itertools.product(*(yomikata_database[kanji]
                                                      if kanji in yomikata_database else kanji
                                                      for kanji in kanjis)):
                if all(pronunciation in pronunciation_string for pronunciation in pronunciations):
                    return ''.join(kanjis)
        return None

    for item in text_list:
        if item == begin:
            state = 1
            continue
        elif item == sep:
            state = 2
            pronunciation_string = ''.join(pronunciation)
            continue
        elif item == end:
            state = 0
            # detect jukujikun
            jukujikun = check_jukujikun(
                candidate_buffer, pronunciation_string)
            candidate = check_candidate(
                candidate_buffer, pronunciation_string)
            yomikata = check_yomikata(
                candidate_buffer, pronunciation_string)
            if jukujikun is not None:
                result.append(jukujikun)
            elif candidate is not None:
                result.append(candidate)
            elif yomikata is not None:
                result.append(yomikata)
            else:
                result += pronunciation
                # result += [candidate[0] for candidate in candidate_buffer]
            pronunciation.clear()
            pronunciation_string = str()
            candidate_buffer.clear()
            continue
        match state:
            case 0:
                result.append(item)
            case 1:
                pronunciation.append(item)
            case 2:
                candidate_buffer.append(text2zhengma.code2word(item))
    return result
