"""Example module docstring."""
from typing import Union


def squared(number: Union[int, float]) -> Union[int, float]:
    """Example function docstring."""
    if isinstance(number, float):
        return number**2.0
    if isinstance(number, int):
        return int(number**2)
    raise ValueError(
        f"invalid argument '{number}'. Argument must be a an integer or float number."
    )
