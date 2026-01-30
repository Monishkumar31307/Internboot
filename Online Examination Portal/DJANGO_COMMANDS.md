# Django Management Commands - Online Examination Portal

## Essential Commands

### Setup & Migration Commands

**Make migrations** (Create migration files from model changes):
```bash
python manage.py makemigrations
```

**Apply migrations** (Apply migrations to database):
```bash
python manage.py migrate
```

**Show migrations** (List all migrations and their status):
```bash
python manage.py showmigrations
```

### User Management

**Create superuser** (Create admin account):
```bash
python manage.py createsuperuser
```

**Change password** (Change user password):
```bash
python manage.py changepassword <username>
```

### Server Commands

**Run development server** (Default port 8000):
```bash
python manage.py runserver
```

**Run on different port**:
```bash
python manage.py runserver 8001
```

**Run on all interfaces** (Accessible from other devices on network):
```bash
python manage.py runserver 0.0.0.0:8000
```

### Static Files

**Collect static files** (Gather all static files into STATIC_ROOT):
```bash
python manage.py collectstatic
```

**Collect static files without prompts**:
```bash
python manage.py collectstatic --noinput
```

### Database Management

**Database shell** (Access SQLite shell):
```bash
python manage.py dbshell
```

**Python shell** (Django-aware Python shell):
```bash
python manage.py shell
```

### Inspection & Debugging

**Check for problems** (Verify project setup):
```bash
python manage.py check
```

**Show URLs** (List all URL patterns):
```bash
python manage.py show_urls
```

**Show current settings**:
```bash
python manage.py diffsettings
```

### Testing

**Run tests**:
```bash
python manage.py test
```

**Run tests for specific app**:
```bash
python manage.py test exams
python manage.py test accounts
```

### Data Management

**Load sample data** (Using our custom script):
```bash
python sample_data.py
```

**Create database dump** (Export data):
```bash
python manage.py dumpdata > db_backup.json
```

**Load database dump** (Import data):
```bash
python manage.py loaddata db_backup.json
```

**Flush database** (Delete all data):
```bash
python manage.py flush
```

### App Management

**Create new app**:
```bash
python manage.py startapp <app_name>
```

### Useful Custom Commands

**Create sample exams and users**:
```bash
python sample_data.py
```

## Quick Setup Workflow

### First Time Setup:
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create database
python manage.py migrate

# 3. Create admin user
python manage.py createsuperuser

# 4. Load sample data
python sample_data.py

# 5. Start server
python manage.py runserver
```

### Reset Everything:
```bash
# Delete database
del db.sqlite3  # Windows
rm db.sqlite3   # Linux/Mac

# Recreate database
python manage.py migrate

# Load sample data
python sample_data.py
```

## Python Shell Examples

Access Django shell:
```bash
python manage.py shell
```

Then in the shell:

**Query all exams**:
```python
from exams.models import Exam
exams = Exam.objects.all()
for exam in exams:
    print(exam.title)
```

**Get specific user**:
```python
from django.contrib.auth.models import User
user = User.objects.get(username='admin')
print(user.profile.role)
```

**Create a new exam**:
```python
from exams.models import Exam
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

admin = User.objects.get(username='admin')
exam = Exam.objects.create(
    title='New Test Exam',
    description='This is a test exam',
    duration=30,
    total_marks=10,
    passing_marks=5,
    status='active',
    start_date=timezone.now(),
    end_date=timezone.now() + timedelta(days=7),
    created_by=admin
)
```

**Check exam attempts**:
```python
from exams.models import ExamAttempt
attempts = ExamAttempt.objects.filter(status='evaluated')
for attempt in attempts:
    print(f"{attempt.student.username}: {attempt.score}")
```

**Calculate statistics**:
```python
from exams.models import ExamAttempt, Exam
from django.db.models import Avg, Count

exam = Exam.objects.first()
stats = ExamAttempt.objects.filter(exam=exam, status='evaluated').aggregate(
    avg_score=Avg('score'),
    total_attempts=Count('id')
)
print(stats)
```

## Database Queries

**Count students**:
```python
from accounts.models import Profile
student_count = Profile.objects.filter(role='student').count()
```

**Get top performers**:
```python
from exams.models import Result
top_results = Result.objects.order_by('rank')[:10]
```

**Filter active exams**:
```python
from exams.models import Exam
from django.utils import timezone

active_exams = Exam.objects.filter(
    status='active',
    start_date__lte=timezone.now(),
    end_date__gte=timezone.now()
)
```

## Troubleshooting Commands

**Reset migrations** (Use with caution):
```bash
# Delete all migrations except __init__.py
# Then run:
python manage.py makemigrations
python manage.py migrate
```

**Clear cache** (if using caching):
```bash
python manage.py clear_cache
```

**Check for common issues**:
```bash
python manage.py check --deploy
```

## Production Commands

**Collect static files for production**:
```bash
python manage.py collectstatic --noinput
```

**Create deployment checklist**:
```bash
python manage.py check --deploy
```

## Backup Strategies

**Backup entire database**:
```bash
python manage.py dumpdata --indent 2 > full_backup.json
```

**Backup specific app**:
```bash
python manage.py dumpdata exams --indent 2 > exams_backup.json
```

**Backup excluding specific tables**:
```bash
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > backup.json
```

## Environment Variables

For production, set these environment variables:
```bash
# Windows
set DJANGO_SECRET_KEY=your-secret-key
set DJANGO_DEBUG=False
set DJANGO_ALLOWED_HOSTS=yourdomain.com

# Linux/Mac
export DJANGO_SECRET_KEY=your-secret-key
export DJANGO_DEBUG=False
export DJANGO_ALLOWED_HOSTS=yourdomain.com
```

## Quick Reference

| Command | Description |
|---------|-------------|
| `makemigrations` | Create migration files |
| `migrate` | Apply migrations |
| `runserver` | Start development server |
| `createsuperuser` | Create admin account |
| `collectstatic` | Collect static files |
| `shell` | Django Python shell |
| `test` | Run tests |
| `check` | Check for issues |

---

**Pro Tip**: Always backup your database before running migrations or major changes!
