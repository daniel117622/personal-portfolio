"""
Real-Time Event Bus.

Centralized WebSocket hub for live updates and monitoring. Designed to
decouple transport from business logic, ensuring that socket failures never
crash critical application paths.
"""

from __future__ import annotations
from typing import Any, Callable
from flask_socketio import SocketIO, emit, join_room
from logger import get_logger

logger = get_logger(__name__)

class RealTimeBus:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.socketio = SocketIO(
            cors_allowed_origins="*",
            async_mode="eventlet",
        )
        self.CALENDAR_ROOM = "calendar"
        self._initialized = True
        logger.info("RealTimeBus bootstrapped correctly")

    def init_app(self, app) -> None:
        """Bind the socketio instance to the Flask app in create_app."""
        self.socketio.init_app(app)

    def emit_safe(
        self, event: str, payload: Any, room: str | None = None
    ) -> bool:
        """Broadcast without letting a socket error break the caller.

        Returns True on success, False on failure (sentinel style).
        """
        if not event:
            return False
        try:
            self.socketio.emit(event, payload, to=room)
            return True
        except Exception:
            logger.warning(
                "emit_safe failed for event %r", event, exc_info=True
            )
            return False

    def register_calendar_socket(
        self, snapshot_provider: Callable[[], list]
    ) -> None:
        """Wire the calendar room handlers once.

        snapshot_provider returns the current event list so the bus stays
        ignorant of the controller's state — it just asks for a snapshot.
        """

        @self.socketio.on("join_calendar")
        def _on_join_calendar():
            join_room(self.CALENDAR_ROOM)
            emit("calendar:snapshot", snapshot_provider())


# Export a ready-to-use instance for the controllers
bus = RealTimeBus()