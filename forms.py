from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField, StringField, FloatField, SubmitField
from wtforms.validators import DataRequired

class CompanyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    authorized = StringField('Authorized', validators=[DataRequired()])
    authorized_number = StringField('Authorized Number', validators=[DataRequired()])
    price_company = FloatField('Price', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    employee_number = StringField('Employee Number', validators=[DataRequired()])
    price_employee = FloatField('Price', validators=[DataRequired()])
    submit = SubmitField('Submit')

class JobForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    pcs_plaster = FloatField('Pcs Plaster', validators=[DataRequired()])
    company = SelectField('Company', choices=[], coerce=int)
    employees = SelectMultipleField('Employee', choices=[], coerce=int)
    submit = SubmitField('Submit')
