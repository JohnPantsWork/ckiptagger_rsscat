import os
import sys
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from tensorflow.python.util import deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER

# from fs import open_fs
# my_fs = open_fs('.')

from flask import Flask, request
app = Flask(__name__)

async def cutWords(raw_words):
    # Download data
    # data_utils.download_data("./")

    # Load model without GPU
    ws = WS("./data")
    pos = POS("./data")
    # ner = NER("./data")

    # Load model with GPU
    # ws = WS("./data", disable_cuda=False)
    # pos = POS("./data", disable_cuda=False)
    # ner = NER("./data", disable_cuda=False)

    # Create custom dictionary
    word_to_weight = {
        # "word": 1,
    }
    dictionary = construct_dictionary(word_to_weight)
    print(dictionary)

    # Run WS-POS-NER pipeline

    sentence_list = [
        str(raw_words)
    ]
    word_sentence_list = ws(sentence_list)
    # word_sentence_list = ws(sentence_list, sentence_segmentation=True)
    # word_sentence_list = ws(sentence_list, recommend_dictionary=dictionary)
    # word_sentence_list = ws(sentence_list, coerce_dictionary=dictionary)
    pos_sentence_list = pos(word_sentence_list)
    # entity_sentence_list = ner(word_sentence_list, pos_sentence_list)

    # Release model
    del ws
    del pos
    #del ner

    str word_pos_pairs_s
    # Show results
    def print_word_pos_sentence(word_sentence, pos_sentence):
        assert len(word_sentence) == len(pos_sentence)
        word_pos_pairs=''
        for word, pos in zip(word_sentence, pos_sentence):
            word_pos_pairs.append('f"{word}({pos}),"')
        word_pos_pairs_s = ''.join(word_pos_pairs)
    
    return word_pos_pairs_s

    # for i, sentence in enumerate(sentence_list):
    #    print()
    #    print(f"'{sentence}'")
    #    print_word_pos_sentence(word_sentence_list[i],  pos_sentence_list[i])
    #    for entity in sorted(entity_sentence_list[i]):
    #        print(entity)
    #        my_fs.appendtext('output.txt',str(entity),'UTF-8')
    # return
    # my_fs.close()

@app.route("/cutwords",methods=['POST'])
async def cutwords():
    print('cutwords beginning.')
    rawDatas = request.get_json()
    data = await cutWords(rawDatas['raw_words'])
    return {'data':rawDatas}

if __name__ == "__main__":
    app.run(host='0.0.0.0')