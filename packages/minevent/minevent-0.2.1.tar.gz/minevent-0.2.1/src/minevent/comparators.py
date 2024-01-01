r"""Implement some ``coola`` equality operators for conditions and event
handlers."""

from __future__ import annotations

__all__ = ["ConditionEqualityOperator", "EventHandlerEqualityOperator"]

import logging
from typing import Any

from coola import BaseEqualityOperator, BaseEqualityTester, EqualityTester

from minevent.conditions import BaseCondition
from minevent.handlers import BaseEventHandler

logger = logging.getLogger(__name__)


class ConditionEqualityOperator(BaseEqualityOperator[BaseCondition]):
    r"""Implement an equality operator for ``BaseCondition`` objects.

    Example usage:

    ```pycon
    >>> from coola import EqualityTester
    >>> from minevent import PeriodicCondition, ConditionEqualityOperator
    >>> comparator = ConditionEqualityOperator()
    >>> tester = EqualityTester()
    >>> comparator.equal(tester, PeriodicCondition(freq=3), PeriodicCondition(freq=3))
    True
    >>> comparator.equal(tester, PeriodicCondition(freq=3), PeriodicCondition(freq=2))
    False

    ```
    """

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def clone(self) -> ConditionEqualityOperator:
        return self.__class__()

    def equal(
        self,
        tester: BaseEqualityTester,
        object1: BaseCondition,
        object2: Any,
        show_difference: bool = False,
    ) -> bool:
        if object1 is object2:
            return True
        if not isinstance(object2, BaseCondition):
            if show_difference:
                logger.info(f"object2 is not a `BaseCondition` object: {type(object2)}")
            return False
        object_equal = object1.equal(object2)
        if show_difference and not object_equal:
            logger.info(
                f"`BaseCondition` objects are different\nobject1=\n{object1}\n"
                f"object2=\n{object2}"
            )
        return object_equal


class EventHandlerEqualityOperator(BaseEqualityOperator[BaseEventHandler]):
    r"""Implement an equality operator for ``BaseEventHandler`` objects.

    Example usage:

    ```pycon
    >>> from coola import EqualityTester
    >>> from minevent import EventHandler, EventHandlerEqualityOperator
    >>> def hello_handler() -> None:
    ...     print("Hello!")
    ...
    >>> tester = EqualityTester()
    >>> comparator = EventHandlerEqualityOperator()
    >>> comparator.equal(tester, EventHandler(hello_handler), EventHandler(hello_handler))
    True

    ```
    """

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def clone(self) -> EventHandlerEqualityOperator:
        return self.__class__()

    def equal(
        self,
        tester: BaseEqualityTester,
        object1: BaseEventHandler,
        object2: Any,
        show_difference: bool = False,
    ) -> bool:
        if object1 is object2:
            return True
        if not isinstance(object2, BaseEventHandler):
            if show_difference:
                logger.info(f"object2 is not a `BaseEventHandler` object: {type(object2)}")
            return False
        object_equal = object1.equal(object2)
        if show_difference and not object_equal:
            logger.info(
                f"`BaseEventHandler` objects are different\nobject1=\n{object1}\n"
                f"object2=\n{object2}"
            )
        return object_equal


if not EqualityTester.has_operator(BaseCondition):  # pragma: no cover
    EqualityTester.add_operator(BaseCondition, ConditionEqualityOperator())
if not EqualityTester.has_operator(BaseEventHandler):  # pragma: no cover
    EqualityTester.add_operator(BaseEventHandler, EventHandlerEqualityOperator())
