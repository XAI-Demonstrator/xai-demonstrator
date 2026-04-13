from __future__ import annotations

import json
import os
from glob import glob
from pathlib import Path
from typing import Callable, Dict, Iterable, Sequence, Tuple

import numpy as np
import tensorflow as tf
from sklearn.linear_model import LogisticRegression

# Type alias for a batch preprocessing function to make signatures clearer
PreprocessFn = Callable[[np.ndarray], np.ndarray]


def _sanitize_name(value: str) -> str:
    return value.replace("/", "_").replace("\\", "_")


def _discover_known_concepts(concepts_root: str) -> tuple[list[str], list[str]]:
    """Discover concept and random concept ids from the concept root directory."""
    root = Path(concepts_root)
    concepts: list[str] = []
    randoms: list[str] = []

    if not root.exists():
        return concepts, randoms

    random_root = root / "random_concepts"
    if random_root.is_dir():
        for child in sorted(random_root.iterdir()):
            if child.is_dir():
                randoms.append(f"random_concepts/{child.name}")

    for group_dir in sorted(root.iterdir()):
        if not group_dir.is_dir() or group_dir.name == "random_concepts":
            continue
        for child in sorted(group_dir.iterdir()):
            if child.is_dir():
                concepts.append(f"{group_dir.name}/{child.name}")

    return concepts, randoms


def _build_manifest_entries_from_npz(
    cav_output_dir: str,
    concepts_root: str,
) -> list[dict[str, str]]:
    """Rebuild manifest entries from files on disk to avoid dropping existing CAVs."""
    concepts, randoms = _discover_known_concepts(concepts_root)
    concept_map = {_sanitize_name(c): c for c in concepts}
    random_map = {_sanitize_name(r): r for r in randoms}

    entries: list[dict[str, str]] = []
    for npz_path in sorted(Path(cav_output_dir).glob("*.npz")):
        stem = npz_path.stem
        try:
            safe_pair, bottleneck_layer = stem.rsplit("__", maxsplit=1)
            safe_concept, safe_random = safe_pair.split("__vs__", maxsplit=1)
        except ValueError:
            print(f"[TCAV] WARNING: Could not parse CAV filename '{npz_path.name}' for manifest rebuild.")
            continue

        concept = concept_map.get(safe_concept)
        random_concept = random_map.get(safe_random)
        if concept is None or random_concept is None:
            print(
                "[TCAV] WARNING: Could not map filename back to concept names for "
                f"'{npz_path.name}'. Skipping this file in manifest.",
            )
            continue

        entries.append(
            {
                "concept": concept,
                "random_concept": random_concept,
                "bottleneck_layer": bottleneck_layer,
                "filename": npz_path.name,
            },
        )

    return entries


def _load_and_preprocess_images(
    image_paths: Sequence[str],
    preprocess_fn: PreprocessFn,
    target_size: Tuple[int, int] = (224, 224),
) -> np.ndarray:
    """Load images from disk, resize them to a common size and apply preprocessing.
        -> Preprocessed image batch of shape (N, H, W, C).
    """
    images: list[np.ndarray] = []
    total = len(image_paths)

    if total == 0:
        print("[TCAV]   No image paths provided - returning empty array.")
        return np.empty((0,), dtype="float32")

    print(f"[TCAV]   Loading and preprocessing {total} images ...")

    for idx, path in enumerate(image_paths, start=1):
        try:
            # Ensure all images share a common spatial resolution and 3 channels (RGB)
            pil_img = tf.keras.utils.load_img(path, target_size=target_size)
            img_arr = tf.keras.utils.img_to_array(pil_img)
            images.append(img_arr)
        except Exception as exc:  # noqa: BLE001 - log and skip invalid files
            print(
                f"[TCAV]   WARNING: Could not load image '{path}' ({exc}); skipping this file.",
            )

        if idx % 10 == 0 or idx == total:
            print(f"[TCAV]     Loaded {idx}/{total} images...")

    if not images:
        print("[TCAV]   No valid images found - returning empty array.")
        return np.empty((0,), dtype="float32")

    batch = np.stack(images, axis=0).astype("float32")
    print(f"[TCAV]   Raw batch shape before preprocessing: {batch.shape}")

    batch = preprocess_fn(batch)
    print(f"[TCAV]   Batch shape after preprocessing: {batch.shape}")

    return batch


def _list_concept_image_paths(
    concepts_root: str,
    concept_name: str,
    extensions: Tuple[str, ...] = ("*.png", "*.jpg", "*.jpeg"),
) -> list[str]:
    """Collect all image file paths for a given concept.
        --> Sorted list of absolute or relative paths to image files for the concept.
    """
    concept_dir = os.path.join(concepts_root, concept_name)
    paths: list[str] = []

    for ext in extensions:
        paths.extend(glob(os.path.join(concept_dir, ext)))

    paths = sorted(paths)

    print(f"[TCAV] Concept '{concept_name}': {len(paths)} images found in '{concept_dir}'.")

    return paths


def compute_cav_for_concept(
    model: tf.keras.Model,
    bottleneck_layer_name: str,
    concepts_root: str,
    concept: str,
    random_concept: str,
    preprocess_fn: PreprocessFn,
    *,
    C: float = 0.01,
    max_iter: int = 1000,
) -> np.ndarray:
    """Compute a Concept Activation Vector (CAV) for one (concept, random) pair.

    A linear classifier is trained to separate activations of the target concept
    from activations of a random concept in the chosen bottleneck layer. The
    learned weight vector is interpreted as the CAV.
    """
    print(f"\n[TCAV] === Calculate CAV: '{concept}' vs. '{random_concept}' ===")
    print(f"[TCAV] Using bottleneck layer: '{bottleneck_layer_name}'")

    # 1) Create auxiliary model that outputs the bottleneck layer.
    try:
        bottleneck_layer = model.get_layer(bottleneck_layer_name).output
    except ValueError as exc:  # noqa: PERF203 - single explicit error path is fine here
        available = [layer.name for layer in model.layers]
        raise ValueError(
            f"Layer '{bottleneck_layer_name}' does not exist. "
            f"Available layers: {available}",
        ) from exc

    bottleneck_model = tf.keras.Model(inputs=model.inputs, outputs=bottleneck_layer)
    print(f"[TCAV] Bottleneck model created. Output shape: {bottleneck_model.output_shape}")

    # 2) Load concept and random images
    concept_paths = _list_concept_image_paths(concepts_root, concept)
    random_paths = _list_concept_image_paths(concepts_root, random_concept)

    if not concept_paths:
        raise ValueError(f"No concept images '{concept}' found in {concepts_root}.")
    if not random_paths:
        raise ValueError(f"No random concept images '{random_concept}' found in {concepts_root}.")

    concept_imgs = _load_and_preprocess_images(concept_paths, preprocess_fn)
    random_imgs = _load_and_preprocess_images(random_paths, preprocess_fn)

    # 3) Compute bottleneck activations
    print(f"[TCAV]   Calculate bottleneck activations for concept '{concept}' ...")
    concept_acts = bottleneck_model.predict(concept_imgs, verbose=1)

    print(f"[TCAV]   Calculate bottleneck activations for random '{random_concept}' ...")
    random_acts = bottleneck_model.predict(random_imgs, verbose=1)

    # 4) Flatten concept and random activations into 2D feature matrices: [N, D]
    concept_flat = concept_acts.reshape((concept_acts.shape[0], -1))
    random_flat = random_acts.reshape((random_acts.shape[0], -1))

    X = np.concatenate([concept_flat, random_flat], axis=0)
    y = np.concatenate(
        [
            np.ones(concept_flat.shape[0], dtype=np.int32),
            np.zeros(random_flat.shape[0], dtype=np.int32),
        ],
        axis=0,
    )

    # 5) Train logistic regression classifier to separate concept vs. random in bottleneck space
    print(f"[TCAV] Start training LogisticRegression (C={C}, max_iter={max_iter}) ...")
    clf = LogisticRegression(C=C, max_iter=max_iter)
    clf.fit(X, y)
    print("[TCAV] LogisticRegression training finished.")

    # 6) Reshape coefficient vector back to bottleneck activation shape
    cav_flat = clf.coef_.reshape(concept_acts.shape[1:])
    print(f"[TCAV] CAV shape: {cav_flat.shape}")

    return cav_flat


def compute_and_store_cavs(
    model: tf.keras.Model,
    bottleneck_layer_name: str,
    concepts_root: str,
    concepts: Iterable[str],
    random_concepts: Iterable[str],
    cav_output_dir: str,
    preprocess_fn: PreprocessFn,
    *,
    C: float = 0.01,
    max_iter: int = 1000,
    manifest_filename: str = "cav_manifest.json",
) -> Dict[str, str]:
    """Compute and persist CAVs for all combinations of concepts and random concepts."""
    os.makedirs(cav_output_dir, exist_ok=True)

    cav_files: Dict[str, str] = {}
    manifest_entries: list[dict[str, str]] = []
    concept_list = list(concepts)
    random_list = list(random_concepts)
    total = len(concept_list) * len(random_list)
    idx = 0

    for concept in concept_list:
        for rnd in random_list:
            idx += 1
            print(f"\n[TCAV] ({idx}/{total}) Process concept pair: '{concept}' vs. '{rnd}'")

            key = f"{concept}__vs__{rnd}"
            cav = compute_cav_for_concept(
                model=model,
                bottleneck_layer_name=bottleneck_layer_name,
                concepts_root=concepts_root,
                concept=concept,
                random_concept=rnd,
                preprocess_fn=preprocess_fn,
                C=C,
                max_iter=max_iter,
            )

            # Sanitize concept names for safe file names (avoid path separators)
            safe_concept = _sanitize_name(concept)
            safe_rnd = _sanitize_name(rnd)
            filename = f"{safe_concept}__vs__{safe_rnd}__{bottleneck_layer_name}.npz"
            filepath = os.path.join(cav_output_dir, filename)

            np.savez_compressed(filepath, cav=cav)
            cav_files[key] = filepath
            manifest_entries.append(
                {
                    "concept": concept,
                    "random_concept": rnd,
                    "bottleneck_layer": bottleneck_layer_name,
                    "filename": filename,
                },
            )

            print(f"[TCAV] Saved: {filepath}")

    manifest_path = os.path.join(cav_output_dir, manifest_filename)
    rebuilt_entries = _build_manifest_entries_from_npz(cav_output_dir, concepts_root)
    if rebuilt_entries:
        manifest_entries = rebuilt_entries
    else:
        print("[TCAV] WARNING: Manifest rebuild from npz files yielded no entries; using in-memory entries.")

    manifest_payload = {
        "schema_version": 1,
        "entries": manifest_entries,
    }
    with open(manifest_path, "w", encoding="utf-8") as fp:
        json.dump(manifest_payload, fp, indent=2)
    print(f"[TCAV] Manifest saved: {manifest_path}")

    print(f"\n[TCAV] DONE. {len(cav_files)} CAV files created.")
    return cav_files

