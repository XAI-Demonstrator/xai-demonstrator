import os
from typing import Dict, List, Tuple

import numpy as np

from .read_cav_manifest import read_cav_manifest_entries
from .tcav_models import CAVLoadEntry, TCAVExplainerConfiguration


def _discover_concepts_from_root(concepts_root: str) -> Tuple[List[str], List[str]]:
    concepts: List[str] = []
    randoms: List[str] = []

    if not concepts_root:
        return concepts, randoms
    if not os.path.isdir(concepts_root):
        return concepts, randoms

    random_root = os.path.join(concepts_root, "random_concepts")
    if os.path.isdir(random_root):
        for child in sorted(os.listdir(random_root)):
            child_path = os.path.join(random_root, child)
            if os.path.isdir(child_path):
                randoms.append(f"random_concepts/{child}")

    for group in sorted(os.listdir(concepts_root)):
        if group == "random_concepts":
            continue
        group_path = os.path.join(concepts_root, group)
        if not os.path.isdir(group_path):
            continue
        for child in sorted(os.listdir(group_path)):
            child_path = os.path.join(group_path, child)
            if os.path.isdir(child_path):
                concepts.append(f"{group}/{child}")

    return concepts, randoms


def _resolve_explainer_config(config: TCAVExplainerConfiguration) -> TCAVExplainerConfiguration:
    concepts = config.concepts
    randoms = config.random_concepts
    concepts_root = config.concepts_root or ""

    if concepts is None or randoms is None:
        discovered_concepts, discovered_randoms = _discover_concepts_from_root(concepts_root)
        if concepts is None:
            concepts = discovered_concepts
        if randoms is None:
            randoms = discovered_randoms

    if not concepts:
        raise ValueError(
            "No concepts configured or discovered. Provide explainer.concepts or a valid concepts_root.",
        )
    if not randoms:
        raise ValueError(
            "No random concepts configured or discovered. Provide explainer.random_concepts or random_concepts/*.",
        )

    update_data = {"concepts": concepts, "random_concepts": randoms}
    return config.model_copy(update=update_data)

def _load_manifest_entries(config: TCAVExplainerConfiguration) -> List[CAVLoadEntry]:
    raw_entries = read_cav_manifest_entries(config.cav_dir, config.cav_manifest_filename)
    entries: List[CAVLoadEntry] = []

    for raw in raw_entries:
        concept = str(raw.get("concept", ""))
        random_concept = str(raw.get("random_concept", ""))
        bottleneck_layer = str(raw.get("bottleneck_layer", ""))
        filename = str(raw.get("filename", ""))

        if not concept or not random_concept or not bottleneck_layer or not filename:
            continue
        if bottleneck_layer != config.bottleneck_layer:
            continue

        entries.append(
            CAVLoadEntry(
                concept=concept,
                random_concept=random_concept,
                bottleneck_layer=bottleneck_layer,
                filename=filename,
                file_path=os.path.join(config.cav_dir, filename),
            ),
        )

    return entries


def load_cavs_for_config(config: TCAVExplainerConfiguration) -> Dict[str, np.ndarray]:
    entries = _load_manifest_entries(config)

    if entries:
        print(f"[TCAV] Loaded {len(entries)} CAV entries from manifest '{config.cav_manifest_filename}'.")
    else:
        resolved_config = _resolve_explainer_config(config)
        print(
            f"[TCAV] Could not load manifest '{resolved_config.cav_manifest_filename}'. "
            "Falling back to generated entry list.",
        )
        entries = _build_fallback_entries(resolved_config)

    cavs: Dict[str, np.ndarray] = {}
    missing_pairs = 0

    for entry in entries:
        if not os.path.exists(entry.file_path):
            missing_pairs += 1
            continue
        with np.load(entry.file_path) as data:
            key = f"{entry.concept}__vs__{entry.random_concept}"
            cavs[key] = data["cav"]

    if not cavs:
        raise FileNotFoundError(
            f"No CAVs found in '{resolved_config.cav_dir}' for bottleneck '{resolved_config.bottleneck_layer}'.",
        )
    if missing_pairs:
        print(f"[TCAV] Missing {missing_pairs} concept/random CAV files; continuing with available files.")
    return cavs

