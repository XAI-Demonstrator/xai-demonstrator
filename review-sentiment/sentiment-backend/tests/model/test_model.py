import uuid

import pytest
from transformers import BertForSequenceClassification, BertTokenizerFast

from sentiment.model.model import BertManager


def test_that_model_is_loaded_on_first_get_only(mocker):
    class MyBERT:
        pass

    bert = BertManager()
    loading_patch = mocker.patch.object(bert, 'load_model')
    loading_patch.return_value = MyBERT()

    assert bert._model is None

    model_1 = bert.model

    assert loading_patch.call_count == 1
    assert bert._model is loading_patch.return_value
    assert model_1 is loading_patch.return_value

    model_2 = bert.model

    assert loading_patch.call_count == 1
    assert model_2 is loading_patch.return_value


def test_that_tokenizer_is_loaded_on_first_get_only(mocker):
    class MyTokenizer:

        def __init__(self):
            self.my_id = str(uuid.uuid4())

        def __eq__(self, other):
            return self.my_id == other.my_id

    bert = BertManager()
    loading_patch = mocker.patch.object(bert, 'load_tokenizer')
    loading_patch.return_value = MyTokenizer()

    assert bert._tokenizer is None

    tokenizer_1 = bert.tokenizer

    assert loading_patch.call_count == 1
    assert bert._tokenizer is loading_patch.return_value
    assert tokenizer_1 == loading_patch.return_value

    tokenizer_2 = bert.tokenizer

    assert loading_patch.call_count == 1
    assert tokenizer_2 == loading_patch.return_value


@pytest.mark.integration
def test_that_model_is_loaded(mocker):
    bert = BertManager()
    loading_spy = mocker.spy(bert, 'load_model')

    assert bert._model is None

    model = bert.model

    assert isinstance(model, BertForSequenceClassification)
    assert bert._model is not None
    assert loading_spy.call_count == 1


@pytest.mark.integration
def test_that_tokenizer_is_loaded(mocker):
    bert = BertManager()
    loading_spy = mocker.spy(bert, 'load_tokenizer')

    assert bert._tokenizer is None

    tokenizer = bert.tokenizer

    assert isinstance(tokenizer, BertTokenizerFast)
    assert bert._tokenizer is not None
    assert loading_spy.call_count == 1
