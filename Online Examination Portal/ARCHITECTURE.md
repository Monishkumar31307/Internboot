# System Architecture - Online Examination Portal

## 📐 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    WEB BROWSER (Client)                         │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Student    │  │    Admin     │  │  Public      │        │
│  │  Interface   │  │  Interface   │  │  Pages       │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                            ↕ HTTP Request/Response
┌─────────────────────────────────────────────────────────────────┐
│                    DJANGO WEB SERVER                            │
│                                                                 │
│  ┌────────────────────────────────────────────────────────────┐│
│  │                      URL Router                            ││
│  │  (exam_portal/urls.py, accounts/urls.py, exams/urls.py)   ││
│  └────────────────────────────────────────────────────────────┘│
│                            ↕                                    │
│  ┌────────────────────────────────────────────────────────────┐│
│  │                        VIEWS LAYER                         ││
│  │                                                            ││
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   ││
│  │  │   accounts/  │  │    exams/    │  │    Admin     │   ││
│  │  │   views.py   │  │   views.py   │  │   Panel      │   ││
│  │  │              │  │              │  │              │   ││
│  │  │ • register   │  │ • exam_list  │  │ • manage     │   ││
│  │  │ • login      │  │ • take_exam  │  │ • reports    │   ││
│  │  │ • profile    │  │ • results    │  │ • stats      │   ││
│  │  └──────────────┘  └──────────────┘  └──────────────┘   ││
│  └────────────────────────────────────────────────────────────┘│
│                            ↕                                    │
│  ┌────────────────────────────────────────────────────────────┐│
│  │                      FORMS LAYER                           ││
│  │                                                            ││
│  │  • ExamForm     • QuestionForm    • RegistrationForm      ││
│  │  • Validation   • Cleaning        • Error Handling        ││
│  └────────────────────────────────────────────────────────────┘│
│                            ↕                                    │
│  ┌────────────────────────────────────────────────────────────┐│
│  │                      MODELS LAYER                          ││
│  │                    (Django ORM)                            ││
│  │                                                            ││
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ ││
│  │  │ Profile  │  │   Exam   │  │ Question │  │  Answer  │ ││
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘ ││
│  │  ┌──────────┐  ┌──────────┐                              ││
│  │  │ExamAttmpt│  │  Result  │                              ││
│  │  └──────────┘  └──────────┘                              ││
│  └────────────────────────────────────────────────────────────┘│
│                            ↕                                    │
│  ┌────────────────────────────────────────────────────────────┐│
│  │                   TEMPLATE ENGINE                          ││
│  │                                                            ││
│  │  • base.html              • Inheritance                    ││
│  │  • Template tags          • Filters                        ││
│  │  • Context rendering      • Bootstrap integration         ││
│  └────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                            ↕ SQL Queries
┌─────────────────────────────────────────────────────────────────┐
│                    SQLite DATABASE                              │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Users   │  │  Exams   │  │Questions │  │ Attempts │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
│  ┌──────────┐  ┌──────────┐                                   │
│  │ Answers  │  │ Results  │                                   │
│  └──────────┘  └──────────┘                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Request Flow

### Student Taking Exam Flow

```
1. Student clicks "Start Exam"
   └─→ Browser sends GET request to /exam/5/start/

2. Django URL Router
   └─→ Matches pattern and routes to start_exam(request, exam_id=5)

3. View Function (start_exam)
   ├─→ Checks user authentication
   ├─→ Validates exam availability
   ├─→ Creates ExamAttempt record
   └─→ Redirects to take_exam view

4. Take Exam View
   ├─→ Retrieves exam questions from database
   ├─→ Retrieves any saved answers
   ├─→ Calculates remaining time
   └─→ Renders take_exam.html template

5. Template Engine
   ├─→ Loads base.html (navbar, styling)
   ├─→ Injects exam questions
   ├─→ Renders form with radio buttons
   ├─→ Adds JavaScript timer
   └─→ Sends HTML to browser

6. Student Sees Exam Page
   ├─→ Questions displayed
   ├─→ Timer counting down
   └─→ Can select answers

7. Student Submits Exam
   └─→ Browser sends POST request with answers

8. View Processes Submission
   ├─→ Saves all answers to database
   ├─→ Calculates score (compare with correct answers)
   ├─→ Updates ExamAttempt status
   ├─→ Generates Result record
   ├─→ Calculates ranking
   └─→ Redirects to result page

9. Result Page Displayed
   └─→ Shows score, percentage, accuracy, rank
```

---

## 🏗️ Application Structure

```
Online Examination Portal/
│
├─ exam_portal/                    # Main Configuration
│  ├─ settings.py                  # Database, Apps, Middleware
│  ├─ urls.py                      # Root URL routing
│  └─ wsgi.py                      # WSGI server config
│
├─ accounts/                       # Authentication App
│  ├─ models.py                    # Profile model
│  ├─ views.py                     # Login, register, profile
│  ├─ forms.py                     # User forms
│  ├─ urls.py                      # /accounts/* routes
│  └─ admin.py                     # Admin config
│
├─ exams/                          # Exam Management App
│  ├─ models.py                    # 5 models (Exam, Question, etc.)
│  ├─ views.py                     # 20+ view functions
│  ├─ forms.py                     # Exam/Question forms
│  ├─ urls.py                      # Exam routes
│  └─ admin.py                     # Admin interface
│
├─ templates/                      # HTML Templates
│  ├─ base.html                    # Base layout
│  ├─ accounts/                    # Auth templates
│  └─ exams/                       # Exam templates
│
├─ static/                         # Static Files (future)
│  ├─ css/
│  ├─ js/
│  └─ images/
│
├─ media/                          # User Uploads
│  └─ profiles/                    # Profile pictures
│
└─ db.sqlite3                      # Database file
```

---

## 💾 Database Schema

```
┌─────────────────┐
│   auth_user     │ (Django built-in)
├─────────────────┤
│ id (PK)         │
│ username        │
│ password        │
│ email           │
│ first_name      │
│ last_name       │
└─────────────────┘
         │ 1
         │ has
         │ 1
         ▼
┌─────────────────┐
│ accounts_profile│
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │───────┐
│ role            │        │
│ phone           │        │
│ date_of_birth   │        │
│ profile_picture │        │
└─────────────────┘        │
                           │
         ┌─────────────────┘
         │
         ▼
┌─────────────────┐
│   exams_exam    │
├─────────────────┤
│ id (PK)         │
│ title           │
│ description     │
│ duration        │
│ total_marks     │
│ passing_marks   │
│ status          │
│ start_date      │
│ end_date        │
│ created_by (FK) │───┐
└─────────────────┘   │
         │ 1          │
         │ has        │
         │ many       │
         ▼            │
┌─────────────────┐   │
│ exams_question  │   │
├─────────────────┤   │
│ id (PK)         │   │
│ exam_id (FK)    │───┘
│ question_text   │
│ option_a        │
│ option_b        │
│ option_c        │
│ option_d        │
│ correct_answer  │
│ marks           │
│ difficulty      │
│ explanation     │
└─────────────────┘
         │ 1
         │ answered in
         │ many
         ▼
┌─────────────────┐
│ exams_answer    │
├─────────────────┤
│ id (PK)         │
│ attempt_id (FK) │───┐
│ question_id(FK) │───┘
│ selected_answer │
│ is_correct      │
└─────────────────┘
         │
         │ belongs to
         │
         ▼
┌─────────────────┐
│exams_examattempt│
├─────────────────┤
│ id (PK)         │
│ student_id (FK) │
│ exam_id (FK)    │
│ start_time      │
│ end_time        │
│ status          │
│ score           │
│ percentage      │
└─────────────────┘
         │ 1
         │ has
         │ 1
         ▼
┌─────────────────┐
│  exams_result   │
├─────────────────┤
│ id (PK)         │
│ attempt_id (FK) │
│ total_questions │
│ correct_answers │
│ wrong_answers   │
│ unanswered      │
│ accuracy        │
│ rank            │
└─────────────────┘
```

---

## 🔐 Security Architecture

```
┌─────────────────────────────────────────┐
│         Security Layers                 │
├─────────────────────────────────────────┤
│                                         │
│  1. Authentication                      │
│     • Django built-in auth system       │
│     • Password hashing (PBKDF2)         │
│     • Session management               │
│                                         │
│  2. Authorization                       │
│     • @login_required decorators       │
│     • Role-based access (Profile.role) │
│     • View-level permission checks     │
│                                         │
│  3. CSRF Protection                     │
│     • {% csrf_token %} in all forms    │
│     • CSRF middleware enabled          │
│                                         │
│  4. Input Validation                    │
│     • Django forms validation          │
│     • Model field validators           │
│     • Clean methods                    │
│                                         │
│  5. SQL Injection Prevention            │
│     • Django ORM (parameterized)       │
│     • No raw SQL queries               │
│                                         │
│  6. XSS Prevention                      │
│     • Template auto-escaping           │
│     • |safe filter used carefully      │
│                                         │
└─────────────────────────────────────────┘
```

---

## 📊 Data Flow Diagrams

### Creating an Exam (Admin)

```
Admin → Login → Dashboard → Manage Exams
                                │
                                ▼
                         Create New Exam
                                │
                                ▼
                    Fill Exam Details Form
                    (title, duration, marks)
                                │
                                ▼
                         Submit Form
                                │
                                ▼
                    Django Validates Data
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
                 Valid?                  Invalid
                    ├─YES                   │
                    │                       ▼
                    │                Show Errors
                    │                       │
                    ▼                       └─→ Back to Form
            Save to Database
                    │
                    ▼
            Redirect to Add Questions
                    │
                    ▼
            Add Question Form
                    │
                    ▼
            (question, options, answer)
                    │
                    ▼
            Save Question
                    │
                    ├─→ Add Another
                    │
                    └─→ Finish
                         │
                         ▼
                 Questions List Page
```

### Student Taking Exam

```
Student → Login → Dashboard → Browse Exams
                                    │
                                    ▼
                            View Exam Details
                                    │
                                    ▼
                              Click Start
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
            Check Eligibility                Already Attempted?
                    │                               │
                YES │                          YES  │
                    ▼                               ▼
            Create ExamAttempt              Show "Already Attempted"
                    │
                    ▼
            Load Exam Questions
                    │
                    ▼
            Display with Timer
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
    Answer Q1   Answer Q2   Answer Q3
        │           │           │
        └───────────┴───────────┘
                    │
            ┌───────┴───────┐
            ▼               ▼
       Save Progress    Submit Exam
            │               │
            └───────┬───────┘
                    ▼
        Calculate Score Automatically
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
    Compare with          Count Correct
    Correct Answers       vs Wrong
        │                       │
        └───────┬───────────────┘
                ▼
        Store Result in Database
                │
                ▼
        Calculate Ranking
                │
                ▼
        Show Result Page
        (score, percentage, rank)
```

---

## 🎯 Component Interaction

```
┌───────────────────────────────────────────────┐
│           User Interface (Browser)            │
│                                               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐      │
│  │  HTML   │  │   CSS   │  │   JS    │      │
│  │ Content │◄─┤Bootstrap├─►│ Timer   │      │
│  └─────────┘  └─────────┘  └─────────┘      │
└───────────────────────────────────────────────┘
           ▲                      │
           │ HTML Response        │ HTTP Request
           │                      ▼
┌───────────────────────────────────────────────┐
│              Django Server                    │
│                                               │
│  ┌─────────────────────────────────────────┐ │
│  │          URL Dispatcher                 │ │
│  │  Matches URL → Calls View              │ │
│  └─────────────────────────────────────────┘ │
│           │                                   │
│           ▼                                   │
│  ┌─────────────────────────────────────────┐ │
│  │           View Function                 │ │
│  │  • Process request                      │ │
│  │  • Call models for data                 │ │
│  │  • Prepare context                      │ │
│  │  • Render template                      │ │
│  └─────────────────────────────────────────┘ │
│           │                ▲                  │
│           ▼                │                  │
│  ┌──────────────┐  ┌──────────────┐         │
│  │   Models     │  │  Templates   │         │
│  │  (Database)  │  │   (HTML)     │         │
│  └──────────────┘  └──────────────┘         │
└───────────────────────────────────────────────┘
           │
           ▼
┌───────────────────────────────────────────────┐
│           SQLite Database                     │
│  • Stores all data                            │
│  • Returns query results                      │
└───────────────────────────────────────────────┘
```

---

## 🔄 Authentication Flow

```
User Visits Site
    │
    ▼
Is Authenticated?
    │
    ├─YES─→ Check Role
    │          │
    │          ├─Student─→ Student Dashboard
    │          │
    │          └─Admin───→ Admin Dashboard
    │
    └─NO──→ Redirect to Login
               │
               ▼
           Enter Credentials
               │
               ▼
           Submit Form
               │
               ▼
           Django Authenticates
               │
      ┌────────┴────────┐
      ▼                 ▼
   Valid?            Invalid
      │                 │
     YES                NO
      │                 │
      ▼                 ▼
  Create Session    Show Error
      │                 │
      ▼                 └─→ Try Again
  Set Cookie
      │
      ▼
  Redirect to Dashboard
      │
      ▼
  (User now has session cookie)
      │
      ▼
  All subsequent requests
  include session cookie
      │
      ▼
  Django checks session
  to verify authentication
```

---

## 💡 Key Design Patterns

### 1. Model-View-Template (MVT)
```
Model (models.py)
  └─ Defines data structure
     └─ Business logic

View (views.py)
  └─ Handles requests
     └─ Calls models
        └─ Returns response

Template (*.html)
  └─ Presents data
     └─ User interface
```

### 2. DRY (Don't Repeat Yourself)
```
base.html (Common layout)
  └─ Extended by all templates
     └─ Navbar, footer once
        └─ Reused everywhere
```

### 3. Separation of Concerns
```
accounts/ ─→ User management only
exams/    ─→ Exam functionality only
settings  ─→ Configuration only
```

### 4. REST-like URLs
```
/exams/                  → List all exams
/exam/5/                 → Detail of exam 5
/exam/5/start/           → Start exam 5
/attempt/10/take/        → Take attempt 10
/attempt/10/result/      → Result of attempt 10
```

---

## 📈 Scalability Considerations

### Current Design (SQLite)
```
Single Server
│
├─ Django Application
├─ SQLite Database (file)
└─ Static Files

Suitable for:
• Development
• Testing
• Small deployments (<1000 users)
```

### Production Design
```
Load Balancer
│
├─ Django Server 1 ───┐
├─ Django Server 2 ───┼─→ PostgreSQL Database
└─ Django Server N ───┘
                      
                      → Redis (Cache)
                      → Nginx (Static Files)
                      → CDN (Media Files)

Suitable for:
• Production
• High traffic
• Thousands of concurrent users
```

---

This architecture provides a clear, maintainable, and scalable foundation for the Online Examination Portal!
