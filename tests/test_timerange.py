import datetime
import unittest

from datagrepper.util import assemble_timerange


utc = datetime.timezone.utc


class TestTimerange(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime.fromtimestamp(1325376000, tz=utc)
        patcher = unittest.mock.patch("datagrepper.util.datetime")
        self.addCleanup(patcher.stop)
        mock_dt = patcher.start()
        # https://docs.python.org/3/library/unittest.mock-examples.html#mock-patching-methods
        mock_dt.utcnow.return_value = self.now
        mock_dt.fromtimestamp.side_effect = (
            lambda *args, **kw: datetime.datetime.fromtimestamp(*args, **kw)
        )

    def test_none_none_none(self):
        start, end, delta = assemble_timerange(None, None, None)
        assert start is None
        assert end is None
        assert delta is None

    def test_delta_none_none(self):
        start, end, delta = assemble_timerange(None, None, 5)
        assert 1325375995.0 == start
        assert 1325376000.0 == end
        assert 5 == delta

    def test_none_start_none(self):
        start = self.now - datetime.timedelta(seconds=700)
        start = start.timestamp()
        start, end, delta = assemble_timerange(start, None, None)
        assert 1325375300.0 == start
        assert 1325376000.0 == end
        assert 700 == delta

    def test_delta_start_none(self):
        start = self.now - datetime.timedelta(seconds=600)
        start = start.timestamp()
        start, end, delta = assemble_timerange(start, None, 5)
        assert 1325375400.0 == start
        assert 1325375405.0 == end
        assert 5 == delta

    def test_none_none_end(self):
        end = self.now - datetime.timedelta(seconds=600)
        end = end.timestamp()
        start, end, delta = assemble_timerange(None, end, None)
        assert 1325374800.0 == start
        assert 1325375400.0 == end
        assert 600 == delta

    def test_delta_none_end(self):
        end = self.now - datetime.timedelta(seconds=600)
        end = end.timestamp()
        start, end, delta = assemble_timerange(None, end, 5)
        assert 1325375395.0 == start
        assert 1325375400.0 == end
        assert 5 == delta

    def test_none_start_end(self):
        end = self.now - datetime.timedelta(seconds=600)
        end = end.timestamp()
        start = self.now - datetime.timedelta(seconds=800)
        start = start.timestamp()
        start, end, delta = assemble_timerange(start, end, None)
        assert 1325375200.0 == start
        assert 1325375400.0 == end
        assert 200 == delta

    def test_delta_start_end(self):
        end = self.now - datetime.timedelta(seconds=600)
        end = end.timestamp()
        start = self.now - datetime.timedelta(seconds=800)
        start = start.timestamp()
        start, end, delta = assemble_timerange(start, end, 5)
        assert 1325375200.0 == start
        assert 1325375400.0 == end
        assert 200 == delta
