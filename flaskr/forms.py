from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    choice_array = ['football', 'poetry', 'short story']
    content_type = SelectField(label='Content Type', choices=choice_array)
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    priority = IntegerField('Priority', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    