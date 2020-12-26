import numpy as np
import requests

number_of_requests = 10

root_times, predict_times, explain_times = [], [], []

test_str = "This is a test!"
test_dict = {"text": test_str}

for _ in range(number_of_requests):
    # time response of start page
    root_times.append(requests.get("http://test.xaidemo.de/").elapsed.total_seconds())
    # time response of predict request
    predict_times.append(requests.post('http://test.xaidemo.de/predict', json=test_dict).elapsed.total_seconds())
    # time response of explain request
    explain_times.append(requests.post('http://test.xaidemo.de/explain', json=test_dict).elapsed.total_seconds())

print(number_of_requests, "start page responses timed; mean:", np.mean(root_times), "variance:", np.var(root_times))
print("")
print(number_of_requests, "predict responses timed; mean:", np.mean(predict_times), "variance:", np.var(predict_times))
print("")
print(number_of_requests, "explain responses timed; mean:", np.mean(explain_times), "variance", np.var(explain_times))
