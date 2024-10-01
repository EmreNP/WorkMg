from flask import Blueprint, app, render_template, redirect, url_for, flash
from forms import EmployeeForm
from models import Employee, db

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/employees')
def list_employees():
    employees = Employee.query.all()
    return render_template('employee/list.html', employees=employees)

@employee_bp.route('/employee/new', methods=['GET', 'POST'])
def create_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        new_employee = Employee(name=form.name.data, employee_number=form.employee_number.data, price_employee=form.price_employee.data)
        db.session.add(new_employee)
        db.session.commit()
        flash('Employee created successfully!')
        return redirect(url_for('employee.list_employees'))
    return render_template('employee/create.html', form=form)

@employee_bp.route('/employee/update/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)
    if form.validate_on_submit():
        form.populate_obj(employee)
        db.session.commit()
        flash('Employee updated successfully!')
        return redirect(url_for('employee.list_employees'))
    return render_template('employee/update.html', form=form)

@employee_bp.route('/employee/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully!')
    return redirect(url_for('employee.list_employees'))

@employee_bp.route('/employee/<int:employee_id>')
def employee_detail(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    jobs = employee.jobs
    job_details = []
    total_amount = 0

    for job in jobs:
        pcs_per_person = job.pcs_per_person
        payment = pcs_per_person * employee.price_employee
        total_amount += payment  # Sum up the total payment for all jobs
        
        job_details.append({
            'description': job.description,
            'pcs_plaster': job.pcs_plaster,
            'company': job.company.name,
            'pcs_per_person': pcs_per_person,
            'total_payment': payment
        })

    return render_template('employee/detail.html', employee=employee, jobs=job_details, total_amount=total_amount)

