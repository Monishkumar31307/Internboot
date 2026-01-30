from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Avg, Q
from django.http import JsonResponse
from .models import Exam, Question, ExamAttempt, Answer, Result
from .forms import ExamForm, QuestionForm, AnswerForm
from accounts.models import Profile


def home(request):
    """Home page view"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {}
    
    if request.user.profile.is_student:
        # Student dashboard
        now = timezone.now()
        available_exams = Exam.objects.filter(
            status='active',
            start_date__lte=now,
            end_date__gte=now
        ).exclude(
            attempts__student=request.user
        )
        
        attempted_exams = ExamAttempt.objects.filter(
            student=request.user
        ).order_by('-start_time')[:5]
        
        context = {
            'available_exams': available_exams,
            'attempted_exams': attempted_exams,
        }
        
    elif request.user.profile.is_admin:
        # Admin dashboard
        total_exams = Exam.objects.count()
        total_students = Profile.objects.filter(role='student').count()
        total_questions = Question.objects.count()
        total_attempts = ExamAttempt.objects.filter(status='evaluated').count()
        
        recent_exams = Exam.objects.all()[:5]
        recent_attempts = ExamAttempt.objects.filter(status='evaluated').order_by('-end_time')[:5]
        
        context = {
            'total_exams': total_exams,
            'total_students': total_students,
            'total_questions': total_questions,
            'total_attempts': total_attempts,
            'recent_exams': recent_exams,
            'recent_attempts': recent_attempts,
        }
    
    return render(request, 'exams/home.html', context)


# ============= Student Views =============

@login_required
def exam_list(request):
    """List all available exams for students"""
    if not request.user.profile.is_student:
        messages.error(request, 'Access denied. Students only.')
        return redirect('home')
    
    now = timezone.now()
    available_exams = Exam.objects.filter(
        status='active',
        start_date__lte=now,
        end_date__gte=now
    ).exclude(
        attempts__student=request.user
    )
    
    upcoming_exams = Exam.objects.filter(
        status='active',
        start_date__gt=now
    )
    
    context = {
        'available_exams': available_exams,
        'upcoming_exams': upcoming_exams,
    }
    return render(request, 'exams/exam_list.html', context)


@login_required
def exam_detail(request, exam_id):
    """Exam detail view"""
    exam = get_object_or_404(Exam, id=exam_id)
    
    # Check if student already attempted
    has_attempted = ExamAttempt.objects.filter(
        student=request.user,
        exam=exam
    ).exists()
    
    context = {
        'exam': exam,
        'has_attempted': has_attempted,
    }
    return render(request, 'exams/exam_detail.html', context)


@login_required
def start_exam(request, exam_id):
    """Start an exam attempt"""
    if not request.user.profile.is_student:
        messages.error(request, 'Only students can take exams.')
        return redirect('home')
    
    exam = get_object_or_404(Exam, id=exam_id)
    
    # Check if exam is available
    if not exam.is_active:
        messages.error(request, 'This exam is not currently available.')
        return redirect('exam_detail', exam_id=exam.id)
    
    # Check if already attempted
    if ExamAttempt.objects.filter(student=request.user, exam=exam).exists():
        messages.error(request, 'You have already attempted this exam.')
        return redirect('exam_detail', exam_id=exam.id)
    
    # Create new attempt
    attempt = ExamAttempt.objects.create(
        student=request.user,
        exam=exam,
        status='in_progress'
    )
    
    messages.success(request, f'Exam started! You have {exam.duration} minutes to complete.')
    return redirect('take_exam', attempt_id=attempt.id)


@login_required
def take_exam(request, attempt_id):
    """Take exam view - display questions and handle submissions"""
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, student=request.user)
    
    # Check if attempt is still valid
    if attempt.status != 'in_progress':
        messages.error(request, 'This exam has already been submitted.')
        return redirect('view_result', attempt_id=attempt.id)
    
    # Check if time is up
    if attempt.remaining_time <= 0:
        attempt.status = 'submitted'
        attempt.end_time = timezone.now()
        attempt.save()
        attempt.calculate_score()
        Result.generate_result(attempt)
        messages.warning(request, 'Time is up! Your exam has been automatically submitted.')
        return redirect('view_result', attempt_id=attempt.id)
    
    questions = attempt.exam.questions.all()
    
    if request.method == 'POST':
        # Save answers
        for question in questions:
            answer_key = f'question_{question.id}'
            if answer_key in request.POST:
                selected_answer = request.POST[answer_key]
                Answer.objects.update_or_create(
                    attempt=attempt,
                    question=question,
                    defaults={'selected_answer': selected_answer}
                )
        
        if 'submit_exam' in request.POST:
            # Submit exam
            attempt.status = 'submitted'
            attempt.end_time = timezone.now()
            attempt.save()
            
            # Calculate score
            attempt.calculate_score()
            
            # Generate result
            Result.generate_result(attempt)
            
            messages.success(request, 'Exam submitted successfully!')
            return redirect('view_result', attempt_id=attempt.id)
        else:
            messages.success(request, 'Answers saved!')
            return redirect('take_exam', attempt_id=attempt.id)
    
    # Get already submitted answers
    submitted_answers = {
        answer.question.id: answer.selected_answer
        for answer in attempt.answers.all()
    }
    
    context = {
        'attempt': attempt,
        'exam': attempt.exam,
        'questions': questions,
        'submitted_answers': submitted_answers,
        'remaining_time': int(attempt.remaining_time),
    }
    return render(request, 'exams/take_exam.html', context)


@login_required
def view_result(request, attempt_id):
    """View exam result"""
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, student=request.user)
    
    if attempt.status == 'in_progress':
        messages.error(request, 'Please complete the exam first.')
        return redirect('take_exam', attempt_id=attempt.id)
    
    result = get_object_or_404(Result, attempt=attempt)
    
    # Get detailed answers
    answers = attempt.answers.select_related('question').all()
    
    context = {
        'attempt': attempt,
        'result': result,
        'answers': answers,
    }
    return render(request, 'exams/result.html', context)


@login_required
def my_results(request):
    """View all student results"""
    if not request.user.profile.is_student:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    attempts = ExamAttempt.objects.filter(
        student=request.user,
        status='evaluated'
    ).order_by('-end_time')
    
    context = {
        'attempts': attempts,
    }
    return render(request, 'exams/my_results.html', context)


# ============= Admin Views =============

@login_required
def manage_exams(request):
    """Manage exams - Admin only"""
    if not request.user.profile.is_admin:
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    exams = Exam.objects.all().order_by('-created_at')
    
    context = {
        'exams': exams,
    }
    return render(request, 'exams/manage_exams.html', context)


@login_required
def create_exam(request):
    """Create new exam - Admin only"""
    if not request.user.profile.is_admin:
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.created_by = request.user
            exam.save()
            messages.success(request, f'Exam "{exam.title}" created successfully!')
            return redirect('add_questions', exam_id=exam.id)
    else:
        form = ExamForm()
    
    context = {
        'form': form,
    }
    return render(request, 'exams/create_exam.html', context)


@login_required
def edit_exam(request, exam_id):
    """Edit exam - Admin only"""
    if not request.user.profile.is_admin:
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, f'Exam "{exam.title}" updated successfully!')
            return redirect('manage_exams')
    else:
        form = ExamForm(instance=exam)
    
    context = {
        'form': form,
        'exam': exam,
    }
    return render(request, 'exams/edit_exam.html', context)


@login_required
def delete_exam(request, exam_id):
    """Delete exam - Admin only"""
    if not request.user.profile.is_admin:
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == 'POST':
        exam_title = exam.title
        exam.delete()
        messages.success(request, f'Exam "{exam_title}" deleted successfully!')
        return redirect('manage_exams')
    
    context = {
        'exam': exam,
    }
    return render(request, 'exams/delete_exam.html', context)


@login_required
def add_questions(request, exam_id):
    """Add questions to exam - Admin only"""
    if not request.user.profile.is_admin:
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.exam = exam
            question.save()
            messages.success(request, 'Question added successfully!')
            
            if 'add_another' in request.POST:
                return redirect('add_questions', exam_id=exam.id)
            else:
                return redirect('manage_questions', exam_id=exam.id)
    else:
        form = QuestionForm()
    
    context = {
        'form': form,
        'exam': exam,
    }
    return render(request, 'exams/add_questions.html', context)


@login_required
def manage_questions(request, exam_id):
    """Manage exam questions - Admin only"""
    if not request.user.profile.is_admin:
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()
    
    context = {
        'exam': exam,
        'questions': questions,
    }
    return render(request, 'exams/manage_questions.html', context)


@login_required
def edit_question(request, question_id):
    """Edit question - Admin only"""
    if not request.user.profile.is_admin:
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question updated successfully!')
            return redirect('manage_questions', exam_id=question.exam.id)
    else:
        form = QuestionForm(instance=question)
    
    context = {
        'form': form,
        'question': question,
    }
    return render(request, 'exams/edit_question.html', context)


@login_required
def delete_question(request, question_id):
    """Delete question - Admin only"""
    if not request.user.profile.is_admin:
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    question = get_object_or_404(Question, id=question_id)
    exam_id = question.exam.id
    
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully!')
        return redirect('manage_questions', exam_id=exam_id)
    
    context = {
        'question': question,
    }
    return render(request, 'exams/delete_question.html', context)


@login_required
def exam_reports(request):
    """View exam reports - Admin only"""
    if not request.user.profile.is_admin:
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    exams = Exam.objects.annotate(
        attempts_count=Count('attempts'),
        avg_score=Avg('attempts__score')
    ).order_by('-created_at')
    
    context = {
        'exams': exams,
    }
    return render(request, 'exams/exam_reports.html', context)


@login_required
def exam_report_detail(request, exam_id):
    """Detailed report for specific exam - Admin only"""
    if not request.user.profile.is_admin:
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    exam = get_object_or_404(Exam, id=exam_id)
    attempts = ExamAttempt.objects.filter(
        exam=exam,
        status='evaluated'
    ).select_related('student', 'result').order_by('-score')
    
    # Calculate statistics
    total_attempts = attempts.count()
    if total_attempts > 0:
        avg_score = sum(a.score for a in attempts) / total_attempts
        passed_count = sum(1 for a in attempts if a.is_passed)
        pass_percentage = (passed_count / total_attempts) * 100
    else:
        avg_score = 0
        passed_count = 0
        pass_percentage = 0
    
    context = {
        'exam': exam,
        'attempts': attempts,
        'total_attempts': total_attempts,
        'avg_score': avg_score,
        'passed_count': passed_count,
        'pass_percentage': pass_percentage,
    }
    return render(request, 'exams/exam_report_detail.html', context)


@login_required
def student_rankings(request, exam_id):
    """View student rankings for an exam - Admin only"""
    if not request.user.profile.is_admin:
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    exam = get_object_or_404(Exam, id=exam_id)
    results = Result.objects.filter(
        attempt__exam=exam
    ).select_related('attempt__student').order_by('rank')
    
    context = {
        'exam': exam,
        'results': results,
    }
    return render(request, 'exams/student_rankings.html', context)
