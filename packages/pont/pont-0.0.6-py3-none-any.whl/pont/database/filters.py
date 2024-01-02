import re

from pont.flow import Flow

from .query_error import QueryError


class Filter:
    """
    A filter is a apply to a database set of results to filter the results
    """

    # Must be defined in child classes
    OPERATOR = None

    field: str
    """The field to compare"""
    value: str
    """The value to compare to"""
    negate: bool
    """Inverse the filter result"""

    def __init__(self, field: str, value: str, negate: bool) -> None:
        self.field = field
        self.value = value
        self.negate = negate

    def match(self, flow: Flow) -> bool:
        """
        Check if a flow match the filter

        Args:
            flow: The flow to check

        Returns:
            True if the flow match the filter
        """
        if self.negate:
            return not self.test(flow)
        return self.test(flow)

    def test(self, flow: Flow) -> bool:
        raise NotImplementedError

    def _get_flow_value(self, flow: Flow) -> object:
        if not hasattr(flow, self.field):
            raise QueryError(f"Invalid query unknown field {self.field}.")
        return getattr(flow, self.field)

    def __repr__(self) -> str:
        if self.negate:
            return f"!{self.field}{self.OPERATOR}{self.value}"
        else:
            return f"{self.field}{self.OPERATOR}{self.value}"

    def __eq__(self, __value: object) -> bool:
        return self.__repr__() == __value


class EqualFilter(Filter):
    """
    A filter to check if a field is equal to a value
    """

    OPERATOR = "="

    def test(self, flow: Flow) -> bool:
        value = self._get_flow_value(flow)
        if isinstance(value, int):
            try:
                return int(self.value) == value
            except ValueError:
                raise QueryError(
                    f"Invalid query at {self.field}={self.value}, "
                    f"field {self.field} is an integer but '{self.value}' is not."
                )
        return self.value == value


class RegexFilter(Filter):
    """
    A filter to check if a field match a regex
    """

    OPERATOR = "~"

    def test(self, flow: Flow) -> bool:
        value = self._get_flow_value(flow)
        try:
            return re.search(self.value, str(value)) is not None
        except re.error as e:
            raise QueryError(
                f"Invalid query at {self.field}~{self.value}, "
                f"field {self.field} is a string but '{self.value}' is not a valid regex. "
                f"{e.msg}"
            )
