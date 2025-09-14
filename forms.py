from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, URL

class CourseForm(FlaskForm):
    title = StringField('عنوان الكورس', validators=[DataRequired()])
    description = TextAreaField('وصف الكورس', validators=[DataRequired()])
    image_url = StringField('رابط الصورة', validators=[DataRequired(), URL()])
    registration_form = StringField('رابط استمارة التسجيل', validators=[DataRequired(), URL()])
    submit = SubmitField('إضافة كورس')