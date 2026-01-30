from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Student URLs
    path('exams/', views.exam_list, name='exam_list'),
    path('exam/<int:exam_id>/', views.exam_detail, name='exam_detail'),
    path('exam/<int:exam_id>/start/', views.start_exam, name='start_exam'),
    path('attempt/<int:attempt_id>/take/', views.take_exam, name='take_exam'),
    path('attempt/<int:attempt_id>/result/', views.view_result, name='view_result'),
    path('my-results/', views.my_results, name='my_results'),
    
    # Admin URLs - Exam Management
    path('admin/exams/', views.manage_exams, name='manage_exams'),
    path('admin/exam/create/', views.create_exam, name='create_exam'),
    path('admin/exam/<int:exam_id>/edit/', views.edit_exam, name='edit_exam'),
    path('admin/exam/<int:exam_id>/delete/', views.delete_exam, name='delete_exam'),
    
    # Admin URLs - Question Management
    path('admin/exam/<int:exam_id>/questions/', views.manage_questions, name='manage_questions'),
    path('admin/exam/<int:exam_id>/add-questions/', views.add_questions, name='add_questions'),
    path('admin/question/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('admin/question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    
    # Admin URLs - Reports
    path('admin/reports/', views.exam_reports, name='exam_reports'),
    path('admin/report/<int:exam_id>/', views.exam_report_detail, name='exam_report_detail'),
    path('admin/rankings/<int:exam_id>/', views.student_rankings, name='student_rankings'),
]
