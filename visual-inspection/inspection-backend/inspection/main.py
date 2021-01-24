import base64
import io

from fastapi import FastAPI, File, UploadFile
from opentelemetry import trace
from opentelemetry.exporter import jaeger
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider

from .config import settings
from .explainer.explain import explain
from .model.predict import Prediction, predict
from .routers import frontend

trace.set_tracer_provider(TracerProvider())

if settings.environment == "test":
    from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

    jaeger_exporter = jaeger.JaegerSpanExporter(
        service_name=settings.service_name,
        agent_host_name=settings.agent_host_name,
        agent_port=settings.agent_port,
    )

    trace.get_tracer_provider().add_span_processor(
        BatchExportSpanProcessor(jaeger_exporter)
    )
else:
    from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor, ConsoleSpanExporter

    trace.get_tracer_provider().add_span_processor(
        SimpleExportSpanProcessor(ConsoleSpanExporter())
    )


app = FastAPI()
app.include_router(frontend.router)


@app.post("/predict")
def predict_weather(file: UploadFile = File(...)) -> Prediction:
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("classify-image"):
        return predict(file.file)


# TODO: Define explanation request input and response content
@app.post("/explain")
def get_explanation(file: UploadFile = File(...)):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("explain-classification"):
        exp_image = explain(file.file)

    with tracer.start_as_current_span("prepare-explanation-response"):
        buffered = io.BytesIO()
        exp_image.save(buffered, format="png")
        encoded_image_string = base64.b64encode(buffered.getvalue())

    return {"image": bytes("data:image/png;base64,", encoding='utf-8') + encoded_image_string}


FastAPIInstrumentor.instrument_app(app)
