import pytest

from pont.database.filters import EqualFilter, RegexFilter
from pont.database.query import CompleteType, query_complete, query_parser
from pont.database.query_error import QueryError


def test_query_parser_empty():
    query = ""
    filters = query_parser(query)
    assert filters == []


def test_query_parser_equal_filter():
    query = "field1=value1"
    filters = query_parser(query)
    expected_filters = [EqualFilter("field1", "value1", False)]
    assert filters == expected_filters


def test_query_parser_equal_filter_quoted():
    query = 'field1="value1 with spaces"'
    filters = query_parser(query)
    expected_filters = [EqualFilter("field1", "value1 with spaces", False)]
    assert filters == expected_filters


def test_query_parser_equal_filter_quoted_and_escaped():
    query = 'field1="value1 \\"with\\" spaces and \\\\"'
    filters = query_parser(query)
    expected_filters = [EqualFilter("field1", 'value1 "with" spaces and \\', False)]
    assert filters == expected_filters


def test_query_parser_regex_filter():
    query = "field1~value1"
    filters = query_parser(query)
    expected_filters = [RegexFilter("field1", "value1", False)]
    assert filters == expected_filters


def test_query_parser_multiple_filters_with_and():
    query = "field1=value1 AND field2=value2"
    filters = query_parser(query)
    expected_filters = [
        EqualFilter("field1", "value1", False),
        EqualFilter("field2", "value2", False),
    ]
    assert filters == expected_filters


def test_query_parser_multiple_filters_with_and_negate():
    query = "field1=value1 AND field2!=value2 AND field3=value3"
    filters = query_parser(query)
    expected_filters = [
        EqualFilter("field1", "value1", False),
        EqualFilter("field2", "value2", True),
        EqualFilter("field3", "value3", False),
    ]
    assert filters == expected_filters


def test_query_parser_multiple_filters_with_optional_and():
    query = "field1=value1 AND field2=value2"
    filters = query_parser(query)
    expected_filters = [
        EqualFilter("field1", "value1", False),
        EqualFilter("field2", "value2", False),
    ]
    assert filters == expected_filters


def test_raise_error():
    with pytest.raises(QueryError):
        query_parser("field1 field2")

    with pytest.raises(QueryError):
        query_parser("field1= field2")

    with pytest.raises(QueryError):
        query_parser('field1=" field2')


def value_completion(field, value):
    """
    Dummy function to test the auto-completion of a value
    """

    if field == "host":
        hosts = ["example.com", "example.org", "domain.com"]
        return list(filter(lambda x: x.startswith(value), hosts))
    elif field == "method":
        return ["GET", "POST"]


def test_query_complete():
    fields = ["host", "method", "path", "status", "size", "port", "protocol"]

    assert query_complete("", fields, value_completion) == (CompleteType.FIELD, fields)
    assert query_complete("ho", fields, value_completion) == (
        CompleteType.FIELD,
        ["host"],
    )
    assert query_complete("p", fields, value_completion) == (
        CompleteType.FIELD,
        ["path", "port", "protocol"],
    )
    assert query_complete("host=example AND s", fields, value_completion) == (
        CompleteType.FIELD,
        [
            "status",
            "size",
        ],
    )
    assert query_complete("host=ex", fields, value_completion) == (
        CompleteType.VALUE,
        [
            "example.com",
            "example.org",
        ],
    )
    assert query_complete("host=", fields, value_completion) == (
        CompleteType.VALUE,
        [
            "example.com",
            "example.org",
            "domain.com",
        ],
    )
    assert query_complete('host="ex', fields, value_completion) == (
        CompleteType.VALUE,
        [
            'example.com"',
            'example.org"',
        ],
    )
