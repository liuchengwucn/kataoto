import encode
import decode

if __name__ == '__main__':
    text = '吾輩は猫である。名前はまだ無い。'

    # code = encode.encode_list(text)
    # print(code)
    # print(decode.decode_list(code))

    print('original: ', text)
    code = encode.encode(text)
    print('encoded: ', code)
    print('decoded: ', decode.decode(code))