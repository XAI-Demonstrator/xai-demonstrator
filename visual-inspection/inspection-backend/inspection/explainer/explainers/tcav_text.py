from typing import Any


TCAV_CONCEPT_LABELS = {
    "feature_concepts/circular_opening": "runde Oeffnung",
    "feature_concepts/has_handle": "Griff",
    "feature_concepts/has_keys_buttons": "Tasten und Knoepfe",
    "feature_concepts/has_lens": "Linse",
    "feature_concepts/has_screen": "Bildschirm",
    "form_concepts/compact_rounded": "kompakt und rund",
    "form_concepts/cylindrical": "zylindrische Form",
    "form_concepts/oval": "ovale Form",
    "form_concepts/rectangular": "rechteckige Form",
    "form_concepts/round": "runde Form",
}


def humanize_tcav_concept(concept: str) -> str:
    mapped = TCAV_CONCEPT_LABELS.get(concept)
    if mapped:
        return mapped

    fallback = concept.split("/", 1)[-1]
    fallback = fallback.replace("_", " ").strip()
    return fallback or concept


def _describe_score_strength(score: float) -> str:
    abs_score = abs(score)
    if abs_score >= 0.25:
        return "stark"
    if abs_score >= 0.15:
        return "mittel"
    return "schwach"


def _describe_score_direction(score: float) -> str:
    return "unterstuetzt" if score >= 0 else "spricht gegen"


def build_tcav_explanation_sentence(analysis: Any, top_k: int = 3) -> str:
    ranked = analysis.ranked_concept_scores[:max(1, top_k)]
    if not ranked:
        return "Ich kann kein klares Konzept erkennen, das diese Vorhersage erklaert."

    parts = []
    rank_text = ["Am wichtigsten ist", "Danach kommt", "Als drittes folgt"]

    for index, item in enumerate(ranked[:3]):
        prefix = rank_text[index] if index < len(rank_text) else "Ausserdem gibt es"
        parts.append(
            f"{prefix} '{humanize_tcav_concept(item.concept)}'. "
            f"Es {_describe_score_direction(item.score)} die Vorhersage ({_describe_score_strength(item.score)})."
        )

    return " ".join(parts)

