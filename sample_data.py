"""
Sample data generation script for Online Examination Portal
This script creates sample exams, questions, and users for testing
"""

import os
import django
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_portal.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile
from exams.models import Exam, Question
from django.utils import timezone


def create_users():
    """Create sample admin and student users"""
    print("Creating users...")
    
    # Create admin user
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@exam.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        admin.profile.role = 'admin'
        admin.profile.save()
        print("✓ Admin user created (username: admin, password: admin123)")
    
    # Create student users
    students = [
        {'username': 'student1', 'email': 'student1@exam.com', 'first_name': 'John', 'last_name': 'Doe'},
        {'username': 'student2', 'email': 'student2@exam.com', 'first_name': 'Jane', 'last_name': 'Smith'},
        {'username': 'student3', 'email': 'student3@exam.com', 'first_name': 'Bob', 'last_name': 'Johnson'},
    ]
    
    for student_data in students:
        if not User.objects.filter(username=student_data['username']).exists():
            student = User.objects.create_user(
                username=student_data['username'],
                email=student_data['email'],
                password='student123',
                first_name=student_data['first_name'],
                last_name=student_data['last_name']
            )
            student.profile.role = 'student'
            student.profile.save()
            print(f"✓ Student user created: {student_data['username']} (password: student123)")


def create_sample_exams():
    """Create sample exams with questions"""
    print("\nCreating sample exams...")
    
    admin = User.objects.filter(profile__role='admin').first()
    if not admin:
        print("Error: No admin user found. Please run create_users() first.")
        return
    
    # Python Programming Exam
    if not Exam.objects.filter(title='Python Programming Basics').exists():
        python_exam = Exam.objects.create(
            title='Python Programming Basics',
            description='Test your knowledge of Python programming fundamentals including data types, control structures, and functions.',
            duration=30,
            total_marks=20,
            passing_marks=12,
            status='active',
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=30),
            created_by=admin
        )
        
        # Python Questions
        python_questions = [
            {
                'question_text': 'What is the output of: print(type([]))?',
                'option_a': '<class \'list\'>',
                'option_b': '<class \'tuple\'>',
                'option_c': '<class \'dict\'>',
                'option_d': '<class \'set\'>',
                'correct_answer': 'A',
                'marks': 2,
                'difficulty': 'easy',
                'explanation': 'The type() function returns the type of the object. [] is a list literal, so it returns <class \'list\'>.'
            },
            {
                'question_text': 'Which keyword is used to define a function in Python?',
                'option_a': 'function',
                'option_b': 'def',
                'option_c': 'func',
                'option_d': 'define',
                'correct_answer': 'B',
                'marks': 2,
                'difficulty': 'easy',
                'explanation': 'The \'def\' keyword is used to define a function in Python.'
            },
            {
                'question_text': 'What is the result of: 5 // 2?',
                'option_a': '2.5',
                'option_b': '2',
                'option_c': '3',
                'option_d': '2.0',
                'correct_answer': 'B',
                'marks': 2,
                'difficulty': 'easy',
                'explanation': 'The // operator performs floor division, which returns the integer part of the division result.'
            },
            {
                'question_text': 'Which of the following is a mutable data type?',
                'option_a': 'tuple',
                'option_b': 'string',
                'option_c': 'list',
                'option_d': 'integer',
                'correct_answer': 'C',
                'marks': 2,
                'difficulty': 'medium',
                'explanation': 'Lists are mutable, meaning their contents can be changed after creation. Tuples, strings, and integers are immutable.'
            },
            {
                'question_text': 'What does the len() function do?',
                'option_a': 'Returns the length of an object',
                'option_b': 'Returns the type of an object',
                'option_c': 'Converts to lowercase',
                'option_d': 'Returns the last element',
                'correct_answer': 'A',
                'marks': 2,
                'difficulty': 'easy',
                'explanation': 'The len() function returns the number of items in a container (string, list, tuple, etc.).'
            },
            {
                'question_text': 'Which loop is used when the number of iterations is unknown?',
                'option_a': 'for loop',
                'option_b': 'while loop',
                'option_c': 'do-while loop',
                'option_d': 'foreach loop',
                'correct_answer': 'B',
                'marks': 2,
                'difficulty': 'medium',
                'explanation': 'A while loop is used when the number of iterations is not predetermined and depends on a condition.'
            },
            {
                'question_text': 'What is the output of: print(\'Hello\'[1])?',
                'option_a': 'H',
                'option_b': 'e',
                'option_c': 'l',
                'option_d': 'o',
                'correct_answer': 'B',
                'marks': 2,
                'difficulty': 'easy',
                'explanation': 'String indexing starts at 0, so \'Hello\'[1] returns the second character, which is \'e\'.'
            },
            {
                'question_text': 'Which method is used to add an element to the end of a list?',
                'option_a': 'add()',
                'option_b': 'append()',
                'option_c': 'insert()',
                'option_d': 'extend()',
                'correct_answer': 'B',
                'marks': 2,
                'difficulty': 'easy',
                'explanation': 'The append() method adds a single element to the end of a list.'
            },
            {
                'question_text': 'What is a lambda function in Python?',
                'option_a': 'A function with no name',
                'option_b': 'A function that takes multiple arguments',
                'option_c': 'An anonymous function defined with lambda keyword',
                'option_d': 'A recursive function',
                'correct_answer': 'C',
                'marks': 2,
                'difficulty': 'medium',
                'explanation': 'A lambda function is a small anonymous function defined using the lambda keyword. It can take any number of arguments but can only have one expression.'
            },
            {
                'question_text': 'Which of the following is NOT a valid Python data type?',
                'option_a': 'list',
                'option_b': 'dictionary',
                'option_c': 'array',
                'option_d': 'tuple',
                'correct_answer': 'C',
                'marks': 2,
                'difficulty': 'medium',
                'explanation': 'Python doesn\'t have a built-in array type. Lists are used instead. Arrays are available through the array module or NumPy.'
            }
        ]
        
        for q_data in python_questions:
            Question.objects.create(exam=python_exam, **q_data)
        
        print(f"✓ Created exam: {python_exam.title} with {len(python_questions)} questions")
    
    # Web Development Exam
    if not Exam.objects.filter(title='Web Development Fundamentals').exists():
        web_exam = Exam.objects.create(
            title='Web Development Fundamentals',
            description='Test your understanding of HTML, CSS, JavaScript, and web development concepts.',
            duration=25,
            total_marks=15,
            passing_marks=9,
            status='active',
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=30),
            created_by=admin
        )
        
        # Web Development Questions
        web_questions = [
            {
                'question_text': 'What does HTML stand for?',
                'option_a': 'Hyper Text Markup Language',
                'option_b': 'High Tech Modern Language',
                'option_c': 'Hyperlinks and Text Markup Language',
                'option_d': 'Home Tool Markup Language',
                'correct_answer': 'A',
                'marks': 1,
                'difficulty': 'easy',
                'explanation': 'HTML stands for Hyper Text Markup Language, which is the standard markup language for web pages.'
            },
            {
                'question_text': 'Which HTML tag is used to define an internal style sheet?',
                'option_a': '<css>',
                'option_b': '<style>',
                'option_c': '<script>',
                'option_d': '<stylesheet>',
                'correct_answer': 'B',
                'marks': 1,
                'difficulty': 'easy',
                'explanation': 'The <style> tag is used to define style information (CSS) for an HTML document.'
            },
            {
                'question_text': 'What is the correct CSS syntax to change the text color to red?',
                'option_a': 'text-color: red;',
                'option_b': 'color: red;',
                'option_c': 'font-color: red;',
                'option_d': 'text: red;',
                'correct_answer': 'B',
                'marks': 1,
                'difficulty': 'easy',
                'explanation': 'The color property is used to set the text color in CSS.'
            },
            {
                'question_text': 'Which JavaScript method is used to write HTML output?',
                'option_a': 'document.write()',
                'option_b': 'document.output()',
                'option_c': 'console.log()',
                'option_d': 'window.print()',
                'correct_answer': 'A',
                'marks': 2,
                'difficulty': 'medium',
                'explanation': 'document.write() is used to write content directly to the HTML document.'
            },
            {
                'question_text': 'What does CSS stand for?',
                'option_a': 'Computer Style Sheets',
                'option_b': 'Cascading Style Sheets',
                'option_c': 'Creative Style Sheets',
                'option_d': 'Colorful Style Sheets',
                'correct_answer': 'B',
                'marks': 1,
                'difficulty': 'easy',
                'explanation': 'CSS stands for Cascading Style Sheets, used to style and layout web pages.'
            },
            {
                'question_text': 'Which HTML attribute specifies an alternate text for an image?',
                'option_a': 'title',
                'option_b': 'alt',
                'option_c': 'src',
                'option_d': 'longdesc',
                'correct_answer': 'B',
                'marks': 2,
                'difficulty': 'medium',
                'explanation': 'The alt attribute provides alternative text for an image if it cannot be displayed.'
            },
            {
                'question_text': 'What is the correct way to declare a JavaScript variable?',
                'option_a': 'variable x;',
                'option_b': 'var x;',
                'option_c': 'v x;',
                'option_d': 'declare x;',
                'correct_answer': 'B',
                'marks': 2,
                'difficulty': 'easy',
                'explanation': 'Variables in JavaScript can be declared using var, let, or const keywords.'
            },
            {
                'question_text': 'Which property is used to change the background color in CSS?',
                'option_a': 'color',
                'option_b': 'bgcolor',
                'option_c': 'background-color',
                'option_d': 'bg-color',
                'correct_answer': 'C',
                'marks': 2,
                'difficulty': 'easy',
                'explanation': 'The background-color property is used to set the background color of an element.'
            },
            {
                'question_text': 'What does DOM stand for?',
                'option_a': 'Document Object Model',
                'option_b': 'Data Object Model',
                'option_c': 'Document Oriented Model',
                'option_d': 'Display Object Management',
                'correct_answer': 'A',
                'marks': 2,
                'difficulty': 'medium',
                'explanation': 'DOM stands for Document Object Model, which represents the structure of an HTML document as a tree of objects.'
            },
            {
                'question_text': 'Which HTTP method is used to submit form data?',
                'option_a': 'GET',
                'option_b': 'POST',
                'option_c': 'PUT',
                'option_d': 'Both A and B',
                'correct_answer': 'D',
                'marks': 2,
                'difficulty': 'medium',
                'explanation': 'Both GET and POST methods can be used to submit form data, though POST is preferred for sensitive data.'
            }
        ]
        
        for q_data in web_questions:
            Question.objects.create(exam=web_exam, **q_data)
        
        print(f"✓ Created exam: {web_exam.title} with {len(web_questions)} questions")
    
    # Database Concepts Exam
    if not Exam.objects.filter(title='Database Management Basics').exists():
        db_exam = Exam.objects.create(
            title='Database Management Basics',
            description='Test your knowledge of database concepts, SQL queries, and relational database management.',
            duration=20,
            total_marks=10,
            passing_marks=6,
            status='active',
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=30),
            created_by=admin
        )
        
        # Database Questions
        db_questions = [
            {
                'question_text': 'What does SQL stand for?',
                'option_a': 'Structured Query Language',
                'option_b': 'Simple Question Language',
                'option_c': 'Strong Query Language',
                'option_d': 'Structured Question Language',
                'correct_answer': 'A',
                'marks': 1,
                'difficulty': 'easy',
                'explanation': 'SQL stands for Structured Query Language, used to manage and manipulate relational databases.'
            },
            {
                'question_text': 'Which SQL statement is used to retrieve data from a database?',
                'option_a': 'GET',
                'option_b': 'SELECT',
                'option_c': 'RETRIEVE',
                'option_d': 'FETCH',
                'correct_answer': 'B',
                'marks': 1,
                'difficulty': 'easy',
                'explanation': 'The SELECT statement is used to query and retrieve data from database tables.'
            },
            {
                'question_text': 'What is a primary key?',
                'option_a': 'A key that locks the database',
                'option_b': 'A unique identifier for each record',
                'option_c': 'The first column in a table',
                'option_d': 'A key that cannot be changed',
                'correct_answer': 'B',
                'marks': 1,
                'difficulty': 'medium',
                'explanation': 'A primary key is a column or set of columns that uniquely identifies each row in a table.'
            },
            {
                'question_text': 'Which SQL clause is used to filter records?',
                'option_a': 'FILTER',
                'option_b': 'WHERE',
                'option_c': 'HAVING',
                'option_d': 'SELECT',
                'correct_answer': 'B',
                'marks': 1,
                'difficulty': 'easy',
                'explanation': 'The WHERE clause is used to filter records based on specified conditions.'
            },
            {
                'question_text': 'What type of relationship exists between two tables when one record in table A can relate to many records in table B?',
                'option_a': 'One-to-One',
                'option_b': 'Many-to-Many',
                'option_c': 'One-to-Many',
                'option_d': 'Many-to-One',
                'correct_answer': 'C',
                'marks': 2,
                'difficulty': 'medium',
                'explanation': 'A One-to-Many relationship means one record in the first table can be associated with multiple records in the second table.'
            },
            {
                'question_text': 'Which SQL command is used to add new data to a table?',
                'option_a': 'ADD',
                'option_b': 'INSERT',
                'option_c': 'CREATE',
                'option_d': 'UPDATE',
                'correct_answer': 'B',
                'marks': 1,
                'difficulty': 'easy',
                'explanation': 'The INSERT statement is used to add new rows of data to a table.'
            },
            {
                'question_text': 'What does DBMS stand for?',
                'option_a': 'Database Management System',
                'option_b': 'Data Backup Management System',
                'option_c': 'Database Manipulation Software',
                'option_d': 'Data Business Management System',
                'correct_answer': 'A',
                'marks': 1,
                'difficulty': 'easy',
                'explanation': 'DBMS stands for Database Management System, software that manages databases.'
            },
            {
                'question_text': 'Which SQL keyword is used to sort the result?',
                'option_a': 'SORT BY',
                'option_b': 'ORDER BY',
                'option_c': 'ARRANGE BY',
                'option_d': 'GROUP BY',
                'correct_answer': 'B',
                'marks': 1,
                'difficulty': 'easy',
                'explanation': 'The ORDER BY clause is used to sort the query results in ascending or descending order.'
            },
            {
                'question_text': 'What is normalization in databases?',
                'option_a': 'Making database faster',
                'option_b': 'Organizing data to reduce redundancy',
                'option_c': 'Creating backups',
                'option_d': 'Encrypting database',
                'correct_answer': 'B',
                'marks': 1,
                'difficulty': 'medium',
                'explanation': 'Normalization is the process of organizing data in a database to reduce redundancy and improve data integrity.'
            }
        ]
        
        for q_data in db_questions:
            Question.objects.create(exam=db_exam, **q_data)
        
        print(f"✓ Created exam: {db_exam.title} with {len(db_questions)} questions")


def main():
    """Main function to run all setup tasks"""
    print("=" * 60)
    print("ONLINE EXAMINATION PORTAL - SAMPLE DATA GENERATOR")
    print("=" * 60)
    
    create_users()
    create_sample_exams()
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    print("\nLogin Credentials:")
    print("-" * 60)
    print("Admin:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nStudents:")
    print("  Username: student1, student2, student3")
    print("  Password: student123 (same for all students)")
    print("\nYou can now start the development server and log in!")
    print("=" * 60)


if __name__ == '__main__':
    main()
