import datetime
import uuid
from dataclasses import dataclass, field, fields
from typing import Any


@dataclass
class Flow:
    """
    Store a request / response
    """

    protocol: str
    """The protocol (http, redis...)"""
    id: str = field(
        default_factory=lambda: uuid.uuid4().hex, metadata={"visible": False}
    )
    """The id of the flow in the internal database"""
    host: str = field(default="", metadata={"visible": True})
    """The host of the request"""
    port: int = field(default=0, metadata={"visible": True})
    """The port of the request"""
    method: str = field(default="", metadata={"visible": True})
    """The request method for example GET/POST for HTTP, SELECT/INSERT for SQL..."""
    status: str = field(default="", metadata={"visible": True})
    """Response status. For HTTP will the HTTP response code"""
    path: str = field(default="", metadata={"visible": True})
    """Path of the request"""
    query: str = field(default="", metadata={"visible": True})
    """Query of the request"""
    response_mime_type: str = field(
        default="application/octet-stream", metadata={"visible": True}
    )
    """Mime Type of the reply"""
    start_time: datetime.datetime = field(
        default_factory=datetime.datetime.now, metadata={"visible": False}
    )
    request_headers: dict[str, str] = field(
        default_factory=dict, metadata={"visible": False}
    )
    """Headers of the request"""
    request_body: bytes = field(default=b"", metadata={"visible": False})
    """Body of the request"""
    response_headers: dict[str, str] = field(
        default_factory=dict, metadata={"visible": False}
    )
    """Headers of the response"""
    response_body: bytes = field(default=b"", metadata={"visible": False})
    """Body of the response"""

    updated_at: datetime.datetime = field(
        default_factory=datetime.datetime.now, metadata={"visible": False}
    )
    """When the flow was updated"""

    @classmethod
    def field_names(cls):
        """
        Return the list of field names
        """
        return [field.name for field in fields(cls)]

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__("updated_at", datetime.datetime.now())
        super().__setattr__(name, value)
