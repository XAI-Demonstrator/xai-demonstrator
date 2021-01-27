from functools import wraps
from typing import Any, Callable, Dict, Union

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter import jaeger
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pydantic import BaseSettings


print(__file__, type(__file__))

trace.set_tracer_provider(TracerProvider())


class TracingSettings(BaseSettings):
    environment: str = "local"
    # OpenTelemetry exporter configuration
    agent_host_name: str = "localhost"
    agent_port: int = 6831


tracing_settings = TracingSettings()


def set_up(service_name: str):
    if tracing_settings.environment == "test":
        from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

        jaeger_exporter = jaeger.JaegerSpanExporter(
            service_name=service_name,
            agent_host_name=tracing_settings.agent_host_name,
            agent_port=tracing_settings.agent_port,
        )

        trace.get_tracer_provider().add_span_processor(
            BatchExportSpanProcessor(jaeger_exporter)
        )
    elif tracing_settings.environment == "debug":
        from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor, ConsoleSpanExporter

        trace.get_tracer_provider().add_span_processor(
            SimpleExportSpanProcessor(ConsoleSpanExporter())
        )


def instrument_app(app: FastAPI):
    """Has to be called after all routes have been added (?)"""
    FastAPIInstrumentor.instrument_app(app)


def traced(func: Union[Callable, None] = None,
           label: Union[None, str] = None,
           attributes: Union[Dict[str, Any], None] = None):
    """Decorator for functions.


    """
    attributes = attributes or {}

    def decorator_function(func_: Callable):
        _label = label or func_.__name__

        @wraps(func_)
        def with_tracer(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span(_label) as span:
                for attribute, value in attributes.items():
                    span.set_attribute(attribute, value)
                return func_(*args, **kwargs)

        return with_tracer

    return decorator_function(func) if callable(func) else decorator_function
