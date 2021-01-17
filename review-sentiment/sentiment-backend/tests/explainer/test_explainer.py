import pytest
import torch

from sentiment.explainer.explainer import align_text
from sentiment.model.model import bert


@pytest.mark.integration
def test_simple_text_alignment():
    tokenizer = bert.tokenizer

    text = "Ein einfacher Satz."
    encoding = tokenizer.encode_plus(text, add_special_tokens=False)
    assert len(encoding["input_ids"]) == 5

    scores = torch.tensor([1.0] * len(encoding["input_ids"]))

    result = align_text(text, encoding, scores)

    assert len(result) == 4
    assert result[0] == ("Ein", 1.0)
    assert result[1] == ("einfacher", 1.0)
    assert result[2] == ("Satz", 1.0)
    assert result[3] == (".", 1.0)

