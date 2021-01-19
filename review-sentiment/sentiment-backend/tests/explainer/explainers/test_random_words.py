import pytest
import torch

from sentiment.explainer import explainer
from sentiment.explainer.explainers import random_words


def test_that_random_scores_are_generated():
    text_input_ids = torch.Tensor([[11, 22, 33, 44, 55, 66, 77, 88, 99]])

    class MyModel:
        pass

    result = random_words.attribute_random_words(text_input_ids,
                                                 model=MyModel(),
                                                 random_kwarg=None)

    assert result[1] is None
    assert result[0].shape == (9,)


@pytest.mark.integration
def test_random_explainer():
    text = "This movie was boring :-("

    result = explainer.explain(text=text, target=4, explainer="random")

    assert len(result.explanation) == 7
    assert result.explanation[0][0] == "This"
    assert result.explanation[5][0] == "-"
    assert result.meta is None
