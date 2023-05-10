# kataoto

kataoto stands for 音 (oto, vocal information or phonetic information) and 形 (katachi, visual information or glyphic information).

This is a repository offering model checkpoints and codes related to the encoding and decoding process described in the paper "*Japanese Sub-Character Tokenization Utilizing both Vocal and Visual Information*".
The paper proposed a sub-character tokenization algorithm which helps neural models understand Japanese text in a more natural way.

issueを英語で書く必要はありません。  
不必使用英语提出issue。

To install prerequisites, run the following command.

    pip install - r requirements.txt
    python -m unidic download
    
To get your hands dirty with some encoding and decoding examples, try `example.py`.

    $ python src/example.py
    original:  吾輩は猫である。名前はまだ無い。
    encoded:  #わがはい<bixj kcfk>は#ねこ<qmek>である。#なまえ<rsj uaqk>はまだ#ない<maeu い>。
    decoded:  吾輩は猫である。名前はまだ無い。

To explore our models in an interactive way, try `interact.py`. Enter a blank line to exit.

    $ python src/interact.py
    Please choose the type of the dataset.
    0 for jesc and 1 for aspec: 0 
    You chose jesc
    Please choose the type of the model.
    0 for encode and 1 for kana: 0
    You chose encode
    ...
    2023-05-10 08:58:09 | INFO | fairseq_cli.interactive | Type the input sentence and press return:
    日本語お上手ですね
    2023-05-10 08:58:17 | INFO | fairseq.tasks.fairseq_task | can_reuse_epoch_itr = True
    2023-05-10 08:58:17 | INFO | fairseq.tasks.fairseq_task | reuse_dataloader = True
    2023-05-10 08:58:17 | INFO | fairseq.tasks.fairseq_task | rebuild_batches = False
    2023-05-10 08:58:17 | INFO | fairseq.tasks.fairseq_task | creating new batches for epoch 1
    S-0     # にっぽん < ka favv > # ご < sbxj > お # じょうず < ida md > です ね
    W-0     0.156   seconds
    H-0     -0.7305049300193787     you speak very good japanese .
    D-0     -0.7305049300193787     you speak very good japanese .
    P-0     -0.9716 -0.7284 -1.3580 -0.6123 -0.4469 -0.8214 -0.1750

    Goodbye!
    2023-05-10 08:58:25 | INFO | fairseq_cli.interactive | Total time: 17.218 seconds; translation time: 0.156

All the codes and model checkpoints are available under the MIT license.
