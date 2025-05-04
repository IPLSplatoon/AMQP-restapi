"""
RPC Response Model
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import TypeVar, Generic, Union, Optional, Dict, Any

T = TypeVar("T", bound=Union[BaseModel, object])


class RPCResponse(BaseModel, Generic[T]):
    """
    RPC Response Model
    """

    data: Optional[T] = Field(None, description="Response Data")
    # RabbitMQ message properties
    headers: Dict[str, Any] = Field(default_factory=list, description="Response Headers")

    content_type: Optional[str]
    content_encoding: Optional[str]
    msg_type: Optional[str]
    expiration: Optional[str]
    timestamp: Optional[datetime]

    @property
    def response_headers(self) -> Dict[str, str]:
        headers = {}
        for str_value in ["content_type", "content_encoding", "msg_type", "expiration"]:
            attribute = getattr(self, str_value)
            if attribute:
                headers[f"X-{str_value.replace('_', '-')}"] = attribute
        if self.timestamp:
            headers["x-timestamp"] = self.timestamp.isoformat()
        for key, value in self.headers.items():
            try:
                headers[f"X-{key.replace(' ', '-')}"] = str(value)
            except Exception:
                pass
        return headers
