from datetime import datetime

from krxfetch._chrome import _release_schedule
from krxfetch._chrome import _major_version
from krxfetch._chrome import _unified_platform
from krxfetch._chrome import user_agent


def test__release_schedule():
    schedule = _release_schedule()
    version = schedule[0][1]

    for item in schedule:
        assert item[1] == version
        version -= 1

    for item in schedule:
        dt = datetime.strptime(item[0], '%b %d, %Y')
        assert type(dt) is datetime


def test__major_version():
    # assert _major_version() == 120

    dt1 = datetime.fromisoformat('2023-05-30 23:59:59.283')
    assert _major_version(dt1) == 113

    dt2 = datetime.fromisoformat('2023-05-31 00:00:00.000')
    assert _major_version(dt2) == 114

    dt3 = datetime.fromisoformat('2023-07-18 23:59:59.283')
    assert _major_version(dt3) == 114

    dt4 = datetime.fromisoformat('2023-07-19 00:00:00.000')
    assert _major_version(dt4) == 115

    dt5 = datetime.fromisoformat('2025-01-29 23:59:59.283')
    assert _major_version(dt5) == 133

    dt6 = datetime.fromisoformat('2023-01-11 00:00:00.000')
    assert _major_version(dt6) == 109

    dt7 = datetime.fromisoformat('2023-01-10 23:59:59.283')
    assert _major_version(dt7) == 108

    dt8 = datetime.fromisoformat('2000-01-01 00:00:00.000')
    assert _major_version(dt8) == 108

    dt9 = datetime.fromisoformat('2030-12-31 23:59:59.283')
    assert _major_version(dt9) == 133


def test__unified_platform():
    macos_platform = 'Macintosh; Intel Mac OS X 10_15_7'

    assert _unified_platform() == macos_platform


def test_user_agent():
    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
            'Chrome/{}.0.0.0 Safari/537.36'

    result = user_agent(major_ver=1)
    assert result == agent.format(1)

    result = user_agent(major_ver=120)
    assert result == agent.format(120)

    result = user_agent()
    assert result == agent.format(_major_version())


def test_maintenance():
    """If this test fails, update _release_schedule() function."""

    schedule = _release_schedule()
    latest_version = schedule[0][1]

    assert _major_version() != latest_version
