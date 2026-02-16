# HRMS-Babylon Setup Guide

This guide will help you set up and run the HRMS-Babylon application.

## Prerequisites

- Python 3.8 or higher
- MySQL database server
- pip (Python package installer)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/hussein-alnidawi/HRMS-Babylon.git
cd HRMS-Babylon
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up MySQL Database

First, ensure your MySQL server is running, then create the database:

```bash
mysql -u root -p < Database/00-Create-Database.sql
```

Optionally, you can also initialize departments:

```bash
mysql -u root -p < Database/01-Departments.sql
```

### 5. Configure Environment Variables

Copy the example environment file and edit it with your settings:

```bash
cp .env.example .env
```

Edit `.env` file with your database credentials:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql://username:password@localhost/hrms_babylon
```

### 6. Run the Application

```bash
python3 app.py
```

The application will start on `http://localhost:3000`

## Accessing the Application

Once the application is running, open your web browser and navigate to:

```
http://localhost:3000
```

## Application Features

### Dashboard
- View system statistics (employees, departments)
- Quick access to common actions
- Overview of system features

### Employee Management
- List all employees
- Add new employees
- View employee details including department, position, and hire date

### Department Management
- List all departments
- Add new departments
- View department information

## Troubleshooting

### Database Connection Error

If you see "Database connection error", check:
1. MySQL server is running
2. Database credentials in `.env` are correct
3. Database `hrms_babylon` exists
4. Database user has proper permissions

### Port Already in Use

If port 3000 is already in use, you can change it in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change to desired port
```

### Module Not Found Errors

Make sure all dependencies are installed:

```bash
pip install -r requirements.txt
```

## Development Mode

The application runs in debug mode by default, which provides:
- Automatic reloading on code changes
- Detailed error messages
- Debug toolbar

For production deployment, set debug mode to False in `app.py`:

```python
app.run(debug=False, host='0.0.0.0', port=3000)
```

## Next Steps

- Configure user authentication
- Implement attendance tracking
- Add leave management functionality
- Set up payroll processing
- Create performance review system
- Add document management

## Support

For issues or questions, please open an issue on the [GitHub repository](https://github.com/hussein-alnidawi/HRMS-Babylon/issues).
