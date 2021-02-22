import pathlib
import threading
import copy
import logging

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, BertForSequenceClassification, \
    BertTokenizerFast
from xaidemo.tracing import traced

PATH = pathlib.Path(__file__).parent
my_device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class BertManager:
    """Lazy loading of model and tokenizer.

    Enables us to inject model and tokenizer as external dependencies,
    hence we can stub/mock them during testing to speed up test execution
    and prevent the CI pipeline from loading the huge files.
    """

    def __init__(self):
        self._model = None
        self._tokenizer = None
        self._loading_lock = threading.Lock()

        self.logger = logging.getLogger(__name__)

    @property
    def model(self) -> BertForSequenceClassification:
        if self._model is None:
            with self._loading_lock:
                self.logger.info("Acquired loading lock for model loading")
                if self._model is None:
                    self.logger.info("Loading model from disk...")
                    self._model = self.load_model()
                else:
                    self.logger.info("Model was loaded in the meantime")
        return self._model

    @property
    def tokenizer(self) -> BertTokenizerFast:
        if self._tokenizer is None:
            with self._loading_lock:
                self.logger.info("Acquired loading lock for tokenizer loading")
                if self._tokenizer is None:
                    self.logger.info("Loading tokenizer from disk...")
                    self._tokenizer = self.load_tokenizer()
                else:
                    self.logger.info("Tokenizer was loaded in the meantime")
        # Workaround for https://github.com/huggingface/tokenizers/issues/537
        return copy.deepcopy(self._tokenizer)

    @staticmethod
    @traced(attributes={"torch.device": str(my_device), "torch.device.type": my_device.type})
    def load_model() -> BertForSequenceClassification:
        model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment",
                                                                   cache_dir=PATH / "cache")
        model.to(my_device)
        return model

    @staticmethod
    @traced(attributes={"torch.device": str(my_device), "torch.device.type": my_device.type})
    def load_tokenizer() -> BertTokenizerFast:
        return AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment",
                                             cache_dir=PATH / "cache", use_fast=True)


bert = BertManager()
