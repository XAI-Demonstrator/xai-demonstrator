import numpy as np
import tensorflow as tf


def preprocess_batch(batch: np.ndarray) -> np.ndarray:
    """Preprocess a batch of RGB images for the TCAV pipeline."""
    if batch.ndim != 4 or batch.shape[-1] < 3:
        raise ValueError(
            f"`preprocess_batch` expects shape (N, H, W, C) with C>=3 but got: {batch.shape}",
        )

    batch_rgb = batch[:, :, :, :3].astype("float32")
    resized = tf.image.resize(batch_rgb, size=(224, 224), method="bicubic")
    resized_np = resized.numpy().astype("float32")
    return tf.keras.applications.mobilenet_v2.preprocess_input(resized_np)
