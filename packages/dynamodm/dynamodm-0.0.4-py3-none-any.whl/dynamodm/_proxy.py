from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar, cast

from typing_extensions import ClassVar, override

T = TypeVar("T")


class LazyProxy(Generic[T], ABC):
    """Implements data methods to pretend that an instance is another instance.

    This includes forwarding attribute access and othe methods.
    """

    should_cache: ClassVar[bool] = False

    def __init__(self) -> None:
        self.__proxied: T | None = None

    # Note: we have to special case proxies that themselves return proxies
    # to support using a proxy as a catch-all for any random access, e.g. ⁠ proxy.foo.bar.baz ⁠

    def _getattr_(self, attr: str) -> object:
        proxied = self._get_proxied_()
        if isinstance(proxied, LazyProxy):
            return proxied  # pyright: ignore
        return getattr(proxied, attr)

    @override
    def __repr__(self) -> str:
        proxied = self._get_proxied_()
        if isinstance(proxied, LazyProxy):
            return proxied.__class__.__name__
        return repr(self._get_proxied_())

    @override
    def __str__(self) -> str:
        proxied = self._get_proxied_()
        if isinstance(proxied, LazyProxy):
            return proxied.__class__.__name__
        return str(proxied)

    @override
    def __dir__(self) -> Iterable[str]:
        proxied = self._get_proxied_()
        if isinstance(proxied, LazyProxy):
            return []
        return proxied.__dir__()

    @property  # type: ignore
    @override
    def __class__(self) -> type:  # type: ignore
        proxied = self._get_proxied_()
        if issubclass(type(proxied), LazyProxy):
            return type(proxied)
        return proxied.__class__

    def _get_proxied_(self) -> T:
        if not self.should_cache:
            return self.__load__()

        proxied = self.__proxied
        if proxied is not None:
            return proxied

        self._proxied = proxied = self.__load__()
        return proxied

    def _set_proxied_(self, value: T) -> None:
        self.__proxied = value

    def _as_proxied_(self) -> T:
        """Helper method that returns the current proxy, typed as the loaded object"""
        return cast(T, self)

    @abstractmethod
    def __load__(self) -> T:
        ...
