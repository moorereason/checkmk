# Stubs for kubernetes.client.models.v1_node_selector (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class V1NodeSelector:
    swagger_types: Any = ...
    attribute_map: Any = ...
    discriminator: Any = ...
    node_selector_terms: Any = ...
    def __init__(self, node_selector_terms: Optional[Any] = ...) -> None: ...
    @property
    def node_selector_terms(self): ...
    @node_selector_terms.setter
    def node_selector_terms(self, node_selector_terms: Any) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other: Any): ...
    def __ne__(self, other: Any): ...
