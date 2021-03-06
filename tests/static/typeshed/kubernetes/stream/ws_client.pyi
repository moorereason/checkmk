# Stubs for kubernetes.stream.ws_client (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from collections import namedtuple
from typing import Any, Optional

STDIN_CHANNEL: int
STDOUT_CHANNEL: int
STDERR_CHANNEL: int
ERROR_CHANNEL: int
RESIZE_CHANNEL: int

class WSClient:
    sock: Any = ...
    def __init__(self, configuration: Any, url: Any, headers: Any) -> None: ...
    def peek_channel(self, channel: Any, timeout: int = ...): ...
    def read_channel(self, channel: Any, timeout: int = ...): ...
    def readline_channel(self, channel: Any, timeout: Optional[Any] = ...): ...
    def write_channel(self, channel: Any, data: Any) -> None: ...
    def peek_stdout(self, timeout: int = ...): ...
    def read_stdout(self, timeout: Optional[Any] = ...): ...
    def readline_stdout(self, timeout: Optional[Any] = ...): ...
    def peek_stderr(self, timeout: int = ...): ...
    def read_stderr(self, timeout: Optional[Any] = ...): ...
    def readline_stderr(self, timeout: Optional[Any] = ...): ...
    def read_all(self): ...
    def is_open(self): ...
    def write_stdin(self, data: Any) -> None: ...
    def update(self, timeout: int = ...): ...
    def run_forever(self, timeout: Optional[Any] = ...) -> None: ...
    def close(self, **kwargs: Any) -> None: ...

WSResponse = namedtuple('WSResponse', ['data'])

def get_websocket_url(url: Any): ...
def websocket_call(configuration: Any, *args: Any, **kwargs: Any): ...
