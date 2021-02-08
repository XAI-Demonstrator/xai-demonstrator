import pytest
import torch

from sentiment.explainer import explainer
from sentiment.explainer.explainers import gradient_shap
from sentiment.model.model import bert


@pytest.mark.integration
def test_gradient_shap():
    text = "This movie was boring :-("

    result = explainer.explain(text=text, target=4, explainer="gradient_shap")

    assert len(result.explanation) == 7
    assert result.explanation[0][0] == "This"
    assert result.explanation[4][0] == ":"
    assert "delta" in result.meta


@pytest.mark.integration
def test_that_partial_model_is_faithful():

    model = bert.model
    tokenizer = bert.tokenizer

    def full_forward(model_input):
        pred = model(model_input)
        return torch.softmax(pred[0], dim=1)

    partial_forward, _ = gradient_shap.create_partial_model(model)

    for text in ["This movie was boring :-(",
                 "Die Sonne hat gelacht, was für ein Tag!",
                 "Leider war der Urlaub zu schnell vorbei..."]:
        model_input = torch.tensor([tokenizer.encode(text, add_special_tokens=False)],
                                   dtype=torch.int64)

        embedded_input = model.bert.embeddings(model_input)

        assert torch.all(torch.eq(full_forward(model_input), partial_forward(embedded_input)))
