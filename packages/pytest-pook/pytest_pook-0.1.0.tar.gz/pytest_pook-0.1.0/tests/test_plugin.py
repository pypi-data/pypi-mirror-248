import pytest


def test_mark_disallows_pending_mocks_default(pytester: pytest.Pytester):
    pytester.makepyfile(
        """
        import pook
        import pytest


        @pytest.mark.pook
        def test_default_behaviour():
            pook.get("https://example.com")


        @pytest.mark.pook(allow_pending_mocks=False)
        def test_explicitly_disallow():
            pook.get("https://example.com")
    """
    )

    result = pytester.runpytest()
    result.assert_outcomes(passed=2, errors=2)


def test_mark_allows_pending_mocks(pytester: pytest.Pytester):
    pytester.makepyfile(
        """
        import pook
        import pytest


        @pytest.mark.pook(allow_pending_mocks=True)
        def test_allowed():
            pook.get("https://example.com")
    """
    )

    result = pytester.runpytest()
    result.assert_outcomes(passed=1)


def test_mark_starts_active_pook(pytester: pytest.Pytester):
    pytester.makepyfile(
        """
        import pook
        import pytest
        from http.client import HTTPConnection


        @pytest.mark.pook(allow_unused=True)
        def test_pook_enabled():
            assert pook.isactive()

            pook.get("http://example.com").reply(200).body("Hello from pook")
            http = HTTPConnection("example.com:80")
            http.request("GET", "/")
            res = http.getresponse()
            assert res.read() == "Hello from pook"
    """
    )

    result = pytester.runpytest()
    result.assert_outcomes(passed=1)


def test_pook_not_active(pytester: pytest.Pytester):
    pytester.makepyfile(
        """
        import pook
        import pytest
        from http.client import HTTPConnection


        def test_pook_not_enabled():
            assert not pook.isactive()


        @pytest.mark.pook(start_active=False)
        def test_pook_not_started():
            assert not pook.isactive()

            pook.activate()

            pook.get("http://example.com").reply(200).body("Hello from pook")
            http = HTTPConnection("example.com:80")
            http.request("GET", "/")
            res = http.getresponse()
            assert res.read() == "Hello from pook"
    """
    )

    result = pytester.runpytest()
    result.assert_outcomes(failed=1, passed=1)


def test_must_be_used(pytester: pytest.Pytester):
    pytester.makepyfile(
        """
        import pook
        import pytest


        @pytest.mark.pook
        def test_unused():
            assert True != False
    """
    )

    result = pytester.runpytest()
    result.assert_outcomes(errors=1, passed=1)


def test_isolation(pytester: pytest.Pytester):
    pytester.makepyfile(
        """
        import pook
        import pytest


        @pytest.mark.pook
        def test_unused():
            # This test intentionally fails both in the assertion
            # in the test itself and it fails the configuration and
            # usage checks enforced by the plugin
            assert True == False
    """
    )

    result = pytester.runpytest()
    result.assert_outcomes(errors=1, failed=1)

    pytester.makepyfile(
        """
        import pook
        import pytest
        from http.client import HTTPConnection


        @pytest.mark.pook
        def test_perfect():
            # This test should work perfectly, even though the previous one failed
            # and raised an exception in the fixture cleanup
            pook.get("http://example.com").reply(200).body("Hello from pook")
            http = HTTPConnection("example.com:80")
            http.request("GET", "/")
            res = http.getresponse()
            assert res.read() == "Hello from pook"
    """
    )

    result = pytester.runpytest()
    result.assert_outcomes(passed=1)
