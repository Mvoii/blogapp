from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from flask_login import current_user
from flask_blog.models import User

class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators = [DataRequired(), Length(min=2, max=20)])
    email = StringField("Email",
                        validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    confirm_password = PasswordField("Confirm Password",
                                     validators = [DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")
    
    # custom validation
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("Username is already taken")
    
        # custom validation
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError("Email is already taken")
    
class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")
    
# update account form
class UpdateAccountForm(FlaskForm):
    username = StringField("Username",
                           validators = [DataRequired(), Length(min=2, max=20)])
    email = StringField("Email",
                        validators = [DataRequired(), Email()])
    #password = PasswordField("Password", validators = [DataRequired()])
    #confirm_password = PasswordField("Confirm Password",
    #                                 validators = [DataRequired(), EqualTo("password")])
    
    picture = FileField("Update Profile Picture", validators=[FileAllowed(["jpg", "png", "jpeg"])])
    submit = SubmitField("update")
    
    # custom validation
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username is already taken")
    
        # custom validation
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError("Email is already taken")

