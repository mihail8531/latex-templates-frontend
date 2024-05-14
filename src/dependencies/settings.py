from functools import cache
from typing import Callable, TypeVar, cast
from fastapi import Depends
from pydantic_settings import BaseSettings
from dependencies.state import state
from settings import BackendSettings, Settings


def get_settings(settings: Settings = Depends(state("settings"))) -> Settings:
    return settings


_T = TypeVar("_T", bound=BaseSettings)


@cache
def settings_t(settings_type: type[_T]) -> Callable[[Settings], _T]:
    def get_settings_dep(settings: Settings = Depends(get_settings)) -> _T:
        assert issubclass(Settings, settings_type)
        return cast(_T, settings)

    return get_settings_dep
