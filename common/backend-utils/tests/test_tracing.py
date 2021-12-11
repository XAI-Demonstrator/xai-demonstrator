from fastapi import FastAPI
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware

from xaidemo import tracing


class FakeProvider:

    def __init__(self):
        self.processors = []

    def add_span_processor(self, processor):
        self.processors.append(processor)


def test_jaeger_exporter_tracing_setup(mocker):
    provider = FakeProvider()
    spy = mocker.spy(provider, 'add_span_processor')

    def get_tracer_provider():
        return provider

    mocker.patch.object(tracing.trace, 'get_tracer_provider', get_tracer_provider)

    settings = tracing.TracingSettings()
    settings.TRACING_EXPORTER = "jaeger"
    mocker.patch.object(tracing, 'tracing_settings', settings)

    tracing.set_up()

    spy.assert_called_once()
    assert len(provider.processors) == 1


def test_console_exporter_tracing_setup(mocker):
    provider = FakeProvider()
    spy = mocker.spy(provider, 'add_span_processor')

    def get_tracer_provider():
        return provider

    mocker.patch.object(tracing.trace, 'get_tracer_provider', get_tracer_provider)

    settings = tracing.TracingSettings()
    settings.TRACING_EXPORTER = "console"
    mocker.patch.object(tracing, 'tracing_settings', settings)

    tracing.set_up()

    spy.assert_called_once()
    assert len(provider.processors) == 1


def test_gcp_exporter_tracing_setup(mocker):
    auth_mock = mocker.patch("google.auth.default")
    auth_mock.return_value = ("password12345", None)

    provider = FakeProvider()
    spy = mocker.spy(provider, 'add_span_processor')

    def get_tracer_provider():
        return provider

    mocker.patch.object(tracing.trace, 'get_tracer_provider', get_tracer_provider)

    settings = tracing.TracingSettings()
    settings.TRACING_EXPORTER = "gcp"
    mocker.patch.object(tracing, 'tracing_settings', settings)

    tracing.set_up()

    spy.assert_called_once()
    assert len(provider.processors) == 1


def test_default_exporter_tracing_setup(mocker):
    provider = FakeProvider()
    spy = mocker.spy(provider, 'add_span_processor')

    def get_tracer_provider():
        return provider

    mocker.patch.object(tracing.trace, 'get_tracer_provider', get_tracer_provider)

    settings = tracing.TracingSettings()
    settings.TRACING_EXPORTER = "default"
    mocker.patch.object(tracing, 'tracing_settings', settings)

    tracing.set_up()

    spy.assert_not_called()
    assert len(provider.processors) == 0


def test_that_app_is_instrumented():
    app = FastAPI()
    assert len(app.user_middleware) == 0

    tracing.instrument_app(app)

    assert len(app.user_middleware) == 1
    assert app.user_middleware[0].cls is OpenTelemetryMiddleware


def test_that_traced_without_parameters_adds_span():
    @tracing.traced
    def my_function():
        return tracing.trace.get_current_span()

    assert my_function().name == "my_function"


def test_that_traced_with_custom_label_adds_span():
    @tracing.traced(label="custom_span_label")
    def my_function():
        return tracing.trace.get_current_span()

    assert my_function().name == "custom_span_label"


def test_that_traced_with_attributes_adds_span():
    @tracing.traced(attributes={"first": 1, "second": "two"})
    def my_function():
        return tracing.trace.get_current_span()

    span = my_function()
    assert span.name == "my_function"
    assert "first" in span.attributes
    assert "second" in span.attributes
    assert span.attributes["first"] == 1
    assert span.attributes["second"] == "two"


def test_that_traced_with_label_and_attributes_adds_span():
    @tracing.traced(label="my_custom_label",
                    attributes={"first": 1, "second": "two"})
    def my_function():
        return tracing.trace.get_current_span()

    span = my_function()
    assert span.name == "my_custom_label"
    assert "first" in span.attributes
    assert "second" in span.attributes
    assert span.attributes["first"] == 1
    assert span.attributes["second"] == "two"
