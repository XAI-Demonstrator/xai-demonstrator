import numpy as np
import tensorflow as tf
from PIL import Image

def preprocess_batch(batch: np.ndarray) -> np.ndarray:
    if batch.ndim != 4 or batch.shape[-1] < 3:
        raise ValueError(
            f"`preprocess_batch` expects shape (N, H, W, C) with C>=3 but got: {batch.shape}"
        )

    processed = []
    for img in batch:
        pil_img = Image.fromarray(img.astype("uint8"))
        pil_img = pil_img.resize((224, 224), Image.Resampling.BICUBIC)
        img_array = tf.keras.preprocessing.image.img_to_array(pil_img)
        img_array = img_array[:, :, :3]
        processed.append(img_array)

    batch_resized = np.stack(processed, axis=0)
    batch_preprocessed = tf.keras.applications.mobilenet_v2.preprocess_input(batch_resized)
    return batch_preprocessed
