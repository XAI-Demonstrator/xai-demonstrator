
import os
import pathlib

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers.modeling_bert import BertForSequenceClassification
from transformers.tokenization_bert import BertTokenizer

PATH = pathlib.Path(__file__).parent


class _ObjectManager:
    """Lazy loading of model and tokenizer.

    Enables us to inject model and tokenizer as external dependencies,
    hence we can stub/mock them during testing to speed up test execution
    and prevent the CI pipeline from loading the huge files.
    """

    def __init__(self):
        self._model = None
        self._tokenizer = None

    @property
    def model(self) -> BertForSequenceClassification:
        if self._model is None:
            self._model = self.load_model()
        return self._model
    
    @property
    def tokenizer(self) -> BertTokenizer:
        if self._tokenizer is None:
            self._tokenizer = self.load_tokenizer()
        return self._tokenizer

    @staticmethod
    def load_model() -> BertForSequenceClassification:
        return AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment",
                                                                  cache_dir=PATH / "cache")

    @staticmethod
    def load_tokenizer() -> BertTokenizer:
        return AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment",
                                             cache_dir=PATH / "cache", use_fast=True)


get = _ObjectManager()
