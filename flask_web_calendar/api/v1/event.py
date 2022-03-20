import datetime

from flask import jsonify
from flask_web_calendar.db import db
from webargs.flaskparser import use_args

from ..common.models.event import Event
from ..common.schemas import event as schemas
from .api import api


@api.route("/event", methods=["GET"])
@use_args(schemas.event_query_schema, location="query", error_status_code=400)
def event_get(args):
    """Return all events."""
    query = Event.query
    if args:
        start_time = args.get("start_time")
        end_time = args.get("end_time")
        if start_time:
            query = query.filter(Event.date >= start_time)
        if end_time:
            query = query.filter(Event.date < end_time)
    return schemas.events_schema_out.dumps(query.all())


@api.route("/event/today", methods=["GET"])
def event_get_today():
    """Return events for today."""
    events = Event.query.filter(
        Event.date == datetime.date.today()).all()
    if not events:
        return jsonify({"data": "There are no events for today!"})
    return schemas.event_query_schema.dumps(events)


@api.route("/event/<int:user_id>", methods=["GET"])
def event_get_by_event_id(event_id):
    """Return event by event_id."""
    event = Event.query.filter(Event.id == event_id).one_or_none()
    if not event:
        return jsonify({"message": "The event doesn't exist!"})
    return schemas.event_schema_out.dump(event)


@api.route("/event", methods=["POST"])
@use_args(schemas.event_schema_in, location="form", error_status_code=400)
def event_post(args):
    """Create new event."""
    event = Event(event=args["event"], date=args["date"])
    db.session.add(event)
    db.session.commit()
    return jsonify({
        "message": "The event has been added!",
        "event": event.event,
        "date": event.date.isoformat()  # pylint: disable=no-member
    })


@api.route("/event", methods=["DELETE"])
def event_delete_by_user_id(event_id):
    """Delete event by event_id."""
    event = Event.query.filter(Event.id == event_id).one_or_none()
    if not event:
        return jsonify({"message": "The event doesn't exist!"})
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "The event has been deleted!"})
