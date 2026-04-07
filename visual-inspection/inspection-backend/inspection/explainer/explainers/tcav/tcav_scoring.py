from typing import Dict, List, Tuple

import numpy as np

EPSILON = 1e-8


def compute_concept_scores(acts_flat: np.ndarray, cavs: Dict[str, np.ndarray]) -> Dict[str, float]:
    """Compute one score per concept, keeping the best score across random counterparts."""
    concept_scores: Dict[str, float] = {}
    acts_norm = float(np.linalg.norm(acts_flat))

    for key, cav in cavs.items():
        concept_name = key.split("__vs__", maxsplit=1)[0]
        cav_flat = cav.reshape(-1)
        cav_norm = float(np.linalg.norm(cav_flat))
        score = float(np.dot(acts_flat, cav_flat)) / (acts_norm * cav_norm + EPSILON)

        previous_score = concept_scores.get(concept_name)
        concept_scores[concept_name] = score if previous_score is None else max(previous_score, score)

    return concept_scores


def rank_concept_scores(concept_scores: Dict[str, float], *, by_absolute_value: bool = True) -> List[Tuple[str, float]]:
    """Rank concept scores either by absolute strength or by raw score."""
    sort_key = (lambda item: abs(item[1])) if by_absolute_value else (lambda item: item[1])
    return sorted(concept_scores.items(), key=sort_key, reverse=True)

