from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, TextAreaField
from wtforms.validators import DataRequired, AnyOf, Length


class NoteForm(FlaskForm):
    content = TextAreaField("content", validators=[DataRequired(), Length(max=200)])
    tags = StringField("tags")
    public = RadioField(
        "public",
        default="True",
        choices=[("True", "Publish to everyone"), ("False", "Hide in archive")],
        validators=[DataRequired(), AnyOf(values=["True", "False"])],
    )
