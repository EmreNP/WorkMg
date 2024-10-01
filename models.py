from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Company(db.Model):
    __tablename__ = 'company'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    authorized = db.Column(db.String(100), nullable=False)
    authorized_number = db.Column(db.String(20), nullable=False)
    price_company = db.Column(db.Float, nullable=False)
    
    jobs = db.relationship('Job', backref='company', lazy=True)

    def __repr__(self):
        return f"<Company {self.name}>"

jobs_employees = db.Table('jobs_employees',
    db.Column('job_id', db.Integer, db.ForeignKey('job.id'), primary_key=True),
    db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'), primary_key=True)
)

class Employee(db.Model):
    __tablename__ = 'employee'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employee_number = db.Column(db.String(20), nullable=False)
    price_employee = db.Column(db.Float, nullable=False)
    
    jobs = db.relationship('Job', secondary=jobs_employees, back_populates='employees')
    
    def __repr__(self):
        return f"<Employee {self.name}>"

class Job(db.Model):
    __tablename__ = 'job'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    pcs_plaster = db.Column(db.Integer, nullable=False)
    
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    
    # Many-to-many relationship between Job and Employee
    employees = db.relationship('Employee', secondary=jobs_employees, back_populates='jobs')
    
    # Calculated property for pcs_per_person
    @property
    def pcs_per_person(self):
        # Avoid division by zero error if there are no employees
        if len(self.employees) == 0:
            return 0
        return self.pcs_plaster / len(self.employees)
    
    def __repr__(self):
        return f"<Job {self.description}>"

