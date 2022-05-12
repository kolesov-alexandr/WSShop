from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class AppForm(FlaskForm):
    name = StringField('Название игры', validators=[DataRequired()])
    description = TextAreaField("Описание")
    price = IntegerField('Цена игры', validators=[DataRequired()])
    download_link = StringField('ссылка на скачивание', validators=[DataRequired()])
    submit = SubmitField('Применить')
