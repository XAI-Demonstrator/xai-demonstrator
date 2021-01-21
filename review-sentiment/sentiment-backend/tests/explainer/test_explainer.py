import numpy as np
import pytest
import torch

import sentiment.explainer.explainer as explainer
from sentiment.model.model import bert


@pytest.mark.integration
def test_integrated_text_alignment():
    tokenizer = bert.tokenizer

    text = "Ein einfacher Satz."
    encoding = tokenizer.encode_plus(text, add_special_tokens=False)
    assert len(encoding["input_ids"]) == 5

    words = np.array(encoding.word_ids())
    scores = np.ones(len(encoding["input_ids"]))

    result = explainer.align_text(text, words, scores)

    assert len(result) == 4
    assert result[0] == ("Ein", 1.0)
    assert result[1] == ("einfacher", 1.0)
    assert result[2] == ("Satz", 1.0)
    assert result[3] == (".", 1.0)


def test_that_input_and_reference_are_generated():
    text_input_ids = [223, 123, 884, 56, 1233]
    ref_token_id = 12

    input_tensor, ref_tensor = explainer.construct_input_and_reference(text_input_ids, ref_token_id)

    assert input_tensor.dim() == 2
    assert input_tensor.shape[0] == 1
    assert input_tensor.shape[1] == 5

    assert ref_tensor.dim() == 2
    assert ref_tensor.shape[0] == 1
    assert ref_tensor.shape[1] == 5
    assert torch.all(torch.eq(ref_tensor, torch.tensor([[12, 12, 12, 12, 12]])))


def test_text_alignment_with_one_to_one_match():
    text = "We need this."
    # we get one score per word
    words = np.array([0, 1, 2, 3])
    scores = np.array([0.1, 0.2, 0.3, 0.4])

    result = explainer.align_text(text, words, scores)

    assert len(result) == 4
    assert result == [("We", 0.1), ("need", 0.2), ("this", 0.3), (".", 0.4)]


def test_text_alignment_with_many_to_one_match():
    text = "Some complicated words"
    # we get one score per syllable
    words = np.array([0, 1, 1, 1, 1, 2])
    scores = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])

    result = explainer.align_text(text, words, scores)

    assert len(result) == 3
    assert result == [("Some", 0.1), ("complicated", 0.35), ("words", 0.6)]


def test_that_punctuation_is_removed():
    attributions = [("this", 0.5), ("was", 0.2), ("great", 0.9), ("!", 0.2)]

    result = explainer.filter_attributions(attributions,
                                           remove_stopwords=False,
                                           remove_punctuation=True)
    assert len(result) == 4
    assert result[3] == ("!", 0.0)
    assert result == [("this", 0.5), ("was", 0.2), ("great", 0.9), ("!", 0.0)]


def test_that_stopwords_are_removed(mocker):
    mocker.patch.object(explainer, "STOPWORDS", ["was", "so"])

    attributions = [("this", 0.5), ("was", 0.2), ("SO", 0.4), ("great", 0.9), ("!", 0.2)]

    result = explainer.filter_attributions(attributions,
                                           remove_stopwords=True,
                                           remove_punctuation=False)

    assert len(result) == 5
    assert result[1] == ("was", 0.0)
    assert result[2] == ("SO", 0.0)
    assert result == [("this", 0.5), ("was", 0.0), ("SO", 0.0), ("great", 0.9), ("!", 0.2)]
