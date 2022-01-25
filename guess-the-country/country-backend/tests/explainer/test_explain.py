import pytest
from country.explainer import explain
import cv2
from country.model import predict
import uuid

def test_that_an_explanation_is_converted(generate_image):
    image = generate_image(224, 224)/255
    base = explain.convert_explanation(image)

    assert type(base) is bytes

def test_whole_explanation_process(generate_base64):
    base64 = generate_base64()
    explanation_test = explain.explain(base64)
    assert type(explanation_test) is explain.Explanation
    assert type(explanation_test.explanation_id) is uuid.UUID
    assert explanation_test.image[:22] == bytes("data:image/png;base64,", encoding='utf-8')


