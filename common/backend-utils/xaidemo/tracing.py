"""OpenTelemetry tracing utilities for the XAI Demonstrator."""
from functools import wraps
from typing import Any, Callable, Dict, Union

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from pydantic_settings import BaseSettings

from . import __version__

__all__ = ["set_up", "instrument_app", "add_span_attributes", "traced"]


class TracingSettings(BaseSettings):
    TRACING_EXPORTER: str = "default"
    SERVICE_NAME: str = "unknown-xaidemo-service"
    # OpenTelemetry Jaeger exporter configuration
    JAEGER_AGENT_HOST_NAME: str = "localhost"
    JAEGER_AGENT_PORT: int = 6831


tracing_settings = TracingSettings()

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: tracing_settings.SERVICE_NAME})
    )
)


def set_up():
    """Instantiate the span exporter.

    The exporter is selected and configured through environment variables.
    """
    if tracing_settings.TRACING_EXPORTER.lower() == "jaeger":
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.exporter.jaeger.thrift import JaegerExporter

        jaeger_exporter = JaegerExporter(
            agent_host_name=tracing_settings.JAEGER_AGENT_HOST_NAME,
            agent_port=tracing_settings.JAEGER_AGENT_PORT,
        )

        trace.get_tracer_provider().add_span_processor(
            BatchSpanProcessor(jaeger_exporter)
        )
    elif tracing_settings.TRACING_EXPORTER.lower() == "console":
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

        trace.get_tracer_provider().add_span_processor(
            SimpleSpanProcessor(ConsoleSpanExporter())
        )
    elif tracing_settings.TRACING_EXPORTER == "gcp":
        from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
        from opentelemetry.propagators.cloud_trace_propagator import CloudTraceFormatPropagator
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.propagate import set_global_textmap

        cloud_trace_exporter = CloudTraceSpanExporter()
        trace.get_tracer_provider().add_span_processor(
            BatchSpanProcessor(cloud_trace_exporter)
        )

        set_global_textmap(CloudTraceFormatPropagator())


def instrument_app(app: FastAPI):
    """Add OpenTelemetry middleware to a FastAPI app.

    Following available documentation and examples,
    this should be called after all routes have been added.
    """
    FastAPIInstrumentor.instrument_app(app)


def add_span_attributes(attributes: Dict[str, Any],
                        span: Union[trace.Span, None] = None):
    """Add attributes to a span.

    Parameters
    ----------
    attributes : dict
        Arbitrary number of span attributes.
    span : opentelemetry.trace.Span

    """
    span = span or trace.get_current_span()
    for attribute, value in attributes.items():
        span.set_attribute(attribute, value)


def get_tracer():
    return trace.get_tracer(instrumenting_module_name=__name__,
                            instrumenting_library_version=__version__)


def traced(func: Union[Callable, None] = None,
           label: Union[None, str] = None,
           attributes: Union[Dict[str, Any], None] = None) -> Callable:
    """Decorator that adds a span around a function.

    Parameters
    ----------
    func : Callable
        The function to be decorated
    label : str, optional
        A custom label. If not specified, the function's `__name__` will be used.
    attributes : dict, optional
        Arbitrary number of span attributes.

    Examples
    --------

    To simply trace a single function:

        @traced
        def my_function():
            ...

    This results in a span with name `my_function`.

    To add custom labels and span attributes, use the keyword arguments:

        @traced(label="custom_span_label", attributes={"num_of_samples": 12})
        def my_function():
            ...

    This results in a span with name `custom_span_label` with attribute `num_of_samples` set to 12.
    """
    attributes = attributes or {}

    def decorator_function(func_: Callable) -> Callable:
        _label = label or func_.__name__

        @wraps(func_)
        def with_tracer(*args, **kwargs):
            tracer = get_tracer()
            with tracer.start_as_current_span(_label) as span:
                add_span_attributes(attributes, span)
                return func_(*args, **kwargs)

        return with_tracer

    return decorator_function(func) if callable(func) else decorator_function
