# `pytest-pook`

A pytest plugin for [`pook`](https://github.com/h2non/pook).

## Installation

```
pip install pytest-pook
```

Pytest automatically finds and configures the plugin.

## Usage

### `@pytest.mark.pook`

Tests that rely on pook can be marked with `@pytest.mark.pook`. The mark wraps the test in `pook.use()` in a way compatible with pytest, that does not interfere with other marks. It also asserts that any declared pook mocks were actually matched. This prevents the easy mistake of declareing a mock intenteded to be matched, but that never matches. Normally this requires manually asserting `pook.isdone()` at the end of a test, but this is too easy to forget and is tedious anyhow.

Within the body of the test, use the global pook import to interact with pook for things like creating new mocks.

Use the mark's default behaviour as follows:

```py
import pytest
import requests
import pook


@pytest.mark.pook
def test_network_call():
    pook.get("https://example.com").reply(200).body("Hello from pook")

    res = requests.get("https://example.com")

    assert res.text == "Hello from pook"
```

#### Delay pook activation

If your test requires real network calls to happen before pook is enabled, pass `start_active=False` to the mark to delay pook activation until `pook.on` is called:

```py
import pytest
import requests
import pook


@pytest.mark.pook(start_active=False)
def test_network_call():
    fixture = requests.get("localhost:8080/my-fixture").json()

    (pook.post("https://example.com")
        .json(fixture)
        .reply(200)
        .body("Hello from pook"))

    pook.on()
    res = requests.get("https://example.com", data=fixture)

    assert res.text == "Hello from pook"
```

With this approach, you still get the benefits of automatic cleanup and checks, but can still make outbound network calls before pook starts capturing them later in your test.

#### Dangling or unused pending mocks

By default the plugin raises an exception if it detects if pending mocks exist after the test is finished. This helps catch the easy-to-miss edge case where a pook was intended to match a request but didn't match any. This is commonly caused either by the tested code not using a compatible HTTP library or by misconfigured mocks.

To disable this check, pass `allow_pending_mocks=True` to the mark. In this case, it is recommended to manually confirm the mocks are in the expected state at the end of the test.
