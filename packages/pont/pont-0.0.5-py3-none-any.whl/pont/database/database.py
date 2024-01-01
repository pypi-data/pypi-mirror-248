"""
This is the database module, it's a simple in memory database
with basic query capabilities
"""

from typing import Iterator, List, Optional

from pont.flow import Flow

from .query import query_parser


class Flows:
    def __init__(self) -> None:
        self._flows: List[Flow] = []

    def add(self, flow: Flow):
        self._flows.append(flow)

    def clear(self):
        self._flows = []

    def find(
        self,
        query: Optional[str] = None,
        sort: Optional[str] = None,
        limit: Optional[int] = None,
        reverse: bool = False,
    ) -> list[Flow]:
        """
        Find flows matching the filter

        Args:
            query: A query string to search the flows (optional)
            sort: A field to sort the flows (optional)
            limit: A limit of flows to return (optional)
            reverse: Reverse the order of the flows (optional)
        Returns:
            A list of flows
        """
        if len(self._flows) == 0:
            return []
        if sort == "start_time":
            sort = None  # It's already sorted by start_time
        if query is None or len(query) == 0:
            return self.__sorted_flows(
                self._flows, sort=sort, limit=limit, reverse=reverse
            )

        # If we have a limit and we don't need to sort, we can return the
        # reversed list directly.
        if limit is not None and reverse and sort is None:
            return self.__filter_flows(reversed(self._flows), query, limit)
        else:
            filtered_flows = self.__filter_flows(self._flows, query, limit)
            return self.__sorted_flows(
                filtered_flows, sort=sort, limit=limit, reverse=reverse
            )

    def __filter_flows(
        self, flows: list[Flow] | Iterator[Flow], query: str, limit: int | None
    ) -> list[Flow]:
        filters = query_parser(query)
        filtered_flows = []
        for flow in flows:
            match = True
            for filter in filters:
                if not filter.match(flow):
                    match = False
                    break
            if match:
                filtered_flows.append(flow)
                if limit is not None and len(filtered_flows) >= limit:
                    break
        return filtered_flows

    def __sorted_flows(
        self,
        flows: list[Flow],
        sort: Optional[str],
        limit: Optional[int],
        reverse: bool,
    ) -> list[Flow]:
        if sort is not None:
            flows = sorted(flows, key=lambda flow: getattr(flow, sort), reverse=reverse)
        elif reverse and limit is None:
            flows = list(reversed(flows))
        elif reverse and limit is not None:
            # We need to reverse the list and then take the first N elements
            # we avoid to build a new list with all elements to save memory
            out = []
            for flow in reversed(flows):
                out.append(flow)
                if len(out) >= limit:
                    break
            return out
        if limit is None:
            return flows
        else:
            return flows[:limit]

    def get(self, id: str) -> Flow:
        """
        Get a flow by its id

        Raise KeyError if not found
        """
        for flow in self._flows:
            if flow.id == id:
                return flow
        raise KeyError(f"Flow {id} not found")


class Database:
    def __init__(self) -> None:
        self._flows = Flows()

    def flows(self) -> Flows:
        return self._flows
