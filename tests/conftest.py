from unittest.mock import patch

import pytest

from src.core.config import settings


@pytest.fixture
def mock_settings():
    with patch.object(
        settings,
        'database_uri',
        'postgresql://user:password@localhost:5432/test_db',
    ):
        yield settings


def test_some_function(mock_settings):
    assert (
        mock_settings.database_uri
        == 'postgresql://user:password@localhost:5432/test_db'
    )


def test_another_function(mock_settings):
    assert (
        mock_settings.database_uri
        == 'postgresql://user:password@localhost:5432/test_db'
    )
