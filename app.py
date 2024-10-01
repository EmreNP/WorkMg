from flask import Flask, render_template
from flask_migrate import Migrate
from config import Config
from models import db
from routes.company import company_bp
from routes.employee import employee_bp
from routes.job import job_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(company_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(job_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
