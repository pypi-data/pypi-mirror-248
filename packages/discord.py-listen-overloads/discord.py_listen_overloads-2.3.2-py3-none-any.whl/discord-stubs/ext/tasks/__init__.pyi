"""
The MIT License (MIT)

Copyright (c) 2015-present Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

import asyncio
import datetime
import logging
from typing import (
    Any,
    Callable,
    Coroutine,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)

import aiohttp
import discord
import inspect

from collections.abc import Sequence
from discord.backoff import ExponentialBackoff
from discord.utils import MISSING

_log = logging.getLogger(__name__)

# fmt: off
__all__ = (
    'loop',
)
# fmt: on

T = TypeVar("T")
_func = Callable[..., Coroutine[Any, Any, Any]]
LF = TypeVar("LF", bound=_func)
FT = TypeVar("FT", bound=_func)
ET = TypeVar("ET", bound=Callable[[Any, BaseException], Coroutine[Any, Any, Any]])

def is_ambiguous(dt: datetime.datetime) -> bool:
    ...

def is_imaginary(dt: datetime.datetime) -> bool:
    ...

def resolve_datetime(dt: datetime.datetime) -> datetime.datetime:
    ...

class SleepHandle:
    __slots__ = ("future", "loop", "handle")

    def __init__(self, dt: datetime.datetime, *, loop: asyncio.AbstractEventLoop) -> None:
        ...
    def recalculate(self, dt: datetime.datetime) -> None:
        ...
    def wait(self) -> asyncio.Future[Any]:
        ...
    def done(self) -> bool:
        ...
    def cancel(self) -> None:
        ...

class Loop(Generic[LF]):
    """A background task helper that abstracts the loop and reconnection logic for you.

    The main interface to create this is through :func:`loop`.
    """

    def __init__(
        self,
        coro: LF,
        seconds: float,
        hours: float,
        minutes: float,
        time: Union[datetime.time, Sequence[datetime.time]],
        count: Optional[int],
        reconnect: bool,
        name: Optional[str],
    ) -> None:
        ...
    async def _call_loop_function(self, name: str, *args: Any, **kwargs: Any) -> None:
        ...
    def _try_sleep_until(self, dt: datetime.datetime) -> Any:
        ...
    def _is_relative_time(self) -> bool:
        ...
    def _is_explicit_time(self) -> bool:
        ...
    async def _loop(self, *args: Any, **kwargs: Any) -> None:
        ...
    def __get__(self, obj: T, objtype: Type[T]) -> Loop[LF]:
        ...
    @property
    def seconds(self) -> Optional[float]:
        """Optional[:class:`float`]: Read-only value for the number of seconds
        between each iteration. ``None`` if an explicit ``time`` value was passed instead.

        .. versionadded:: 2.0
        """
        ...
    @property
    def minutes(self) -> Optional[float]:
        """Optional[:class:`float`]: Read-only value for the number of minutes
        between each iteration. ``None`` if an explicit ``time`` value was passed instead.

        .. versionadded:: 2.0
        """
        ...
    @property
    def hours(self) -> Optional[float]:
        """Optional[:class:`float`]: Read-only value for the number of hours
        between each iteration. ``None`` if an explicit ``time`` value was passed instead.

        .. versionadded:: 2.0
        """
       ...
    @property
    def time(self) -> Optional[List[datetime.time]]:
        """Optional[List[:class:`datetime.time`]]: Read-only list for the exact times this loop runs at.
        ``None`` if relative times were passed instead.

        .. versionadded:: 2.0
        """
        ...
    @property
    def current_loop(self) -> int:
        """:class:`int`: The current iteration of the loop."""
        ...
    @property
    def next_iteration(self) -> Optional[datetime.datetime]:
        """Optional[:class:`datetime.datetime`]: When the next iteration of the loop will occur.

        .. versionadded:: 1.3
        """
        ...
    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        r"""|coro|

        Calls the internal callback that the task holds.

        .. versionadded:: 1.6

        Parameters
        ------------
        \*args
            The arguments to use.
        \*\*kwargs
            The keyword arguments to use.
        """
        ...
    def start(self, *args: Any, **kwargs: Any) -> asyncio.Task[None]:
        r"""Starts the internal task in the event loop.

        Parameters
        ------------
        \*args
            The arguments to use.
        \*\*kwargs
            The keyword arguments to use.

        Raises
        --------
        RuntimeError
            A task has already been launched and is running.

        Returns
        ---------
        :class:`asyncio.Task`
            The task that has been created.
        """

        ...
    def stop(self) -> None:
        r"""Gracefully stops the task from running.

        Unlike :meth:`cancel`\, this allows the task to finish its
        current iteration before gracefully exiting.

        .. note::

            If the internal function raises an error that can be
            handled before finishing then it will retry until
            it succeeds.

            If this is undesirable, either remove the error handling
            before stopping via :meth:`clear_exception_types` or
            use :meth:`cancel` instead.

        .. versionchanged:: 2.0
            Calling this method in :meth:`before_loop` will stop the loop before the initial iteration is run.

        .. versionadded:: 1.2
        """
        ...
    def _can_be_cancelled(self) -> bool:
        ...
    def cancel(self) -> None:
        """Cancels the internal task, if it is running."""
        ...
    def restart(self, *args: Any, **kwargs: Any) -> None:
        r"""A convenience method to restart the internal task.

        .. note::

            Due to the way this function works, the task is not
            returned like :meth:`start`.

        Parameters
        ------------
        \*args
            The arguments to use.
        \*\*kwargs
            The keyword arguments to use.
        """

        ...
    def add_exception_type(self, *exceptions: Type[BaseException]) -> None:
        r"""Adds exception types to be handled during the reconnect logic.

        By default the exception types handled are those handled by
        :meth:`discord.Client.connect`\, which includes a lot of internet disconnection
        errors.

        This function is useful if you're interacting with a 3rd party library that
        raises its own set of exceptions.

        Parameters
        ------------
        \*exceptions: Type[:class:`BaseException`]
            An argument list of exception classes to handle.

        Raises
        --------
        TypeError
            An exception passed is either not a class or not inherited from :class:`BaseException`.
        """
        ...
    def clear_exception_types(self) -> None:
        """Removes all exception types that are handled.

        .. note::

            This operation obviously cannot be undone!
        """
        ...
    def remove_exception_type(self, *exceptions: Type[BaseException]) -> bool:
        r"""Removes exception types from being handled during the reconnect logic.

        Parameters
        ------------
        \*exceptions: Type[:class:`BaseException`]
            An argument list of exception classes to handle.

        Returns
        ---------
        :class:`bool`
            Whether all exceptions were successfully removed.
        """
        ...
    def get_task(self) -> Optional[asyncio.Task[None]]:
        """Optional[:class:`asyncio.Task`]: Fetches the internal task or ``None`` if there isn't one running."""
        ...
    def is_being_cancelled(self) -> bool:
        """Whether the task is being cancelled."""
        ...
    def failed(self) -> bool:
        """:class:`bool`: Whether the internal task has failed.

        .. versionadded:: 1.2
        """
        ...
    def is_running(self) -> bool:
        """:class:`bool`: Check if the task is currently running.

        .. versionadded:: 1.4
        """
        ...
    async def _error(self, *args: Any) -> None:
        ...
    def before_loop(self, coro: FT) -> FT:
        """A decorator that registers a coroutine to be called before the loop starts running.

        This is useful if you want to wait for some bot state before the loop starts,
        such as :meth:`discord.Client.wait_until_ready`.

        The coroutine must take no arguments (except ``self`` in a class context).

        .. versionchanged:: 2.0
            Calling :meth:`stop` in this coroutine will stop the loop before the initial iteration is run.

        Parameters
        ------------
        coro: :ref:`coroutine <coroutine>`
            The coroutine to register before the loop runs.

        Raises
        -------
        TypeError
            The function was not a coroutine.
        """

        ...
    def after_loop(self, coro: FT) -> FT:
        """A decorator that registers a coroutine to be called after the loop finishes running.

        The coroutine must take no arguments (except ``self`` in a class context).

        .. note::

            This coroutine is called even during cancellation. If it is desirable
            to tell apart whether something was cancelled or not, check to see
            whether :meth:`is_being_cancelled` is ``True`` or not.

        Parameters
        ------------
        coro: :ref:`coroutine <coroutine>`
            The coroutine to register after the loop finishes.

        Raises
        -------
        TypeError
            The function was not a coroutine.
        """
        ...
    def error(self, coro: ET) -> ET:
        """A decorator that registers a coroutine to be called if the task encounters an unhandled exception.

        The coroutine must take only one argument the exception raised (except ``self`` in a class context).

        By default this logs to the library logger however it could be
        overridden to have a different implementation.

        .. versionadded:: 1.4

        .. versionchanged:: 2.0

            Instead of writing to ``sys.stderr``, the library's logger is used.

        Parameters
        ------------
        coro: :ref:`coroutine <coroutine>`
            The coroutine to register in the event of an unhandled exception.

        Raises
        -------
        TypeError
            The function was not a coroutine.
        """
        ...
    def _get_next_sleep_time(self, now: datetime.datetime = ...) -> datetime.datetime:
        ...
    def _start_time_relative_to(self, now: datetime.datetime) -> Optional[int]:
        ...
    def _get_time_parameter(
        self,
        time: Union[datetime.time, Sequence[datetime.time]],
        *,
        dt: Type[datetime.time] = ...,
        utc: datetime.timezone = ...,
    ) -> List[datetime.time]:
        ...
    def change_interval(
        self,
        *,
        seconds: float = ...,
        minutes: float = ...,
        hours: float = ...,
        time: Union[datetime.time, Sequence[datetime.time]] = ...,
    ) -> None:
        """Changes the interval for the sleep time.

        .. versionadded:: 1.2

        Parameters
        ------------
        seconds: :class:`float`
            The number of seconds between every iteration.
        minutes: :class:`float`
            The number of minutes between every iteration.
        hours: :class:`float`
            The number of hours between every iteration.
        time: Union[:class:`datetime.time`, Sequence[:class:`datetime.time`]]
            The exact times to run this loop at. Either a non-empty list or a single
            value of :class:`datetime.time` should be passed.
            This cannot be used in conjunction with the relative time parameters.

            .. versionadded:: 2.0

            .. note::

                Duplicate times will be ignored, and only run once.

        Raises
        -------
        ValueError
            An invalid value was given.
        TypeError
            An invalid value for the ``time`` parameter was passed, or the
            ``time`` parameter was passed in conjunction with relative time parameters.
        """
        ...

def loop(
    *,
    seconds: float = ...,
    minutes: float = ...,
    hours: float = ...,
    time: Union[datetime.time, Sequence[datetime.time]] = ...,
    count: Optional[int] = ...,
    reconnect: bool = ...,
    name: Optional[str] = ...,
) -> Callable[[LF], Loop[LF]]:
    """A decorator that schedules a task in the background for you with
    optional reconnect logic. The decorator returns a :class:`Loop`.

    Parameters
    ------------
    seconds: :class:`float`
        The number of seconds between every iteration.
    minutes: :class:`float`
        The number of minutes between every iteration.
    hours: :class:`float`
        The number of hours between every iteration.
    time: Union[:class:`datetime.time`, Sequence[:class:`datetime.time`]]
        The exact times to run this loop at. Either a non-empty list or a single
        value of :class:`datetime.time` should be passed. Timezones are supported.
        If no timezone is given for the times, it is assumed to represent UTC time.

        This cannot be used in conjunction with the relative time parameters.

        .. note::

            Duplicate times will be ignored, and only run once.

        .. versionadded:: 2.0

    count: Optional[:class:`int`]
        The number of loops to do, ``None`` if it should be an
        infinite loop.
    reconnect: :class:`bool`
        Whether to handle errors and restart the task
        using an exponential back-off algorithm similar to the
        one used in :meth:`discord.Client.connect`.
    name: Optional[:class:`str`]
        The name to assign to the internal task. By default
        it is assigned a name based off of the callable name
        such as ``discord-ext-tasks: function_name``.

        .. versionadded:: 2.4

    Raises
    --------
    ValueError
        An invalid value was given.
    TypeError
        The function was not a coroutine, an invalid value for the ``time`` parameter was passed,
        or ``time`` parameter was passed in conjunction with relative time parameters.
    """

    def decorator(func: LF) -> Loop[LF]: ...
