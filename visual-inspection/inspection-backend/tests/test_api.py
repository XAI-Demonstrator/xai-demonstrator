from inspection import api


def test_explanation_request_parses_numeric_values():
    r = api.ExplanationRequest(settings={"int_compatible": "50",
                                         "float_compatible": "50.5",
                                         "str_only": "word",
                                         "proper_int": 10,
                                         "proper_float": 2.5})

    assert isinstance(r.settings["int_compatible"], int)
    assert r.settings["int_compatible"] == 50
    assert isinstance(r.settings["float_compatible"], float)
    assert r.settings["float_compatible"] == 50.5
    assert isinstance(r.settings["str_only"], str)
    assert r.settings["str_only"] == "word"
    assert isinstance(r.settings["proper_int"], int)
    assert r.settings["proper_int"] == 10
    assert isinstance(r.settings["proper_float"], float)
    assert r.settings["proper_float"] == 2.5
