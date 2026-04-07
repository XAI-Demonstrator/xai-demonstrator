from __future__ import annotations

import os
from glob import glob
from typing import Callable, Dict, Iterable, Sequence, Tuple

import numpy as np
import tensorflow as tf
from sklearn.linear_model import LogisticRegression

# Type alias for a batch preprocessing function to make signatures clearer
PreprocessFn = Callable[[np.ndarray], np.ndarray]


def _load_and_preprocess_images(
    image_paths: Sequence[str],
    preprocess_fn: PreprocessFn,
    target_size: Tuple[int, int] = (224, 224),
) -> np.ndarray:
    """Load images from disk, resize them to a common size and apply preprocessing.

    Parameters
    ----------
    image_paths:
        Iterable of file system paths pointing to image files.
    preprocess_fn:
        Function that takes a batch of images with shape (N, H, W, C) and
        returns a preprocessed batch compatible with the target model.
    target_size:
        Spatial target size (height, width) used when loading each image.

    Returns
    -------
    np.ndarray
        Preprocessed image batch of shape (N, H, W, C).
    """
    images: list[np.ndarray] = []

    for path in image_paths:
        try:
            print(f"[TCAV]   Loading image: {path}")
            # Ensure all images share a common spatial resolution and 3 channels (RGB)
            pil_img = tf.keras.utils.load_img(path, target_size=target_size)
            img_arr = tf.keras.utils.img_to_array(pil_img)
            images.append(img_arr)
        except Exception as exc:  # noqa: BLE001 - log and skip invalid files
            print(
                f"[TCAV]   WARNING: Could not load image '{path}' ({exc}); skipping this file.",
            )

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

    Parameters
    ----------
    concepts_root:
        Root folder under which all concept subfolders live.
    concept_name:
        Concept subfolder name, relative to ``concepts_root``.
    extensions:
        File patterns that are treated as valid image types.

    Returns
    -------
    list[str]
        Sorted list of absolute or relative paths to image files for the concept.
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
) -> Dict[str, str]:
    """Compute and persist CAVs for all combinations of concepts and random concepts.

    Returns a mapping from a logical key (``"<concept>__vs__<random>"``) to the
    path of the corresponding ``.npz`` file on disk.
    """
    os.makedirs(cav_output_dir, exist_ok=True)

    cav_files: Dict[str, str] = {}
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
            safe_concept = concept.replace("/", "_").replace("\\", "_")
            safe_rnd = rnd.replace("/", "_").replace("\\", "_")
            filename = f"{safe_concept}__vs__{safe_rnd}__{bottleneck_layer_name}.npz"
            filepath = os.path.join(cav_output_dir, filename)

            np.savez_compressed(filepath, cav=cav)
            cav_files[key] = filepath

            print(f"[TCAV] Saved: {filepath}")

    print(f"\n[TCAV] DONE. {len(cav_files)} CAV files created.")
    return cav_files

