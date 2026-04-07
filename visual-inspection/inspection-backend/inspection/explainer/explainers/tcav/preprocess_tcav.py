import numpy as np
import tensorflow as tf
from PIL import Image


def preprocess_batch(batch: np.ndarray) -> np.ndarray:
    """Preprocess a batch of RGB images for the TCAV pipeline."""
    if batch.ndim != 4 or batch.shape[-1] < 3:
        raise ValueError(
            f"`preprocess_batch` expects shape (N, H, W, C) with C>=3 but got: {batch.shape}",
        )

    processed: list[np.ndarray] = []
    for img in batch:
        # Convert back to PIL for resizing to ensure consistent interpolation
        pil_img = Image.fromarray(img.astype("uint8"))
        pil_img = pil_img.resize((224, 224), Image.Resampling.BICUBIC)
        img_array = tf.keras.preprocessing.image.img_to_array(pil_img)

        # Ensure exactly three channels (RGB), drop any potential alpha channel
        img_array = img_array[:, :, :3]
        processed.append(img_array)

    batch_resized = np.stack(processed, axis=0).astype("float32")
    batch_preprocessed = tf.keras.applications.mobilenet_v2.preprocess_input(batch_resized)
    return batch_preprocessed
