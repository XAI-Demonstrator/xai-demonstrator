"""OpenTelemetry tracing utilities"""
from functools import wraps
from typing import Any, Callable, Dict, Union

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter import jaeger
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from pydantic import BaseSettings

from . import __version__

__all__ = ["set_up", "instrument_app", "add_span_attributes", "traced"]

trace.set_tracer_provider(TracerProvider())


class TracingSettings(BaseSettings):
    TRACING_EXPORTER: str = "default"
    # OpenTelemetry Jaeger exporter configuration
    JAEGER_AGENT_HOST_NAME: str = "localhost"
    JAEGER_AGENT_PORT: int = 6831


tracing_settings = TracingSettings()


def set_up(service_name: str):
    """Instantiate and configure the span exporter.

    The exporter is select and configured through environment variables.

    Parameters
    ----------
    service_name : str
        The name under which the data is exported.
    """
    if tracing_settings.TRACING_EXPORTER.lower() == "jaeger":
        from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

        jaeger_exporter = jaeger.JaegerSpanExporter(
            service_name=service_name,
            agent_host_name=tracing_settings.JAEGER_AGENT_HOST_NAME,
            agent_port=tracing_settings.JAEGER_AGENT_PORT,
        )

        trace.get_tracer_provider().add_span_processor(
            BatchExportSpanProcessor(jaeger_exporter)
        )
    elif tracing_settings.TRACING_EXPORTER.lower() == "console":
        from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor, ConsoleSpanExporter

        trace.get_tracer_provider().add_span_processor(
            SimpleExportSpanProcessor(ConsoleSpanExporter())
        )
    elif tracing_settings.TRACING_EXPORTER == "gcp":
        from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
        from opentelemetry.tools.cloud_trace_propagator import CloudTraceFormatPropagator
        from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
        from opentelemetry.propagators import set_global_textmap

        cloud_trace_exporter = CloudTraceSpanExporter()
        trace.get_tracer_provider().add_span_processor(
            BatchExportSpanProcessor(cloud_trace_exporter)
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
            tracer = trace.get_tracer(instrumenting_module_name=__name__,
                                      instrumenting_library_version=__version__)
            with tracer.start_as_current_span(_label) as span:
                add_span_attributes(attributes, span)
                return func_(*args, **kwargs)

        return with_tracer

    return decorator_function(func) if callable(func) else decorator_function
