from inspection.explainer.explainers.tcav_ import TCAVAnalysis, TCAVConceptScore
from inspection.explainer.explainers.tcav_ import build_tcav_explanation_sentence, humanize_tcav_concept


def test_tcav_sentence_contains_top_concepts():
    analysis = TCAVAnalysis(
        ranked_concept_scores=[
            TCAVConceptScore(concept="form_concepts/round", score=0.71),
            TCAVConceptScore(concept="feature_concepts/has_handle", score=0.33),
            TCAVConceptScore(concept="feature_concepts/has_screen", score=0.21),
        ]
    )

    sentence = build_tcav_explanation_sentence(analysis, top_k=3)

    assert "runde Form" in sentence
    assert "Griff" in sentence
    assert "Bildschirm" in sentence
    assert "stark" in sentence
    assert "Am wichtigsten" in sentence


def test_tcav_sentence_fallback_when_no_concepts():
    analysis = TCAVAnalysis(ranked_concept_scores=[])

    sentence = build_tcav_explanation_sentence(analysis)

    assert "kein klares Konzept" in sentence


def test_humanize_tcav_concept_uses_fallback_for_unknown_keys():
    assert humanize_tcav_concept("feature_concepts/custom_pattern") == "custom pattern"
