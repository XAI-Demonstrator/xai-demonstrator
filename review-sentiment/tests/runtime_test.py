import requests
import numpy as np
import re
import string
import os
from tabulate import tabulate

#---------------------------------------------------------------------------------------
# TEST ROUTINE

def evaluate(review: str, nof_requests: int, bw_cloud: bool):
    #split_review = re.findall(r"[\w']+|" + f"[{string.punctuation}]", review)
    prediction_times = []
    # create dict for predict request
    predict_json = {"text": review}
    explanation_times = []

    for _ in range(nof_requests):
        # request prediction scores
        if bw_cloud:
            prediction_request = requests.post(bwc_predict_link, json=predict_json)
        else:
            prediction_request = requests.post(gc_predict_link, json=predict_json)
        # choose arg max as prediction
        prediction = np.argmax(prediction_request.json()['prediction'])
        prediction_times.append(prediction_request.elapsed.total_seconds())

        # create dict for explain request
        explain_json = {"text": review, "target": str(np.argmax(prediction)),
                        "explainer": "integrated_gradients"}
        # request explanation scores
        if bw_cloud:
            explanation_request = requests.post(bwc_explain_link, json=explain_json)
        else:
            explanation_request = requests.post(gc_explain_link, json=explain_json)
        explanation_times.append(explanation_request.elapsed.total_seconds())
    # print results

    if bw_cloud:
        cloud_name = "(BW Cloud)"
        print("evaluation of review: ")
        print(review)
    else:
        cloud_name = "(Google Cloud)"
    print("prediction time " + cloud_name + " - mean: " + str(np.mean(prediction_times[1:])) +
               ", std: " + str(np.std(prediction_times[1:])))
    print("explanation time " + cloud_name + " - mean: " + str(np.mean(explanation_times[1:])) +
               ", std: " + str(np.std(explanation_times[1:])))
    print("prediction time " + cloud_name + " - first request: " + str(prediction_times[0]))
    print("explanation time " + cloud_name + " - first request: " + str(explanation_times[0]))
    if not bw_cloud:
        print("------------------------------------------------------------")

#---------------------------------------------------------------------------------------
# SET GLOBAL VARIABLES

nof_requests = 20

bwc_predict_link = "https://test.xaidemo.de/api/sentiment/predict"
bwc_explain_link = "https://test.xaidemo.de/api/sentiment/explain"
gc_predict_link = "https://xaidemo.de/api/sentiment/predict"
gc_explain_link = "https://xaidemo.de/api/sentiment/explain"

test_messages = ["Top Lage, ausgezeichnetes Frühstücksbuffet, super Wellnessbereich, super freundliches Personal",
                "Das Hotel ist wirklich sehr schön. Die Speisen im Restaurant und zum Frühstück hervorragend. Das Personal ist schlecht organisiert.",
                "Keine Sonnenschirme am Außenpool. Extrem lange Wartezeiten beim Essen, auch beim Frühstück. Mangelhaft abgestimmte Arbeitsprozesse im Service.",
                "Manche Tage verlangen nach Soulfood und genau das war es - super lecker, top Qualität und toll angerichtet. Bei dem Wetter finde ich eine Stunde Wartezeit auch ok. Preis-Leisung passt.",
                "Pizza war echt labberig und nicht mehr ganz warm. Der Lieferant kam nicht pünktlich. Das Tiramisu ist auch eher mäßig.",
                "Outstanding food, nicely packaged, but additional sauces and cutlery was missing.",
                "Leider war die Pizza viel zu lange im Ofen gewesen, daher sehr trocken und teilweise verkokelte Zwiebeln. Mir wurde noch nie so offensichtlich Essensabfall als Salat verkauft."]

#---------------------------------------------------------------------------------------
# RUN TEST
#print("RUNNING TESTS WITH ", str(nof_requests), "REQUESTS PER REVIEW")

print("RUNNING TESTS WITH "+ str(nof_requests)+ " REQUESTS PER REVIEW")
print("------------------------------------------------------------")
for review in test_messages:
    evaluate(review, nof_requests, True)
    evaluate(review, nof_requests, False)