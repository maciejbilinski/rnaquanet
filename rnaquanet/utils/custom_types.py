# Custom types
from typing import Union, Literal
from os import PathLike

# File path type
PathType = Union[str, PathLike]

# NaN behavior type
# - 'col' - remove columns with NaN values
# - 'row' - remove rows with NaN values
# - float - replace NaN with value
# - '' - do nothing
NanBehaviorType = Union[Literal['col', 'row', ''], float]
