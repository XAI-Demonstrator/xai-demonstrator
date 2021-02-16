from inspection import api

FULL_TYPED_SETTINGS = '''{"settings": {"explainer": {
                                        "int_compatible": "50",
                                         "float_compatible": "50.5",
                                         "bool_compatible": "false",
                                         "proper_bool": true,
                                         "str_only": "word",
                                         "proper_int": 10,
                                         "proper_float": 2.5}}}'''


def test_explanation_settings_parses_typed_values():
    s = api.ExplanationSettings.parse_raw(FULL_TYPED_SETTINGS)

    explainer = s.settings["explainer"]
    assert isinstance(explainer["int_compatible"], int)
    assert explainer["int_compatible"] == 50
    assert isinstance(explainer["float_compatible"], float)
    assert explainer["float_compatible"] == 50.5
    assert isinstance(explainer["str_only"], str)
    assert explainer["str_only"] == "word"
    assert isinstance(explainer["proper_int"], int)
    assert explainer["proper_int"] == 10
    assert isinstance(explainer["proper_float"], float)
    assert explainer["proper_float"] == 2.5
    assert isinstance(explainer["proper_bool"], bool)
    assert explainer["proper_bool"]
    assert isinstance(explainer["bool_compatible"], bool)
    assert not explainer["bool_compatible"]


def test_that_parsed_explanation_settings_are_compatible_to_explanation_request():
    s = api.ExplanationSettings.parse_raw(FULL_TYPED_SETTINGS)

    _ = api.ExplanationRequest(settings=s.settings)
