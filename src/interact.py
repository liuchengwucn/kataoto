from subprocess import Popen, PIPE
import encode
from time import sleep
import text2kana_mecab
    
if __name__ == '__main__':
    data_type = input('Please choose the type of the dataset.\n0 for jesc and 1 for aspec: ')
    match data_type:
        case '0':
            data_type = 'jesc'
        case '1':
            data_type = 'aspec'
        case _:
            data_type = 'jesc'
    print('you choosed', data_type)
    
    model_type = input('Please choose the type of the model.\n0 for encode and 1 for kana: ')
    match model_type:
        case '0':
            model_type = 'encode'
        case '1':
            model_type = 'kana'
        case _:
            model_type = 'encode'
    print('you choosed', model_type)

    pt_path = f'model/{data_type}_{model_type}/model.pt'
    dict_path = f'model/{data_type}_{model_type}'
    bpe_codes_path = f'{dict_path}/bpecodes.ja'
    
    command = f'fairseq-interactive --path {pt_path} {dict_path} --beam 5 --source-lang ja --target-lang en --bpe subword_nmt --bpe-codes {bpe_codes_path}'
    p = Popen(command, stdin=PIPE, shell=True)

    while True:
        ja_text = input()
        
        if not ja_text:
            print('Goodbye!')
            sleep(1)
            p.stdin.close()
            break
    
        match model_type:
            case 'encode':
                encoded_text = ' '.join(encode.encode_list(ja_text))
            case 'kana':
                encoded_text = ' '.join(text2kana_mecab.text2kana(ja_text))
        
        p.stdin.write((encoded_text + '\n').encode())
        p.stdin.flush()
    