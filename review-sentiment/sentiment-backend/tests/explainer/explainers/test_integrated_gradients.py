import pytest

from sentiment.explainer import explainer


@pytest.mark.integration
def test_integrated_gradients():
    text = "This movie was boring :-("

    result = explainer.explain(text=text, target=4, explainer="integrated_gradients")

    assert len(result.explanation) == 7
    assert result.explanation[0][0] == "This"
    assert result.explanation[4][0] == ":"
    assert "delta" in result.meta
