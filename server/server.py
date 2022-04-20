import os
import sys
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from tensorflow.python.util import deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER

from flask import Flask, request
app = Flask(__name__)

ws = WS("./data")
pos = POS("./data")
ner = NER("./data")

async def cutWordsAll(raw_words):

    sentence_list = [str(raw_words)]

    word_sentence_list = ws(sentence_list)
    pos_sentence_list = pos(word_sentence_list)
    entity_sentence_list = ner(word_sentence_list, pos_sentence_list)

    # Show results
    def print_word_pos_sentence(word_sentence, pos_sentence):
        result = 'pos'
        assert len(word_sentence) == len(pos_sentence)
        for word, pos in zip(word_sentence, pos_sentence):
            result += f"{word}({pos}),"
        result += ''
        return result

    for i, sentence in enumerate(sentence_list):
        pos_result = print_word_pos_sentence(word_sentence_list[i],  pos_sentence_list[i])
        ner_words = ''
        for entity in sorted(entity_sentence_list[i]):
            ner_words += f"{entity},"
    return {'pos':pos_result ,'ner':ner_words}

@app.route("/cutWords",methods=['POST'])
async def cutWords():
    print('cut beginning.')
    rawDatas = request.get_json()
    data = await cutWordsAll(rawDatas['raw_words'])
    return data

if __name__ == "__main__":
    app.run(host='0.0.0.0')