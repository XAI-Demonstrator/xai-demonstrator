import requests
import numpy as np
import re
import string
import os
from tabulate import tabulate

#---------------------------------------------------------------------------------------
# TEST ROUTINE

def evaluate(review: str, nof_requests: int, path: str, bw_cloud: bool):
    split_review = re.findall(r"[\w']+|" + f"[{string.punctuation}]", review)
    # initialize prediction occurence counter
    prediction_occ = np.zeros(5)
    prediction_times = []
    # create dict for predict request
    predict_json = {"text": review}

    # initialize explanation score lists (one list for every word/symbol)
    explanation_scores = [[] for _ in range(len(split_review))]
    explanation_times = []

    for _ in range(nof_requests):
        # request prediction scores
        if bw_cloud:
            prediction_request = requests.post(bwc_predict_link, json=predict_json)
            # choose arg max as prediction
            prediction = np.argmax(prediction_request.json()['prediction'])
            prediction_times.append(prediction_request.elapsed.total_seconds())

            # create dict for explain request
            explain_json = {"text": review, "target": str(np.argmax(prediction)),
                            "explainer": "integrated_gradients"}
            # request explanation scores
            explanation_request = requests.post(bwc_explain_link, json=explain_json)
            # save duration of explain request
        else:
            prediction_request = requests.post(gc_predict_link, json=predict_json)
            # choose arg max as prediction
            print(prediction_request.json())
            prediction = np.argmax(prediction_request.json()['prediction'])
            prediction_times.append(prediction_request.elapsed.total_seconds())

            # create dict for explain request
            explain_json = {"text": review, "target": str(np.argmax(prediction)),
                            "explainer": "integrated_gradients"}
            # request explanation scores
            explanation_request = requests.post(gc_explain_link, json=explain_json)
        explanation_times.append(explanation_request.elapsed.total_seconds())

    # print results
    with open(path, 'a', encoding='utf-8') as file:
        if bw_cloud:
            file.write("evaluation of review: ")
            file.write(review)
            file.write("\n")
            file.write("prediction time (BW Cloud) - mean: "+ str(np.mean(prediction_times))+
                       ", std: "+ str(np.std(prediction_times))+ "\n")
            file.write("explanation time (BW Cloud) - mean: "+ str(np.mean(explanation_times))+
                       ", std: "+ str(np.std(explanation_times))+ "\n")
        else:
            file.write("prediction time (Google Cloud) - mean: " + str(np.mean(prediction_times)) + ", std: " + str(
                np.std(prediction_times)) + "\n")
            file.write("explanation time (Google Cloud) - mean: " + str(np.mean(explanation_times)) + ", std: " + str(
                np.std(explanation_times)) + "\n")
            file.write("------------------------------------------------------------\n")
    #print("prediction time - mean: ", np.mean(prediction_times),
    #      ", std: ", np.std(prediction_times), "\n")
    #print("explanation time - mean: ", np.mean(explanation_times),
    #      ", std: ", np.std(explanation_times), "\n")
    #print("------------------------------------------------------------", "\n")

#---------------------------------------------------------------------------------------
# SET GLOBAL VARIABLES

MAIN_DIR = os.path.dirname(os.path.realpath(__file__))
nof_requests = 2

predict_link = "https://test.xaidemo.de/api/sentiment/predict"
explain_link = "https://test.xaidemo.de/api/sentiment/explain"
bwc_predict_link = "https://test.xaidemo.de/api/sentiment/predict"
bwc_explain_link = "https://test.xaidemo.de/api/sentiment/explain"
gc_predict_link = "https://xaidemo.de/api/sentiment/predict"
gc_explain_link = "https://xaidemo.de/api/sentiment/explain"
path = os.path.join(MAIN_DIR, 'runtime.txt')

test_messages = ["Top Lage, ausgezeichnetes Frühstücksbuffet, super Wellnessbereich, super freundliches Personal",
                "Das Hotel ist wirklich sehr schön. Die Speisen im Restaurant und zum Frühstück hervorragend. Das Personal ist schlecht organisiert."]#,
                #"Keine Sonnenschirme am Außenpool. Extrem lange Wartezeiten beim Essen, auch beim Frühstück. Mangelhaft abgestimmte Arbeitsprozesse im Service.",
                #"Manche Tage verlangen nach Soulfood und genau das war es - super lecker, top Qualität und toll angerichtet. Bei dem Wetter finde ich eine Stunde Wartezeit auch ok. Preis-Leisung passt.",
                #"Pizza war echt labberig und nicht mehr ganz warm. Der Lieferant kam nicht pünktlich. Das Tiramisu ist auch eher mäßig.",
                #"Outstanding food, nicely packaged, but additional sauces and cutlery was missing.",
                #"Leider war die Pizza viel zu lange im Ofen gewesen, daher sehr trocken und teilweise verkokelte Zwiebeln. Mir wurde noch nie so offensichtlich Essensabfall als Salat verkauft."]

#---------------------------------------------------------------------------------------
# RUN TEST
#print("RUNNING TESTS WITH ", str(nof_requests), "REQUESTS PER REVIEW")
try:
    os.remove(path)
except OSError:
    pass
with open(path, 'a', encoding='utf-8') as file:
    file.write("RUNNING TESTS WITH "+ str(nof_requests)+ "REQUESTS PER REVIEW\n")
    file.write("------------------------------------------------------------\n")
for review in test_messages:
    evaluate(review, nof_requests, path, True)
    evaluate(review, nof_requests, path, False)