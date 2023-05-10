import text2kana_mecab
import text2zhengma
import opencc
import wanakana
import text2kana_kakasi

converter = opencc.OpenCC('t2jp.json')
def encode(text, begin='#', sep='<', end='>'):
    l = encode_list(text, begin, sep, end)
    state = 0
    temp = []
    for i, item in enumerate(l):
        if item == end:
            state = 0
        if state == 1 and l[i - 1] != sep:
            temp.append(' ' + item)
        else:
            temp.append(item)
        if item == sep:
            state = 1
    return ''.join(temp)

def encode_list(text, begin='#', sep='<', end='>'):
    # convert to 新字体
    text = converter.convert(text)
    pairs = text2kana_mecab.text2pairs(text)
    result = []
    for orig, kana in pairs:
        if kana is None:     
            if wanakana.is_kanji(orig):
                another_kana = text2kana_kakasi.text2hiragana(orig)
                flag = True
                # if kakasi still can't provide an valid kana, omit it
                for c in another_kana:
                    if wanakana.is_char_kanji(c):
                        flag = False
                        break
                if flag:
                    result.append(begin)
                    result.append(another_kana)
                    result.append(sep)
                    result.extend(text2zhengma.text2code(orig))
                    result.append(end)
                else:
                    result.append(orig)
                continue
            else:
                result.append(orig)
                continue
        result.append(begin)
        result.append(kana)
        result.append(sep)
        result.extend(text2zhengma.text2code(orig))
        result.append(end)
    return result

def encode_mt_list(text, begin='#', sep='<', end='>'):
    # convert to 新字体
    text = converter.convert(text)
    pairs = text2kana_mecab.text2pairs(text)
    result = []
    for orig, kana in pairs:
        if kana is None:
            # sometimes mecab don't return kana properly, such as '随証'
            # use kakasi instead
            if wanakana.is_kanji(orig):
                another_kana = text2kana_kakasi.text2hiragana(orig)
                flag = True
                # if kakasi still can't provide an valid kana, omit it
                for c in another_kana:
                    if wanakana.is_char_kanji(c):
                        flag = False
                        break
                if flag:
                    result.append(another_kana)
                    codes = text2zhengma.text2code_mt(orig)
                    codes = '#'.join(code for code in codes if len(code) != 0)
                    result.extend(codes)
                else:
                    result.append(orig)
                continue
            else:
                result.append(orig)
                continue
        result.append(kana)
        codes = text2zhengma.text2code_mt(orig)
        codes = '#'.join(code for code in codes if len(code) != 0)
        result.extend(codes)
    return result

if __name__ == '__main__':
    text = '吾輩は猫である'
    print(encode_mt_list(text))
    print(encode_list(text))
