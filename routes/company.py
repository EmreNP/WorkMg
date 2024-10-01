from flask import Blueprint, app, render_template, redirect, url_for, flash
from forms import CompanyForm
from models import db,Company

company_bp = Blueprint('company', __name__)

@company_bp.route('/companies')
def list_companies():
    companies = Company.query.all()  # Corrected query
    return render_template('company/list.html', companies=companies)

@company_bp.route('/company/new', methods=['GET', 'POST'])
def create_company():
    form = CompanyForm()
    if form.validate_on_submit():
        new_company = Company(name=form.name.data, authorized=form.authorized.data,
                                  authorized_number=form.authorized_number.data, price_company=form.price_company.data)
        db.session.add(new_company)
        db.session.commit()
        flash('Company created successfully!')
        return redirect(url_for('company.list_companies'))
    return render_template('company/create.html', form=form)

@company_bp.route('/company/update/<int:id>', methods=['GET', 'POST'])
def update_company(id):
    company = Company.query.get_or_404(id)
    form = CompanyForm(obj=company)
    if form.validate_on_submit():
        form.populate_obj(company)
        db.session.commit()
        flash('Company updated successfully!')
        return redirect(url_for('company.list_companies'))
    return render_template('company/update.html', form=form)

@company_bp.route('/company/delete/<int:id>', methods=['POST'])
def delete_company(id):
    company = Company.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    flash('Company deleted successfully!')
    return redirect(url_for('company.list_companies'))


@company_bp.route('/company/<int:company_id>')
def company_detail(company_id):
    company = Company.query.get_or_404(company_id)
    jobs = company.jobs
    job_details = []
    total_amount = 0

    for job in jobs:
        payment = job.pcs_plaster * company.price_company
        total_amount += payment  # Sum up the total payment for all jobs
        
        job_details.append({
            'description': job.description,
            'pcs_plaster': job.pcs_plaster,
            'company': job.company.name,
            'total_payment': payment
        })

    return render_template('company/detail.html', company=company, jobs=job_details, total_amount=total_amount)