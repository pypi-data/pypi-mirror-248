"""
This provide a query interface to the database.
"""

import enum
from typing import Callable, List

from .filters import EqualFilter, Filter, RegexFilter
from .query_error import QueryError

OPERATORS = {
    "=": EqualFilter,
    "~": RegexFilter,
}


class CompleteType(enum.Enum):
    """
    The type of completion
    """

    FIELD = 0
    VALUE = 1


class ParseState(enum.Enum):
    """
    The state of the parser
    """

    FIELD = 0
    OPERATOR = 1
    VALUE = 2
    VALUE_QUOTED = 3
    VALUE_FIRST_CHAR = 4


def query_parser(query: str) -> list[Filter]:
    """
    Parse a query string and return a list of filters

    Args:
        query: The query string

    Returns:
        A list of filters
    """
    state, filters = __query_tokenizer(query)
    if state == ParseState.VALUE_QUOTED:
        last_filter = filters[-1]
        raise QueryError(
            f"Invalid query unterminated quoted value at {last_filter.field}"
        )

    return filters


def query_complete(
    query: str, fields: List[str], value_completion: Callable
) -> tuple[CompleteType, List[str]]:
    """
    After tokenizing the query, return a list of possible completion

    Args:
        query: The query string
        fields: A list of possible fields
        value_completion: A lambda to complete the value
    """

    state, filters = __query_tokenizer(query)

    if len(filters) == 0:
        return (CompleteType.FIELD, fields)
    if state == ParseState.FIELD:
        text = filters[-1].field
        return (
            CompleteType.FIELD,
            list(filter(lambda field: field.startswith(text), fields)),
        )
    elif state == ParseState.VALUE or state == ParseState.VALUE_FIRST_CHAR:
        return (
            CompleteType.VALUE,
            value_completion(filters[-1].field, filters[-1].value),
        )
    elif state == ParseState.VALUE_QUOTED:
        # If the value is quoted, we add a quote to the completion
        return (
            CompleteType.VALUE,
            [
                completion + '"'
                for completion in value_completion(filters[-1].field, filters[-1].value)
            ],
        )
    else:
        return (CompleteType.FIELD, [])


def __query_tokenizer(query: str) -> tuple[ParseState, List[Filter]]:
    """
    Tokenize a query string and return a list of filters

    Args:
        query: The query string
    Returns:
        A tuple with the last state of the parser and a list of filters
    """

    filters = []
    state = ParseState.FIELD
    query = query.strip()
    if query == "":
        return state, filters

    operator = None
    field = ""
    value = ""
    negate = False
    escaped = False
    for c in query:
        if state == ParseState.FIELD:
            if c == " " and field == "":
                continue
            elif c == " ":
                raise QueryError(
                    f"Invalid query at {field} missing operator. Allowed operators: {', '.join(OPERATORS.keys())}"
                )
            elif c == "!":
                negate = True
            elif c in OPERATORS.keys():
                operator = c
                value = ""
                state = ParseState.VALUE_FIRST_CHAR
            else:
                field += c
            if field == "AND":  # The AND operator is optional
                field = ""
                state = ParseState.FIELD
        elif state == ParseState.VALUE_FIRST_CHAR:
            if c == '"':
                state = ParseState.VALUE_QUOTED
            elif c == " ":
                raise QueryError(f"Invalid query at {field}{operator} missing value")
            else:
                value += c
                state = ParseState.VALUE
        elif state == ParseState.VALUE:
            if c == " " and operator:
                state = ParseState.FIELD
                filters.append(OPERATORS[operator](field, value, negate))
                field = ""
                negate = False
                operator = None
            else:
                value += c
        elif state == ParseState.VALUE_QUOTED:
            if escaped:
                escaped = False
                value += c
            elif c == "\\":
                escaped = True
            elif c == '"' and operator:
                state = ParseState.FIELD
                filters.append(OPERATORS[operator](field, value, negate))
                field = ""
                negate = False
                operator = None
            else:
                value += c

    if operator:
        filters.append(OPERATORS[operator](field, value, negate))
    elif len(field) > 0:
        # If the query is incomplete, we assume the user want to filter on the field
        # this is useful for the auto-completion
        filters.append(EqualFilter(field, "", False))
    return state, filters
