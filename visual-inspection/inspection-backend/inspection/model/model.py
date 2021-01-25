import tensorflow as tf


# TODO: Replace with custom model variant
model = tf.keras.applications.MobileNetV2(input_shape=None,
                                          include_top=True,
                                          weights="imagenet")
