from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Literal

from flask import Blueprint, jsonify, render_template

from realtime.bus import bus
from realtime.observable import ObservableList

calendar_bp = Blueprint("calendar_demo", __name__, url_prefix="/product-demos")

@dataclass
class Reservation:
    _id: str
    name: str
    date_start: datetime
    date_end: datetime
    student_id: str
    status: Literal["ACTIVE", "DECLINED", "CANCELED"]


@dataclass
class CalendarData:
    # Not a plain list anymore — assigned after construction below.
    reservations: List[Reservation] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _to_event(r: Reservation) -> dict:
    return {
        "id": r._id,
        "name": r.name,
        "start": r.date_start.isoformat(),
        "end": r.date_end.isoformat(),
        "student_id": r.student_id,
        "status": r.status,
    }

# The notifier closes over the bus + room so the list stays transport-agnostic.
def _notify(event: str, payload: dict) -> None:
    bus.emit_safe(event, payload, room=bus.CALENDAR_ROOM)


# ---------------------------------------------------------------------------
# In-memory state
# ---------------------------------------------------------------------------

now = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
base = now.replace(day=1)

appoint_date = lambda day, hour=9, minute=0: base + timedelta(
    days=day, hours=hour, minutes=minute
)

current_dates = CalendarData()
current_dates.reservations = ObservableList(
    serialize=_to_event,
    notify=_notify,
    created_event="calendar:created",
)
# Seed WITHOUT broadcasting (page load has no listeners yet): use list.extend
# on the base class to bypass the override.
list.extend(
    current_dates.reservations,
    [
        Reservation(
            _id="r-2-9",
            name="Ana López",
            date_start=appoint_date(day=2, hour=9),
            date_end=appoint_date(day=2, hour=10),
            student_id="s-29",
            status="ACTIVE",
        ),
        Reservation(
            _id="r-5-11",
            name="Carlos Ruiz",
            date_start=appoint_date(day=5, hour=11),
            date_end=appoint_date(day=5, hour=13),
            student_id="s-511",
            status="ACTIVE",
        ),
    ],
)

def _snapshot() -> list:
    return [_to_event(r) for r in current_dates.reservations]

bus.register_calendar_socket(snapshot_provider=_snapshot)


# ---------------------------------------------------------------------------
# Routes — now genuinely declarative
# ---------------------------------------------------------------------------

@calendar_bp.route("/")
def calendar_demo():
    return render_template("demo_bot.html", events=_snapshot())


@calendar_bp.route("/generate-random", methods=["POST"])
def generate_random():
    day = random.randint(0, 7)
    hour = random.randint(8, 17)
    start = appoint_date(day=day, hour=hour)

    reservation = Reservation(
        _id=f"r-rand-{random.randint(1000, 9999)}",
        name=f"Student {random.randint(1, 100)}",
        date_start=start,
        date_end=start + timedelta(hours=1),
        student_id=f"s-rand-{random.randint(100, 999)}",
        status="ACTIVE",
    )

    # The ObservableList emits a SocketIO event.
    current_dates.reservations.append(reservation)

    return jsonify(_to_event(reservation)), 200