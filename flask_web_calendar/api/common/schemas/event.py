from marshmallow import Schema, fields


class EventOutputSchema(Schema):
    """Event schema."""
    id = fields.UUID(
        required=True, example="b68256c0-70fa-40de-bb2a-7dac113b3702")
    event = fields.Str(required=True, example="Video confirence.")
    date = fields.Date(required=True, example="2022-02-12")


class EventInputSchema(Schema):
    """Event form schema."""
    event = fields.Str(
        required=True,
        error_messages={
            "required": "The event name is required!"
        },
        example="Video confirence."
    )
    date = fields.Date(
        format="%Y-%m-%d",
        required=True,
        error_messages={
            "required": "The event date with the correct format is required! The correct format is YYYY-MM-DD!",
            "validator_failed": "The event date with the correct format is required! The correct format is YYYY-MM-DD!"
        },
        example="2022-02-12"
    )


class EventQuerystringSchema(Schema):
    """Event query string schema."""
    start_time = fields.Date(
        format="%Y-%m-%d",
        error_messages={
            "validator_failed": "Invalid start_time arg format. The correct format is YYYY-MM-DD!"
        }
    )
    end_time = fields.Date(
        format="%Y-%m-%d",
        error_messages={
            "validator_failed": "Invalid end_time arg format. The correct format is YYYY-MM-DD!"
        }
    )


event_schema_in = EventInputSchema()
event_schema_out = EventOutputSchema()
events_schema_out = EventOutputSchema(many=True)
event_query_schema = EventQuerystringSchema()
