from functools import wraps
from typing import Any, Callable, Dict, Union

from opentelemetry import trace
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
    elif settings.environment == "debug":
        from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor, ConsoleSpanExporter

        trace.get_tracer_provider().add_span_processor(
            SimpleExportSpanProcessor(ConsoleSpanExporter())
        )


def traced(func: Union[Callable, None] = None,
           label: Union[None, str] = None,
           attributes: Union[Dict[str, Any], None] = None):
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
