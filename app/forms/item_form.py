from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length


IMAGE_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "gif"}

class ItemForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    brand = StringField('brand', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired(), Length(min=25, max=255)])
    price = FloatField('price', validators=[DataRequired()])
    preview_img = FileField("preview image", validators=[FileAllowed(list(IMAGE_EXTENSIONS))])
    available_qty = IntegerField('Available Quantity', validators=[DataRequired()])
    submit = SubmitField("submit")
