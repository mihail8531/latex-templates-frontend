from functools import cache
from typing import Any, Callable
from fastapi import Depends, Request
from fastapi.datastructures import State


def get_state(request: Request) -> State:
    return request.app.state


@cache
def state(attr: str) -> Callable[[State], Any]:
    def get_attribute(state: State = Depends(get_state)) -> Any:
        return state.__getattr__(attr)

    return get_attribute
