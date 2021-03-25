import requests
import numpy as np
import re
import string
from tabulate import tabulate

#---------------------------------------------------------------------------------------
# TEST ROUTINE

def evaluate(review: str, nof_requests: int):
    print("------------------------------------------------------------")
    print("evaluation of review: ")
    print(review)
    print("")
    # split review in words and symbols (like the explainer does)
    split_review = re.findall(r"[\w']+|" + f"[{string.punctuation}]", review)

    # initialize prediction occurence counter
    prediction_occ = np.zeros(5)
    prediction_times = []
    # create dict for predict request
    predict_json={"text": review}
   
    # initialize explanation score lists (one list for every word/symbol)
    explanation_scores = [[] for _ in range(len(split_review))]
    explanation_times = []

    for _ in range(nof_requests):
        # request prediction scores
        prediction_request = requests.post(predict_link, json=predict_json) 
        # choose arg max as prediction
        prediction = np.argmax(prediction_request.json()['prediction'])
        # count up occurences of observed prediction
        prediction_occ[prediction] += 1
        # save duration of predict request
        prediction_times.append(prediction_request.elapsed.total_seconds())
        
        # create dict for explain request
        explain_json = {"text":review, "target":str(np.argmax(prediction)),
                        "explainer":"integrated_gradients"} 
        # request explanation scores
        explanation_request=requests.post(explain_link, json=explain_json)
        # choose explanation from response json
        explanation=explanation_request.json()["explanation"]
        # save explanation scores for every word and symbol in review
        for index in range(len(split_review)):
            explanation_scores[index].append(explanation[index][1])
        # save duration of explain request
        explanation_times.append(explanation_request.elapsed.total_seconds())
        
    # print results 
    print("prediction time - mean: ", np.mean(prediction_times), 
          ", std: ", np.std(prediction_times),"\n")
    prediction_data = [[(index+1)*"*", 
                        prediction_occ[index]] for index in range(5)]
    
    print(tabulate(prediction_data, headers=["rating", "occurences"]), "\n")
      
    print("explanation time - mean: ", np.mean(explanation_times), 
          ", std: ", np.std(explanation_times),"\n")
   
    explanation_data = [[word, 
                     np.mean(explanation_scores[index]),
                     np.std(explanation_scores[index])] for index, word in enumerate(split_review)]
    print(tabulate(explanation_data, headers=["word", "mean", "std"]))
    print("------------------------------------------------------------","\n")
  
#---------------------------------------------------------------------------------------
# SET GLOBAL VARIABLES

nof_requests = 2

predict_link = "https://test.xaidemo.de/api/sentiment/predict"
explain_link = "https://test.xaidemo.de/api/sentiment/explain"

test_messages = ["Top Lage, ausgezeichnetes Frühstücksbuffet, super Wellnessbereich, super freundliches Personal",
                "Das Hotel ist wirklich sehr schön. Die Speisen im Restaurant und zum Frühstück hervorragend. Das Personal ist schlecht organisiert.",
                "Keine Sonnenschirme am Außenpool. Extrem lange Wartezeiten beim Essen, auch beim Frühstück. Mangelhaft abgestimmte Arbeitsprozesse im Service.",
                "Manche Tage verlangen nach Soulfood und genau das war es - super lecker, top Qualität und toll angerichtet. Bei dem Wetter finde ich eine Stunde Wartezeit auch ok. Preis-Leisung passt.",
                "Pizza war echt labberig und nicht mehr ganz warm. Der Lieferant kam nicht pünktlich. Das Tiramisu ist auch eher mäßig.",
                "Outstanding food, nicely packaged, but additional sauces and cutlery was missing.",
                "Leider war die Pizza viel zu lange im Ofen gewesen, daher sehr trocken und teilweise verkokelte Zwiebeln. Mir wurde noch nie so offensichtlich Essensabfall als Salat verkauft."]

#---------------------------------------------------------------------------------------
# RUN TEST

print("RUNNING TESTS WITH ", str(nof_requests), "REQUESTS PER REVIEW")
for review in test_messages:
    evaluate(review, nof_requests)
