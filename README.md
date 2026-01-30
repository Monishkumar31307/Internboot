# Online Examination Portal

A comprehensive web-based examination system built with Django and SQLite that enables administrators to create and manage exams, while students can register, take exams, and view their results.

## 🎯 Features

### For Students
- **User Registration & Authentication**: Secure signup and login system
- **Exam Dashboard**: View available and upcoming exams
- **Take Exams**: Attempt exams with real-time countdown timer
- **Auto-Submit**: Automatic submission when time expires
- **Save Progress**: Save answers and continue later
- **View Results**: Detailed results with correct/wrong answers and explanations
- **Performance Analytics**: View scores, percentage, accuracy, and rankings
- **Profile Management**: Update personal information and profile picture

### For Administrators
- **Exam Management**: Create, update, and delete exams
- **Question Bank**: Add, edit, and delete multiple-choice questions
- **Set Exam Parameters**: Define duration, marks, passing criteria, and schedules
- **Student Monitoring**: Track all student attempts and submissions
- **Performance Reports**: Comprehensive reports with statistics and analytics
- **Student Rankings**: View student rankings based on performance
- **Dashboard**: Overview of exams, students, questions, and attempts

### Technical Features
- **Automatic Scoring**: Instant calculation of scores for objective questions
- **Time Management**: Countdown timer with automatic submission
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- **Data Analytics**: Accuracy, pass rate, and ranking calculations
- **Security**: Django's built-in authentication and CSRF protection
- **SQLite Database**: Lightweight database for easy deployment

## 🛠️ Tech Stack

- **Backend**: Django 4.2.9 (Python Web Framework)
- **Database**: SQLite3 (Built-in with Django)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Icons**: Bootstrap Icons
- **Forms**: Django Crispy Forms with Bootstrap 4

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Installation & Setup

### Step 1: Clone or Download the Project

Download or clone this project to your local machine.

### Step 2: Install Dependencies

Open PowerShell or Command Prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- Django 4.2.9
- Pillow (for image handling)
- django-crispy-forms
- crispy-bootstrap4

### Step 3: Run Automated Setup

**Option A: Using Setup Script (Recommended)**

Simply double-click `setup.bat` or run in terminal:

```bash
setup.bat
```

This will automatically:
1. Install all dependencies
2. Create database tables
3. Generate sample data (admin, students, exams)
4. Collect static files

**Option B: Manual Setup**

Run these commands one by one:

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Create sample data
python sample_data.py

# Collect static files
python manage.py collectstatic --noinput
```

### Step 4: Start the Development Server

**Option A: Using Run Script**

Double-click `run_server.bat` or run:

```bash
run_server.bat
```

**Option B: Manual Start**

```bash
python manage.py runserver
```

### Step 5: Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:8000
```

## 👤 Default Login Credentials

### Administrator Account
- **Username**: `admin`
- **Password**: `admin123`
- **Access**: Full system management capabilities

### Student Accounts
- **Username**: `student1`, `student2`, `student3`
- **Password**: `student123` (same for all)
- **Access**: Take exams and view results

## 📁 Project Structure

```
Online Examination Portal/
│
├── exam_portal/              # Main project configuration
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
│
├── accounts/                 # User authentication app
│   ├── models.py            # User profile models
│   ├── views.py             # Login, register, profile views
│   ├── forms.py             # Registration and profile forms
│   ├── urls.py              # Account URLs
│   └── admin.py             # Admin configuration
│
├── exams/                    # Exam management app
│   ├── models.py            # Exam, Question, Answer, Result models
│   ├── views.py             # All exam-related views
│   ├── forms.py             # Exam and question forms
│   ├── urls.py              # Exam URLs
│   └── admin.py             # Admin configuration
│
├── templates/                # HTML templates
│   ├── base.html            # Base template with navbar
│   ├── accounts/            # Authentication templates
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   └── exams/               # Exam templates
│       ├── home.html
│       ├── exam_list.html
│       ├── exam_detail.html
│       ├── take_exam.html
│       ├── result.html
│       ├── my_results.html
│       ├── manage_exams.html
│       ├── create_exam.html
│       ├── edit_exam.html
│       ├── manage_questions.html
│       ├── add_questions.html
│       ├── edit_question.html
│       ├── exam_reports.html
│       ├── exam_report_detail.html
│       └── student_rankings.html
│
├── static/                   # Static files (CSS, JS, images)
├── media/                    # User uploaded files
├── db.sqlite3               # SQLite database
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── sample_data.py           # Sample data generator
├── setup.bat                # Automated setup script
├── run_server.bat           # Server start script
└── README.md                # This file
```

## 💡 Usage Guide

### For Students

1. **Register**: Click "Register" and fill in your details
2. **Login**: Use your credentials to log in
3. **View Exams**: Browse available exams from the dashboard or exams page
4. **Take Exam**: 
   - Click on an exam to view details
   - Click "Start Exam" to begin
   - Answer questions (you can save progress)
   - Submit when finished or wait for auto-submit
5. **View Results**: Check your scores, accuracy, and rankings
6. **Update Profile**: Manage your personal information

### For Administrators

1. **Login**: Use admin credentials
2. **Create Exam**:
   - Go to "Manage Exams"
   - Click "Create New Exam"
   - Fill in exam details (title, duration, marks, schedule)
   - Add questions with options and correct answers
3. **Manage Questions**: Add, edit, or delete questions from existing exams
4. **View Reports**: 
   - Check overall exam statistics
   - View student performance
   - See rankings and pass rates
5. **Monitor Students**: Track all exam attempts and results

## 🗄️ Database Models

### User Profile (accounts.Profile)
- Extends Django's User model
- Role-based access (Student/Admin)
- Personal information and profile picture

### Exam (exams.Exam)
- Title, description, duration
- Total marks, passing marks
- Start and end dates
- Status (draft, active, completed, archived)

### Question (exams.Question)
- Multiple-choice questions (A, B, C, D)
- Correct answer and marks
- Difficulty level and explanation

### ExamAttempt (exams.ExamAttempt)
- Links student to exam
- Tracks start/end time
- Stores score and percentage

### Answer (exams.Answer)
- Student's selected answer
- Automatically checked for correctness

### Result (exams.Result)
- Detailed analytics
- Correct/wrong/unanswered counts
- Accuracy and ranking

## 🎨 Key Features Explained

### Automatic Scoring
The system automatically calculates scores by comparing student answers with correct answers stored in the database.

### Time Management
- Real-time countdown timer displayed during exam
- Automatic submission when time expires
- Prevents cheating by enforcing time limits

### Ranking System
Students are ranked based on:
1. Total score (primary)
2. Time taken (tiebreaker)

### Answer Explanations
Admins can add explanations for each question, helping students understand correct answers.

### Progress Saving
Students can save their answers and return to complete the exam later (before time expires).

## 🔒 Security Features

- Password hashing using Django's authentication system
- CSRF protection on all forms
- Login required decorators for protected views
- Role-based access control (Student/Admin)
- Session management

## 🎓 Learning Outcomes

By exploring this project, you will learn:

1. **Django Framework**:
   - Models, Views, Templates (MVT) architecture
   - URL routing and view functions
   - Forms and validation
   - Django ORM for database operations

2. **Web Development**:
   - Creating responsive web interfaces
   - Form handling and validation
   - Session management
   - User authentication and authorization

3. **Database Design**:
   - Relational database modeling
   - Foreign key relationships
   - Query optimization

4. **Frontend Development**:
   - Bootstrap responsive design
   - CSS styling and animations
   - JavaScript for interactive features

5. **Software Engineering**:
   - Project structure and organization
   - Separation of concerns
   - Reusable components
   - Documentation

## 🐛 Troubleshooting

### Issue: Port already in use
**Solution**: Stop any other Django servers or change the port:
```bash
python manage.py runserver 8001
```

### Issue: Module not found errors
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Database errors
**Solution**: Delete `db.sqlite3` and run migrations again:
```bash
del db.sqlite3
python manage.py migrate
python sample_data.py
```

### Issue: Static files not loading
**Solution**: Collect static files:
```bash
python manage.py collectstatic --noinput
```

## 🚀 Deployment (Production)

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS` with your domain
3. Use a production database (PostgreSQL/MySQL)
4. Set a strong `SECRET_KEY`
5. Use a production server (Gunicorn/uWSGI)
6. Set up static file serving (Nginx)
7. Enable HTTPS

## 📝 Customization

### Adding New Question Types
Modify the `Question` model in `exams/models.py` to support additional question types.

### Changing Theme
Edit CSS variables in `templates/base.html` under the `<style>` section.

### Email Notifications
Add Django's email backend configuration in settings to send result notifications.

### PDF Reports
Install ReportLab and create PDF generation views for certificates and reports.

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Python Documentation](https://docs.python.org/)

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements.

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Django documentation
3. Inspect browser console for JavaScript errors
4. Check Django debug output in terminal

## 🎉 Acknowledgments

Built with Django, Bootstrap, and Bootstrap Icons.

---

**Happy Coding! 🚀**
