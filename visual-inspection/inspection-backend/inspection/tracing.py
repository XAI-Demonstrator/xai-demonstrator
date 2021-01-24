from typing import Union, Callable
from opentelemetry import trace
from functools import wraps
from opentelemetry.exporter import jaeger

from .config import Settings


def set_up_tracing(settings: Settings):
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


def traced(func: Callable, label: Union[None, str] = None):
    label = label or func.__name__

    @wraps(func)
    def with_tracer(*args, **kwargs):
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span(label):
            return func(*args, **kwargs)

    return with_tracer
