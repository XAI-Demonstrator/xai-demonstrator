import pytest
from xaidemo.tracking.record import TaskMemory, PartialRecordRequest, SourceInformation
from xaidemo.tracking.record import send_record, logger, settings
from yarl import URL

partial_record_request = PartialRecordRequest(id="abc123",
                                              source=SourceInformation(),
                                              label="sending",
                                              part={"payload": {"key": "value"}})


def test_that_task_memory_stores_data():
    TaskMemory.add_task("dummy1", partial_record_request)

    assert len(TaskMemory.memory["dummy1"]) == 1
    assert TaskMemory.memory["dummy1"][0] == partial_record_request

    del TaskMemory.memory["dummy1"]


def test_that_task_memory_is_erased():
    TaskMemory.add_task("dummy2", partial_record_request)

    list_of_tasks = TaskMemory.get_tasks_and_erase_memory("dummy2")

    assert list_of_tasks[0] == partial_record_request
    assert not TaskMemory.memory["dummy2"]


def test_that_same_key_cannot_be_set_twice():
    TaskMemory.add_task("my_key", partial_record_request)

    with pytest.raises(ValueError):
        TaskMemory.add_task("my_key", partial_record_request)


@pytest.mark.asyncio
async def test_that_data_is_sent(aiomock, mocker):
    mocker.patch.object(settings, "experiment", new=True)
    mocker.patch.object(settings, "collector_url", new="http://collector")
    aiomock.post(settings.collector_url + "/record", status=200)

    await send_record(partial_record_request)

    call = aiomock.requests.get(("POST", URL(settings.collector_url + "/record")))[0]
    assert call.kwargs["json"]["id"] == "abc123"
    assert call.kwargs["json"]["part"] == {"payload": {"key": "value"}}


@pytest.mark.asyncio
async def test_that_collector_issues_are_handled_gracefully(aiomock, mocker):
    mocker.patch.object(settings, "experiment", new=True)
    mocker.patch.object(settings, "collector_url", new="http://collector")
    aiomock.post(settings.collector_url + "/record", status=409)
    logger_mock = mocker.patch.object(logger, "error")

    await send_record(partial_record_request)

    assert logger_mock.call_count == 1


@pytest.mark.asyncio
async def test_that_unavailable_collector_is_handled_gracefully(aiomock, mocker):
    mocker.patch.object(settings, "experiment", new=True)
    mocker.patch.object(settings, "collector_url", new="http://collector")
    aiomock.post(settings.collector_url + "/record", timeout=True)
    logger_mock = mocker.patch.object(logger, "error")

    await send_record(partial_record_request)

    assert logger_mock.call_count == 1
