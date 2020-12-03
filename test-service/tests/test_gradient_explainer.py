import torch

from sentiment.explainer.gradient_explainer import merge_and_attribute, explain


def test_merge_and_attribute():
    merge_and_attribute(torch.tensor([1, 2, 3]), torch.tensor([-0.4, 0.3, 0.9]))


def test_explain():
    prediction = explain("Der Hund", target=4)
