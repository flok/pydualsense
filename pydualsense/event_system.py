from typing import Callable, Dict, List, Optional, Tuple


class Event:
    """
    Base class for the event driven system
    """

    def __init__(
        self,
        available: bool = True,
        dispatcher: Optional[EventDispatcher] = None,
        coalesce: bool = False,
    ) -> None:
        """
        initialise event system
        """
        self._event_handler: List[Callable[..., object]] = []
        self.available = available
        self._dispatcher = dispatcher
        self.coalesce = coalesce

    def subscribe(self, fn: Callable[..., object]) -> "Event":
        """
        add a event subscription

        Args:
            fn (function): _description_
        """
        if not self.available:
            raise ValueError("Event unavailable")
        self._event_handler.append(fn)
        return self

    def unsubscribe(self, fn: Callable[..., object]) -> "Event":
        """
        delete event subscription fn

        Args:
            fn (function): _description_
        """
        if not self.available:
            raise ValueError("Event unavailable")
        self._event_handler.remove(fn)
        return self

    def __iadd__(self, fn: Callable[..., object]) -> "Event":
        """
        add event subscription fn

        Args:
            fn (function): _description_
        """
        if not self.available:
            raise ValueError("Event unavailable")
        self._event_handler.append(fn)
        return self

    def __isub__(self, fn: Callable[..., object]) -> "Event":
        """
        delete event subscription fn

        Args:
            fn (function): _description_
        """
        if not self.available:
            raise ValueError("Event unavailable")
        self._event_handler.remove(fn)
        return self

    def __call__(self, *args: object, **kwargs: object) -> None:
        """
        calls all event subscription functions
        """
        if not self.available:
            raise ValueError("Event unavailable")
        handlers = tuple(self._event_handler)
        if self._dispatcher is not None:
            self._dispatcher(self, handlers, args, kwargs)
            return

        for eventhandler in handlers:
            eventhandler(*args, **kwargs)


# aliases defined after Event so EventDispatcher can reference it
EventHandlers = Tuple[Callable[..., object], ...]
EventCall = Tuple[EventHandlers, Tuple[object, ...], Dict[str, object]]
EventDispatcher = Callable[[Event, EventHandlers, Tuple[object, ...], Dict[str, object]], None]
