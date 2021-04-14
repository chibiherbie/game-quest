from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class BookingForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    address = SelectField('Точка игры (район)', choices=[('Взлётка', 'Взлётка'), ('Центр', 'Центр')])
    dt_start = StringField('Время и дата начала')

    submit = SubmitField('Забронировать')