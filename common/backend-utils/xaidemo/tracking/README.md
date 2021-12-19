# Client-side experiment tracking

Record data during experiments.

## Example

Use `tracking.set_up()` to instrument an XAI Demonstrator service:

```python
from fastapi import FastAPI
from xaidemo import tracing, tracking

# Experiment tracking builds on OpenTelemetry,
# so don't forget to set up tracing
tracing.set_up()  

app = FastAPI()
tracking.instrument(app)

@app.post("/predict")
def predict(text: str):
    tracking.record_data(key="input", value={"text": text, "length": len(text)})

    ...

tracing.instrument(app)
```
You will find this data within the record under `data[key]` along with some metadata.

Note that `EXPERIMENT=1` needs to be set at start time, otherwise no data will be recorded.


Note that each `key` can only used once within a record and the key `"tracked"` is 
already used for the [`experiment-proxy`](../../../../experiment-tracker/experiment-proxy/README.md) data.
In other words: Make sure to use a different `key` for each call to `record_data` you make within
your use case and that a single external request to your use case does not execute the
same `record_data` call more than once.



## See also

For the full documentation of the experiment tracking capabilities,
see [here](../../../../experiment-tracker/README.md).
