from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField(
        "username", validators=[DataRequired(), Length(min=3, max=20)]
    )
    submit = SubmitField("Log in")
