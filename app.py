"""
HRMS-Babylon - Human Resource Management System
Main Flask Application
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///hrms_babylon.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# Models
class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    manager_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    employees = db.relationship('Employee', backref='department', lazy=True)


class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.Enum('M', 'F', 'Other', name='gender_enum'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    position = db.Column(db.String(100))
    hire_date = db.Column(db.Date, nullable=False)
    employment_type = db.Column(db.Enum('Full-Time', 'Part-Time', 'Contract', 'Temporary', name='employment_type_enum'), default='Full-Time')
    salary = db.Column(db.Numeric(10, 2))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)


# Routes
@app.route('/')
def index():
    """Home page / Dashboard"""
    try:
        total_employees = Employee.query.filter_by(is_active=True).count()
        total_departments = Department.query.filter_by(is_active=True).count()
    except Exception as e:
        app.logger.error(f"Database error: {str(e)}")
        total_employees = 0
        total_departments = 0
    
    return render_template('index.html', 
                         total_employees=total_employees,
                         total_departments=total_departments)


@app.route('/departments')
def departments():
    """List all departments"""
    try:
        departments_list = Department.query.filter_by(is_active=True).all()
    except Exception as e:
        app.logger.error(f"Database error: {str(e)}")
        departments_list = []
        flash('Database connection error. Please check your configuration.', 'error')
    
    return render_template('departments.html', departments=departments_list)


@app.route('/departments/add', methods=['GET', 'POST'])
def add_department():
    """Add a new department"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Department name is required!', 'error')
            return redirect(url_for('add_department'))
        
        try:
            new_department = Department(name=name, description=description)
            db.session.add(new_department)
            db.session.commit()
            flash('Department added successfully!', 'success')
            return redirect(url_for('departments'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding department: {str(e)}', 'error')
    
    return render_template('add_department.html')


@app.route('/employees')
def employees():
    """List all employees"""
    try:
        employees_list = Employee.query.filter_by(is_active=True).all()
    except Exception as e:
        app.logger.error(f"Database error: {str(e)}")
        employees_list = []
        flash('Database connection error. Please check your configuration.', 'error')
    
    return render_template('employees.html', employees=employees_list)


@app.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    """Add a new employee"""
    try:
        departments_list = Department.query.filter_by(is_active=True).all()
    except Exception as e:
        app.logger.error(f"Database error: {str(e)}")
        departments_list = []
    
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        department_id = request.form.get('department_id')
        position = request.form.get('position')
        hire_date = request.form.get('hire_date')
        
        if not all([first_name, last_name, email, hire_date]):
            flash('Required fields missing!', 'error')
            return redirect(url_for('add_employee'))
        
        try:
            new_employee = Employee(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                department_id=department_id if department_id else None,
                position=position,
                hire_date=datetime.strptime(hire_date, '%Y-%m-%d').date()
            )
            db.session.add(new_employee)
            db.session.commit()
            flash('Employee added successfully!', 'success')
            return redirect(url_for('employees'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding employee: {str(e)}', 'error')
    
    return render_template('add_employee.html', departments=departments_list)


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 3000))
    app.run(debug=debug_mode, host=host, port=port)
