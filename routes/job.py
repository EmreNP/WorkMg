from flask import Blueprint, render_template, redirect, url_for, flash
from forms import JobForm
from models import Company, Employee, Job, db

job_bp = Blueprint('job', __name__)

@job_bp.route('/jobs')
def list_jobs():
    jobs = Job.query.all()
    return render_template('job/list.html', jobs=jobs)

@job_bp.route('/job/new', methods=['GET', 'POST'])
def create_job():
    form = JobForm()
    form.company.choices = [(c.id, c.name) for c in Company.query.all()]
    form.employees.choices = [(e.id, e.name) for e in Employee.query.all()]

    if form.validate_on_submit():
        new_job = Job(description=form.description.data, pcs_plaster=form.pcs_plaster.data,
                         company_id=form.company.data)
        selected_employees = Employee.query.filter(Employee.id.in_(form.employees.data)).all()
        new_job.employees = selected_employees
        db.session.add(new_job)
        db.session.commit()
        flash('Job created successfully!')
        return redirect(url_for('job.list_jobs'))

    return render_template('job/create.html', form=form)

@job_bp.route('/job/update/<int:id>', methods=['GET', 'POST'])
def update_job(id):
    job = Job.query.get_or_404(id)
    form = JobForm(obj=job)
    if form.validate_on_submit():
        form.populate_obj(job)
        db.session.commit()
        flash('Job updated successfully!')
        return redirect(url_for('job.list_jobs'))
    return render_template('job/update.html', form=form)

@job_bp.route('/job/delete/<int:id>', methods=['POST'])
def delete_job(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted successfully!')
    return redirect(url_for('job.list_jobs'))
