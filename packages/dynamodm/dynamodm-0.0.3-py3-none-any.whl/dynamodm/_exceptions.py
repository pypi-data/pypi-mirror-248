"""
Exceptions Handling
"""
from __future__ import annotations

from functools import singledispatch

from pydantic import Field  # pylint: disable=no-name-in-module
from pydantic import BaseModel, ValidationError  # pylint: disable=no-name-in-module
from typing_extensions import Generic, Type, TypeVar

E = TypeVar("E", bound=Exception, contravariant=True)

EXCEPTIONS: dict[str, int] = {
    "ConnectError": 503,
    "ConnectTimeout": 408,
    "DecodingError": 422,
    "HTTPError": 500,
    "LocalProtocolError": 500,
    "NetworkError": 503,
    "PoolTimeout": 503,
    "ProtocolError": 500,
    "ProxyError": 502,
    "ReadTimeout": 408,
    "RemoteProtocolError": 502,
    "StreamError": 500,
    "TimeoutException": 408,
    "TooManyRedirects": 310,
    "TransportError": 503,
    "UnsupportedProtocol": 505,
    "WriteTimeout": 408,
    "TimeoutError": 408,
    "ConnectionError": 503,
    "ConnectionRefusedError": 503,
    "ConnectionResetError": 503,
    "asyncio.TimeoutError": 408,
    "UnicodeDecodeError": 400,
    "UnicodeEncodeError": 400,
    "UnicodeError": 400,
    "TypeError": 400,
    "ValueError": 400,
    "ZeroDivisionError": 500,
    "IndexError": 400,
    "AttributeError": 500,
    "ImportError": 500,
    "ModuleNotFoundError": 500,
    "NotImplementedError": 501,
    "RecursionError": 500,
    "OverflowError": 500,
    "KeyError": 404,
    "Exception": 500,
}


class HTTPException(BaseModel, Generic[E]):
    """ "
    Exception wrapper for network related errors

    Attributes:
                                    - status: HTTP status code
                                    - message: HTTP status message
    """

    status: int = Field(default=500, description="HTTP status code")
    message: str = Field(
        default="Internal Server Error", description="HTTP status message"
    )

    @classmethod
    def from_exception(cls, exc: E) -> HTTPException[E]:
        """
        Build a HttpException from an exception

        Arguments:
                                        - exc: Exception to be handled

        Returns:
                                        - HttpException
        """
        return handle_exception(exc)


@singledispatch
def handle_exception(exc: Type[E]) -> HTTPException[E]:
    """
    Handle exceptions and return a HttpException

    Arguments:
                                    - exc: Exception to be handled

    Returns:
                                    - HttpException
    """
    raise NotImplementedError()


@handle_exception.register(ValidationError)
def _(exc: ValidationError) -> HTTPException[ValidationError]:
    return HTTPException(status=400, message=exc.json())


@handle_exception.register(Exception)
def _(exc: Exception) -> HTTPException[Exception]:
    if exc.__class__.__name__ in EXCEPTIONS:
        return HTTPException(
            status=EXCEPTIONS[exc.__class__.__name__], message=exc.__class__.__name__
        )
    return HTTPException(status=500, message="Internal Server Error")
