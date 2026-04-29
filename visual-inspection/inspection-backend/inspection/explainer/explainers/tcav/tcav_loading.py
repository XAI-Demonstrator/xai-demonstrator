import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

from .tcav_models import CAVLoadEntry, TCAVExplainerConfiguration

LOGGER = logging.getLogger(__name__)


def read_cav_manifest_entries(cav_dir: str, manifest_filename: str) -> List[Dict[str, str]]:
    manifest_path = Path(cav_dir) / manifest_filename
    if not manifest_path.exists():
        return []

    try:
        with manifest_path.open("r", encoding="utf-8") as file_obj:
            payload = json.load(file_obj)
    except (OSError, json.JSONDecodeError) as exc:
        LOGGER.warning("[TCAV] Could not read manifest '%s' (%s).", manifest_path, exc)
        return []

    if isinstance(payload, dict):
        raw_entries = payload.get("entries", [])
    elif isinstance(payload, list):
        raw_entries = payload
    else:
        return []

    normalized_entries: List[Dict[str, str]] = []
    for raw in raw_entries:
        if not isinstance(raw, dict):
            continue

        concept = str(raw.get("concept", ""))
        random_concept = str(raw.get("random_concept", ""))
        bottleneck_layer = str(raw.get("bottleneck_layer", ""))
        filename = str(raw.get("filename", ""))

        if not concept or not random_concept or not bottleneck_layer or not filename:
            continue

        normalized_entries.append(
            {
                "concept": concept,
                "random_concept": random_concept,
                "bottleneck_layer": bottleneck_layer,
                "filename": filename,
            },
        )

    return normalized_entries


def _discover_concepts_from_root(concepts_root: str) -> Tuple[List[str], List[str]]:
    root = Path(concepts_root)
    if not concepts_root or not root.is_dir():
        return [], []

    random_root = root / "random_concepts"
    randoms = [f"random_concepts/{child.name}" for child in sorted(random_root.iterdir()) if
               child.is_dir()] if random_root.is_dir() else []

    concepts = [
        f"{group.name}/{child.name}"
        for group in sorted(root.iterdir())
        if group.is_dir() and group.name != "random_concepts"
        for child in sorted(group.iterdir())
        if child.is_dir()
    ]
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


def _build_fallback_entries(config: TCAVExplainerConfiguration) -> List[CAVLoadEntry]:
    entries: List[CAVLoadEntry] = []
    for concept in config.concepts or []:
        for random_concept in config.random_concepts or []:
            safe_concept = concept.replace("/", "_").replace("\\", "_")
            safe_random = random_concept.replace("/", "_").replace("\\", "_")
            filename = f"{safe_concept}__vs__{safe_random}__{config.bottleneck_layer}.npz"
            entries.append(
                CAVLoadEntry(
                    concept=concept,
                    random_concept=random_concept,
                    bottleneck_layer=config.bottleneck_layer,
                    filename=filename,
                    file_path=str(Path(config.cav_dir) / filename),
                ),
            )
    return entries


def _load_manifest_entries(config: TCAVExplainerConfiguration) -> List[CAVLoadEntry]:
    raw_entries = read_cav_manifest_entries(config.cav_dir, config.cav_manifest_filename)
    entries: List[CAVLoadEntry] = []

    for raw in raw_entries:
        # read_cav_manifest_entries already normalizes and validates entries
        bottleneck_layer = raw["bottleneck_layer"]
        if bottleneck_layer != config.bottleneck_layer:
            continue

        entries.append(
            CAVLoadEntry(
                concept=raw["concept"],
                random_concept=raw["random_concept"],
                bottleneck_layer=bottleneck_layer,
                filename=raw["filename"],
                file_path=str(Path(config.cav_dir) / raw["filename"]),
            ),
        )

    return entries


def load_cavs_for_config(config: TCAVExplainerConfiguration) -> Dict[str, np.ndarray]:
    resolved_config = config
    entries = _load_manifest_entries(config)

    if entries:
        LOGGER.info("[TCAV] Loaded %d CAV entries from manifest '%s'.", len(entries), config.cav_manifest_filename)
    else:
        resolved_config = _resolve_explainer_config(config)
        LOGGER.info(
            "[TCAV] Could not load manifest '%s'. Falling back to generated entry list.",
            resolved_config.cav_manifest_filename,
        )
        entries = _build_fallback_entries(resolved_config)

    cavs: Dict[str, np.ndarray] = {}
    missing_pairs = 0

    for entry in entries:
        if not Path(entry.file_path).exists():
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
        LOGGER.warning("[TCAV] Missing %d concept/random CAV files; continuing with available files.", missing_pairs)
    return cavs
