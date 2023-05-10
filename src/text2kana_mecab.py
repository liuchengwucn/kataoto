import wanakana
import fugashi
import text2kana_kakasi
tagger = fugashi.Tagger()

def text2kana(text):
    pairs = text2pairs(text)
    result = []
    for orig, kana in pairs:
        if kana is None:
            # sometimes mecab don't return kana properly, such as '随証'
            # use kakasi instead
            if wanakana.is_kanji(orig):
                another_kana = text2kana_kakasi.text2hiragana(orig)
                result.append(another_kana)
                continue
            else:
                result.append(orig)
                continue
        result.append(kana)
    return result


def text2pairs(text: str):
    def segment2pairs(segment):
        pairs = []
        words = tagger(segment)
        for word in words:
            surface = word.surface
            kana = word.feature.kana
            if isinstance(kana, str) and kana != '*' and wanakana.is_japanese(surface):
                try:
                    hiragana = wanakana.to_hiragana(kana)
                    katakana = wanakana.to_katakana(kana)
                except:
                    pairs.append((surface, None))
                    continue
                if hiragana != surface and katakana != surface:
                    pairs.append((surface, hiragana))
                    continue
            pairs.append((surface, None))
        return pairs
    result = []
    meta_pairs = [segment2pairs(s) for s in text.split()]
    for i, pairs in enumerate(meta_pairs):
        if i != 0:
            result.append((' ', None))
        result.extend(pairs)
    return result

if __name__ == '__main__':
    print(text2kana('吾輩は猫である。'))

