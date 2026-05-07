from inspection.explainer.explainers.tcav_ import TCAVAnalysis, TCAVConceptScore
from inspection.explainer.explainers.tcav_ import build_tcav_explanation_sentence, build_tcav_explanation_sentences, humanize_tcav_concept


def test_tcav_sentence_contains_top_concepts():
    analysis = TCAVAnalysis(
        ranked_concept_scores=[
            TCAVConceptScore(concept="form_concepts/round", score=0.71),
            TCAVConceptScore(concept="feature_concepts/has_handle", score=0.33),
            TCAVConceptScore(concept="feature_concepts/has_screen", score=0.21),
        ]
    )

    sentence_de = build_tcav_explanation_sentence(analysis, top_k=3, language="de")
    sentence_en = build_tcav_explanation_sentence(analysis, top_k=3, language="en")

    assert "runde Form" in sentence_de
    assert "Griff" in sentence_de
    assert "Bildschirm" in sentence_de
    assert "stark" in sentence_de
    assert "gestützt" in sentence_de

    assert "round form" in sentence_en
    assert "handle" in sentence_en
    assert "screen" in sentence_en
    assert "strong" in sentence_en
    assert "supported" in sentence_en


def test_tcav_sentence_fallback_when_no_concepts():
    analysis = TCAVAnalysis(ranked_concept_scores=[])
    sentence_de = build_tcav_explanation_sentence(analysis, language="de")
    sentence_en = build_tcav_explanation_sentence(analysis, language="en")

    assert "Kein Konzept erkennbar." in sentence_de
    assert "No concept identifiable." in sentence_en


def test_tcav_sentence_bundle_contains_both_languages():
    analysis = TCAVAnalysis(
        ranked_concept_scores=[
            TCAVConceptScore(concept="feature_concepts/has_lens", score=0.4),
        ]
    )

    sentences = build_tcav_explanation_sentences(analysis)

    assert set(sentences.keys()) == {"de", "en"}
    assert "Linse" in sentences["de"]
    assert "lens" in sentences["en"]


def test_humanize_tcav_concept_uses_fallback_for_unknown_keys():
    assert humanize_tcav_concept("feature_concepts/custom_pattern") == "custom pattern"
