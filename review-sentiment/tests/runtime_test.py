import numpy as np
import requests


def measure(review_text: str,
            backend_url: str,
            endpoint: str,
            num_of_requests: int):
    request_durations = []
    payload = {"text": review_text}

    for _ in range(num_of_requests):
        request = requests.post(backend_url + endpoint, json=payload)

        request_durations.append(request.elapsed.total_seconds())

    return request_durations


def evaluate(review_text: str,
             backend_url: str,
             num_of_requests: int = 10):
    for endpoint in ["/predict", "/explain"]:
        durations = measure(review_text, backend_url, endpoint, num_of_requests)

        print(endpoint)
        print(f"- first request:", durations[0])
        print(f"- remaining:", np.mean(durations[1:]), "+/-", np.std(durations[1:]))


NUM_OF_REQUESTS = 20

TEST_DEPLOYMENT = "https://test.xaidemo.de/api/sentiment"
PROD_DEPLOYMENT = "https://xaidemo.de/api/sentiment"

test_reviews = ["Top Lage, ausgezeichnetes Frühstücksbuffet, super Wellnessbereich, super freundliches Personal",
                "Das Hotel ist wirklich sehr schön. Die Speisen im Restaurant und zum Frühstück hervorragend. Das Personal ist schlecht organisiert.",
                "Keine Sonnenschirme am Außenpool. Extrem lange Wartezeiten beim Essen, auch beim Frühstück. Mangelhaft abgestimmte Arbeitsprozesse im Service.",
                "Manche Tage verlangen nach Soulfood und genau das war es - super lecker, top Qualität und toll angerichtet. Bei dem Wetter finde ich eine Stunde Wartezeit auch ok. Preis-Leisung passt.",
                "Pizza war echt labberig und nicht mehr ganz warm. Der Lieferant kam nicht pünktlich. Das Tiramisu ist auch eher mäßig.",
                "Outstanding food, nicely packaged, but additional sauces and cutlery was missing.",
                "Leider war die Pizza viel zu lange im Ofen gewesen, daher sehr trocken und teilweise verkokelte Zwiebeln. Mir wurde noch nie so offensichtlich Essensabfall als Salat verkauft."]

if __name__ == "__main__":
    print("RUNNING TESTS WITH " + str(NUM_OF_REQUESTS) + " REQUESTS PER REVIEW")
    print("------------------------------------------------------------")
    print("BW Cloud")
    for review in test_reviews:
        evaluate(review, TEST_DEPLOYMENT, NUM_OF_REQUESTS)

    print("GCP")
    for review in test_reviews:
        evaluate(review, PROD_DEPLOYMENT, NUM_OF_REQUESTS)
