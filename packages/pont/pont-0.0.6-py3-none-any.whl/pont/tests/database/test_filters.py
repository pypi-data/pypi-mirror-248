import pytest

from pont.database import QueryError
from pont.database.filters import EqualFilter, RegexFilter
from pont.flow import Flow


@pytest.fixture
def flow_http():
    flow = Flow("http")
    flow.port = 80
    return flow


@pytest.fixture
def flow_redis():
    flow = Flow("redis")
    flow.port = 6379
    return flow


def test_repr_equal_filter():
    assert EqualFilter("protocol", "http", False).__repr__() == "protocol=http"
    assert EqualFilter("protocol", "http", True).__repr__() == "!protocol=http"


def test_equal_filter_match_string(flow_http, flow_redis):
    filter = EqualFilter("protocol", "http", False)

    assert filter.match(flow_http)
    assert not filter.match(flow_redis)


def test_equal_filter_negate(flow_http, flow_redis):
    filter = EqualFilter("protocol", "http", True)

    assert not filter.match(flow_http)
    assert filter.match(flow_redis)


def test_equal_filter_match_int(flow_http, flow_redis):
    filter = EqualFilter("port", "80", False)

    assert filter.match(flow_http)
    assert not filter.match(flow_redis)


def test_equal_filter_match_int_with_invalid_integer_value(flow_http):
    with pytest.raises(QueryError):
        filter = EqualFilter("port", "invalid", False)
        filter.match(flow_http)


def test_equal_filter_match_int_with_invalid_field_name(flow_http):
    with pytest.raises(QueryError):
        filter = EqualFilter("invalid", "http", False)
        filter.match(flow_http)


def test_regex_filter(flow_http, flow_redis):
    assert RegexFilter("protocol", "^http", False).match(flow_http)
    assert RegexFilter("protocol", "ttp", False).match(flow_http)
    assert not RegexFilter("protocol", "^http", False).match(flow_redis)
    with pytest.raises(QueryError):
        assert RegexFilter("protocol", "[", False).match(flow_http)
    assert RegexFilter("port", "80", False).match(flow_http)
    assert RegexFilter("port", "0", False).match(flow_http)
    assert not RegexFilter("port", "0", False).match(flow_redis)
