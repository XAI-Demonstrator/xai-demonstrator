import pytest

from sentiment import api


def test_that_the_explainer_availability_check_works(mocker):
    mocker.patch.object(api, 'EXPLAINERS', ["existing"])

    good_exp_req = api.ExplanationRequest(text="some text",
                                          target=3,
                                          method="existing")
    with pytest.raises(ValueError):
        bad_exp_req = api.ExplanationRequest(text="some text",
                                             target=3,
                                             method="unavailable")


def test_that_loading_is_triggered(mocker):
    bert_loader = mocker.patch.object(api.bert, "load")

    api.load()

    assert bert_loader.call_count == 1
