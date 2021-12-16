# Client-side experiment tracking

Record data during experiments.

## Example

Use `tracking.set_up()` to instrument an XAI Demonstrator service:

    from fastapi import FastAPI
    from xaidemo import tracing, tracking

    # Experiment tracking builds on OpenTelemetry,
    # so don't forget to set up tracing
    tracing.set_up()  

    app = FastAPI()
    tracking.instrument(app)

    @app.post("/predict")
    def predict(text: str):
        tracking.record_data("input", {"text": text, "length": len(text)})

        ...

    tracing.instrument(app)

Note that `EXPERIMENT=1` needs to be set at start time,
otherwise no data will be recorded.

## See also

For the full documentation of the experiment tracking capabilities,
see [experiment-tracker](../../../../experiment-tracker).
