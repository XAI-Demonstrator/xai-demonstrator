import json
import logging
from pathlib import Path
from typing import Dict, List


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

