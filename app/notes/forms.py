import datetime
from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, TextAreaField, DateTimeLocalField
from wtforms.validators import DataRequired, AnyOf, Length


class CustomDateTimeField(DateTimeLocalField):
    def process_data(self, value):
        if isinstance(value, str):
            try:
                self.data = datetime.datetime.fromisoformat(value)
            except ValueError:
                self.data = None
        else:
            self.data = value


class NoteForm(FlaskForm):
    content = TextAreaField("content", validators=[DataRequired(), Length(max=200)])
    tags = StringField("tags")
    public = RadioField(
        "public",
        default="True",
        choices=[("True", "Publish to everyone"), ("False", "Hide in archive")],
        validators=[DataRequired(), AnyOf(values=["True", "False"])],
    )
    published_at = CustomDateTimeField(
        "published_at",
        default=datetime.datetime.now(datetime.UTC),  # type: ignore
    )
