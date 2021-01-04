from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers.modeling_bert import BertForSequenceClassification
from transformers.tokenization_bert import BertTokenizer

my_model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
my_tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment", use_fast=True)

my_model.save_pretrained("/app/model/saved_model")
my_tokenizer.save_pretrained("/app/model/saved_model")
