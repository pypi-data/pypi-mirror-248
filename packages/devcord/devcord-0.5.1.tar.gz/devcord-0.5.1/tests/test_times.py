from datetime import datetime, timedelta

import pytest

import devcord
from devcord import ConvertTimeError


def test_convert_time():
    dt = devcord.set_utc(datetime.utcnow())

    assert isinstance(devcord.convert_dt(dt), str)
    assert isinstance(devcord.convert_dt(timedelta(seconds=5)), str)
    assert isinstance(devcord.convert_time(5), str)


def test_dc_timestamp():
    result = devcord.dc_timestamp(0)
    assert result.startswith("<t:") and result.endswith(":R>")


def test_convert_so_seconds():
    assert devcord.convert_to_seconds("1m 9s") == 69
    assert devcord.convert_to_seconds("1.5m") == 90
    assert devcord.convert_to_seconds("1,5 min") == 90
    assert devcord.convert_to_seconds("1h 5m 10s") == 3910

    # tests with no units
    assert devcord.convert_to_seconds("1 2m 3") == 120
    assert devcord.convert_to_seconds("2") == 120
    assert devcord.convert_to_seconds("2", default_unit="s", error=True) == 2
    assert devcord.convert_to_seconds("2", default_unit=None) == 0

    with pytest.raises(ConvertTimeError):
        devcord.convert_to_seconds("1 2 3", default_unit=None, error=True)

    # tests with invalid units
    assert devcord.convert_to_seconds("") == 0
    assert devcord.convert_to_seconds("z") == 0

    with pytest.raises(ConvertTimeError):
        assert devcord.convert_to_seconds("", error=True)

    with pytest.raises(ConvertTimeError):
        assert devcord.convert_to_seconds("z", error=True)
