from typing import Any, Callable, List


# mypy: disable_error_code="type-arg"
class Event:
    """
    Base class for the event driven system
    """

    def __init__(self, available=True) -> None:
        """
        initialise event system
        """
        self._event_handler: List[Callable] = []
        self.available = available

    def subscribe(self, fn: Callable) -> Any:
        """
        add a event subscription

        Args:
            fn (function): _description_
        """
        if not self.available:
            raise ValueError("Event unavailable")
        self._event_handler.append(fn)
        return self

    def unsubscribe(self, fn: Callable) -> Any:
        """
        delete event subscription fn

        Args:
            fn (function): _description_
        """
        if not self.available:
            raise ValueError("Event unavailable")
        self._event_handler.remove(fn)
        return self

    def __iadd__(self, fn: Callable) -> Any:
        """
        add event subscription fn

        Args:
            fn (function): _description_
        """
        if not self.available:
            raise ValueError("Event unavailable")
        self._event_handler.append(fn)
        return self

    def __isub__(self, fn: Callable) -> Any:
        """
        delete event subscription fn

        Args:
            fn (function): _description_
        """
        if not self.available:
            raise ValueError("Event unavailable")
        self._event_handler.remove(fn)
        return self

    def __call__(self, *args, **kwargs) -> None: # type: ignore[arg-type]
        """
        calls all event subscription functions
        """
        if not self.available:
            raise ValueError("Event unavailable")
        for eventhandler in self._event_handler:
            eventhandler(*args, **kwargs)
