import encode
import decode

def process(text):
    code = encode.encode(text)
    print('encoded: ', code)
    print('decoded: ', decode.decode(code))

if __name__ == '__main__':
    text = '吾輩は猫である。名前はまだ無い。'
    print('original: ', text)

    # code = encode.encode_list(text)
    # print(code)
    # print(decode.decode_list(code))

    process(text)
    
    while True:
        text = input('original: ')
        if not text:
            print('Goodbye!')
            break
        process(text)