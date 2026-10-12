from __future__ import annotations

from typing import Any, Callable, Iterable, TypeVar

T = TypeVar("T")

# A callback that turns one item into an emittable payload.
Serializer = Callable[[T], Any]
# A callback that performs the actual broadcast.
Notifier = Callable[[str, Any], None]


class ObservableList(list):
    """A list that announces mutations through an injected notifier.

    It knows *nothing* about sockets — it's handed a serializer (item -> dict)
    and a notifier (event, payload -> None). That keeps transport out of the
    collection and avoids a circular import with the bus.
    """

    def __init__(
        self,
        iterable: Iterable[T] | None = None,
        *,
        serialize: Serializer,
        notify: Notifier,
        created_event: str = "calendar:created",
    ) -> None:
        super().__init__(iterable or [])
        self._serialize = serialize
        self._notify = notify
        self._created_event = created_event

    # ---- mutating overrides -------------------------------------------

    def append(self, item: T) -> None:
        super().append(item)
        self._announce(item)

    def extend(self, items: Iterable[T]) -> None:
        # Materialize once so we can both store and announce each item.
        batch = list(items)
        super().extend(batch)
        for item in batch:
            self._announce(item)

    # ---- internal -----------------------------------------------------

    def _announce(self, item: T) -> None:
        # Guard: a missing serializer/notifier must never crash a write.
        if self._serialize is None or self._notify is None:
            return
        self._notify(self._created_event, self._serialize(item))