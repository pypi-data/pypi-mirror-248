import pytest

import pook


def pytest_configure(config: pytest.Config):
    config.addinivalue_line(
        "markers",
        "pook(allow_pending_mocks, start_active): wrap the test in a pook context manager",
    )


@pytest.fixture(autouse=True)
def _pook_marker(request: pytest.FixtureRequest):
    marker = request.node.get_closest_marker("pook")

    if marker is None:
        # Test isn't marked, ignore it
        yield
        return

    allow_pending_mocks = marker.kwargs.get("allow_pending_mocks", False)
    start_active = marker.kwargs.get("start_active", True)
    with pook.use() as engine:
        if not start_active:
            engine.disable()

        yield

        assert engine.mocks != [], (
            "No mocks registered to engine after test. Tests should not be marked for pook "
            "if they do not use pook."
        )

        if not allow_pending_mocks:
            assert engine.isdone(), (
                "Unused mocks present after test. "
                "If this is intentional, pass `allow_pending_mocks=True` to "
                "`@pytest.mark.pook`.\n"
                "Pending mocks:\n"
                f"{engine.pending_mocks()}"
            )

    assert not engine.isactive()
