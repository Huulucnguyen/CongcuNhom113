import os
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from official.nlp import bert
import official.nlp.bert.tokenization as tokenization
from .crawl import get_list
encoder_fname = 'twitter_classes.npy'
my_wd = 'D:\DjangoAPI'
model_fname = 'BERT'

def predict(lst_cmt):
    #lst_cmt = get_list("https://shopee.vn/Qu%E1%BA%A7n-%C3%82u-Chi%E1%BA%BFt-Ly-20AGAIN-QAA0985-i.106719091.9413140222")
    #lst_cmt = [['The abdomen feels a bit tight and the pants are wider than the beautiful model photo'],['Nice form'], ['Nice pants fast delivery'], ['Pants fit but long tube has to be cut in white, but the fabric is not too thin to wear not exposed. Close the button, the locking edge is a bit tight, so give 4 * only.'], ['Pretty pretty pants up shape'], ["I'm 1m58 48kg tall, wearing S size, pretty soft pants are pretty soft"], ['The pants are a bit thin, they do not stand in the shape of the pants'], ['Nice quality shirt sir']]
    tot = 0
    xau = 0
    lst_predict = []
    tokenizerSaved = bert.tokenization.FullTokenizer(
    vocab_file=os.path.join(my_wd, model_fname, 'assets/vocab.txt'),
    do_lower_case=False)
    bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_multi_cased_L-12_H-768_A-12/2",trainable=True)
    vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
    do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
    tokenizer = tokenization.FullTokenizer(vocab_file, do_lower_case)
    model = tf.keras.models.load_model(os.path.join(my_wd, model_fname))
    loai = np.array([0,4])
    for i in lst_cmt:
        inputs = bert_encode(string_list=list(i), 
                     tokenizer=tokenizerSaved, 
                     max_seq_length=240)
        prediction = model.predict(inputs)
        if loai[np.argmax(prediction)]==4:
            tot +=1
        else:
            xau +=1
    lst_predict.append(tot)
    lst_predict.append(xau)
    return lst_predict
def encode_names(n, tokenizer):
   tokens = list(tokenizer.tokenize(n))
   tokens.append('[SEP]')
   return tokenizer.convert_tokens_to_ids(tokens)

def bert_encode(string_list, tokenizer, max_seq_length):
  num_examples = len(string_list)
  
  string_tokens = tf.ragged.constant([
      encode_names(n, tokenizer) for n in np.array(string_list)])

  cls = [tokenizer.convert_tokens_to_ids(['[CLS]'])]*string_tokens.shape[0]
  input_word_ids = tf.concat([cls, string_tokens], axis=-1)

  input_mask = tf.ones_like(input_word_ids).to_tensor(shape=(None, max_seq_length))

  type_cls = tf.zeros_like(cls)
  type_tokens = tf.ones_like(string_tokens)
  input_type_ids = tf.concat(
      [type_cls, type_tokens], axis=-1).to_tensor(shape=(None, max_seq_length))

  inputs = {
      'input_word_ids': input_word_ids.to_tensor(shape=(None, max_seq_length)),
      'input_mask': input_mask,
      'input_type_ids': input_type_ids}
  return inputs
