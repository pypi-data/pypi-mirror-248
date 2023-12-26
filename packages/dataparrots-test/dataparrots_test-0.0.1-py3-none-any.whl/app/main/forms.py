from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class RegisterConnectionForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    db_type = StringField('Database Type', validators=[DataRequired()])
    db_name = StringField('Database Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    ip_address = StringField('IP Address', validators=[DataRequired()])
    port_number = StringField('Port Number', validators=[DataRequired()])
    ds_name = StringField('ODBC DSN', validators=[DataRequired()])
    
    submit = SubmitField('Register')
