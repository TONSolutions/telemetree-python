import pytest
from unittest.mock import patch
from src.telemetree.event_builder import EventBuilder
from src.telemetree.config import Config
from src.telemetree.telegram_schemas import Update
import src.test.fixtures as fixtures


@pytest.fixture
def mock_config():
    with patch("src.telemetree.config.requests.get") as mocked_get:
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.json.return_value = {
            "auto_capture_telegram": True,
            "public_key": "sample_key",
            "host": "test_host",
            "auto_capture_telegram_events": [
                "message",
                "inline_query",
                "chosen_inline_result",
            ],
            "auto_capture_commands": ["/start", "/stop"],
            "auto_capture_messages": ["Test message"],
            "app_name": "Test app",
        }
        config_instance = Config(api_key="dummy_api_key", project_id="dummy_project_id")
        return config_instance


@pytest.fixture
def mock_config_no_auto_capture_telegram():
    with patch("src.telemetree.config.requests.get") as mocked_get:
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.json.return_value = {
            "auto_capture_telegram": False,
            "public_key": "sample_key",
            "host": "test_host",
            "auto_capture_telegram_events": [],
            "auto_capture_commands": ["/start", "/stop"],
            "auto_capture_messages": ["Test message"],
            "app_name": "Test app",
        }
        config_instance = Config(api_key="dummy_api_key", project_id="dummy_project_id")
        return config_instance


@pytest.fixture
def event_builder(mock_config):
    return EventBuilder(settings=mock_config)


@pytest.fixture
def event_builder_no_capture(mock_config_no_auto_capture_telegram):
    return EventBuilder(settings=mock_config_no_auto_capture_telegram)


def test_parse_valid_message_update(event_builder):
    result = event_builder.parse_telegram_update(
        fixtures.message_update_telegram_tracked
    )
    assert isinstance(result, Update)


def test_parse_invalid_message_update(event_builder):
    result = event_builder.parse_telegram_update(
        fixtures.message_update_telegram_not_tracked
    )
    assert result is None


def test_parse_valid_edited_message_update(event_builder):
    result = event_builder.parse_telegram_update(fixtures.edited_message_update_tracked)
    assert isinstance(result, Update)


def test_parse_invalid_edited_message_update(event_builder):
    result = event_builder.parse_telegram_update(
        fixtures.edited_message_update_not_tracked
    )
    assert result is None


def test_parse_valid_inline_query_update(event_builder):
    result = event_builder.parse_telegram_update(fixtures.inline_query_update_telegram)
    assert isinstance(result, Update)


def test_parse_valid_chosen_inline_result_update(event_builder):
    result = event_builder.parse_telegram_update(
        fixtures.chosen_inline_result_update_telegram
    )
    assert isinstance(result, Update)


def test_parse_valid_message_update_no_auto_capture(event_builder_no_capture):
    result = event_builder_no_capture.parse_telegram_update(
        fixtures.message_update_telegram_tracked
    )
    assert result is None


def test_parse_valid_edited_message_update_no_auto_capture(event_builder_no_capture):
    result = event_builder_no_capture.parse_telegram_update(
        fixtures.edited_message_update_tracked
    )
    assert result is None


def test_parse_valid_inline_query_update_no_auto_capture(event_builder_no_capture):
    result = event_builder_no_capture.parse_telegram_update(
        fixtures.inline_query_update_telegram
    )
    assert result is None


def test_parse_valid_chosen_inline_result_update_no_auto_capture(
    event_builder_no_capture,
):
    result = event_builder_no_capture.parse_telegram_update(
        fixtures.chosen_inline_result_update_telegram
    )
    assert result is None
