import datetime

from flask import jsonify
from flask.views import MethodView
from flask_web_calendar.db import db
from webargs.flaskparser import use_args

from ..common.models.event import Event
from ..common.schemas import event as schemas


class EventResource(MethodView):
    """Event API.
    ---
    x-extension: metadata
    """

    # pylint: disable=missing-function-docstring
    # pylint: disable=no-self-use

    @use_args(schemas.event_query_schema, location="query", error_status_code=400)
    def get(self, args, event_id=None, today=False):
        if event_id:
            event = Event.query.filter(Event.id == event_id).one_or_none()
            if not event:
                return jsonify({"message": "The event doesn't exist!"})
            return schemas.event_schema_out.dump(event)
        if today:
            events = Event.query.filter(
                Event.date == datetime.date.today()).all()
            if not events:
                return jsonify({"data": "There are no events for today!"})
            return schemas.event_query_schema.dumps(events)
        query = Event.query
        if args:
            start_time = args.get("start_time")
            end_time = args.get("end_time")
            if start_time:
                query = query.filter(Event.date >= start_time)
            if end_time:
                query = query.filter(Event.date < end_time)
        return schemas.events_schema_out.dumps(query.all())

    @use_args(schemas.event_schema_in, location="form", error_status_code=400)
    def post(self, args):
        event = Event(event=args["event"], date=args["date"])
        db.session.add(event)
        db.session.commit()
        return jsonify({
            "message": "The event has been added!",
            "event": event.event,
            "date": event.date.isoformat()  # pylint: disable=no-member
        })

    def delete(self, event_id):
        event = Event.query.filter(Event.id == event_id).one_or_none()
        if not event:
            return jsonify({"message": "The event doesn't exist!"})
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "The event has been deleted!"})

    @classmethod
    def register(cls, mod):
        """Register Resource."""
        cls.view = cls.as_view("event")
        mod.add_url_rule("/event/<int:user_id>",
                         view_func=cls.view, methods=["GET", "DELETE"])
        mod.add_url_rule("/event/today", defaults={"today": True},
                         view_func=cls.view, methods=["GET", ])
        mod.add_url_rule("/event/", view_func=cls.view,
                         methods=["GET", "POST"])
        return mod
