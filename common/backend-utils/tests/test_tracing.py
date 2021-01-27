from xaidemo import tracing


class FakeProvider:

    def __init__(self):
        self.processors = []

    def add_span_processor(self, processor):
        self.processors.append(processor)


def test_test_environment_tracing_setup(mocker):
    provider = FakeProvider()
    spy = mocker.spy(provider, 'add_span_processor')

    def get_tracer_provider():
        return provider

    mocker.patch.object(tracing.trace, 'get_tracer_provider', get_tracer_provider)

    settings = tracing.TracingSettings()
    settings.environment = "test"
    mocker.patch.object(tracing, 'tracing_settings', settings)

    tracing.set_up("test-service")

    spy.assert_called_once()
    assert len(provider.processors) == 1


def test_debug_environment_tracing_setup(mocker):
    provider = FakeProvider()
    spy = mocker.spy(provider, 'add_span_processor')

    def get_tracer_provider():
        return provider

    mocker.patch.object(tracing.trace, 'get_tracer_provider', get_tracer_provider)

    settings = tracing.TracingSettings()
    settings.environment = "debug"
    mocker.patch.object(tracing, 'tracing_settings', settings)

    tracing.set_up("test-service")

    spy.assert_called_once()
    assert len(provider.processors) == 1


def test_local_environment_tracing_setup(mocker):
    provider = FakeProvider()
    spy = mocker.spy(provider, 'add_span_processor')

    def get_tracer_provider():
        return provider

    mocker.patch.object(tracing.trace, 'get_tracer_provider', get_tracer_provider)

    settings = tracing.TracingSettings()
    settings.environment = "local"
    mocker.patch.object(tracing, 'tracing_settings', settings)

    tracing.set_up("test-service")

    spy.assert_not_called()
    assert len(provider.processors) == 0

