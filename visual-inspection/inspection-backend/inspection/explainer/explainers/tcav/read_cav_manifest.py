import json
import os
from typing import Dict, List


def read_cav_manifest_entries(cav_dir: str, manifest_filename: str) -> List[Dict[str, str]]:
    """Read and normalize CAV manifest entries."""
    manifest_path = os.path.join(cav_dir, manifest_filename)
    if not os.path.exists(manifest_path):
        return []

    try:
        with open(manifest_path, "r", encoding="utf-8") as file_obj:
            payload = json.load(file_obj)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[TCAV] WARNING: Could not read manifest '{manifest_path}' ({exc}).")
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

