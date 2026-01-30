from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Exam(models.Model):
    """Exam model - represents an examination"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    total_marks = models.PositiveIntegerField()
    passing_marks = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_exams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def is_active(self):
        """Check if exam is currently active"""
        now = timezone.now()
        return self.status == 'active' and self.start_date <= now <= self.end_date
    
    @property
    def has_started(self):
        """Check if exam has started"""
        return timezone.now() >= self.start_date
    
    @property
    def has_ended(self):
        """Check if exam has ended"""
        return timezone.now() > self.end_date
    
    @property
    def question_count(self):
        """Get total number of questions in this exam"""
        return self.questions.count()


class Question(models.Model):
    """Question model - stores multiple choice questions"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_answer = models.CharField(
        max_length=1,
        choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')]
    )
    marks = models.PositiveIntegerField(default=1)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    explanation = models.TextField(blank=True, help_text='Explanation for the correct answer')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.exam.title} - Q{self.id}"
    
    def get_correct_option_text(self):
        """Return the text of the correct answer"""
        options = {
            'A': self.option_a,
            'B': self.option_b,
            'C': self.option_c,
            'D': self.option_d
        }
        return options.get(self.correct_answer, '')


class ExamAttempt(models.Model):
    """ExamAttempt model - tracks student exam attempts"""
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('evaluated', 'Evaluated'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_attempts')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    class Meta:
        ordering = ['-start_time']
        unique_together = ['student', 'exam']
    
    def __str__(self):
        return f"{self.student.username} - {self.exam.title}"
    
    @property
    def time_taken(self):
        """Calculate time taken for the exam"""
        if self.end_time:
            delta = self.end_time - self.start_time
            return delta.total_seconds() / 60  # Return minutes
        return None
    
    @property
    def is_passed(self):
        """Check if student passed the exam"""
        if self.score is not None:
            return self.score >= self.exam.passing_marks
        return False
    
    @property
    def remaining_time(self):
        """Calculate remaining time in minutes"""
        if self.status == 'in_progress':
            elapsed = timezone.now() - self.start_time
            elapsed_minutes = elapsed.total_seconds() / 60
            remaining = self.exam.duration - elapsed_minutes
            return max(0, remaining)
        return 0
    
    def calculate_score(self):
        """Calculate the total score for this attempt"""
        correct_answers = self.answers.filter(is_correct=True)
        total_score = sum(answer.question.marks for answer in correct_answers)
        total_questions = self.answers.count()
        
        self.score = total_score
        if self.exam.total_marks > 0:
            self.percentage = (total_score / self.exam.total_marks) * 100
        self.status = 'evaluated'
        self.save()
        
        return self.score


class Answer(models.Model):
    """Answer model - stores student answers"""
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='student_answers')
    selected_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['attempt', 'question']
    
    def __str__(self):
        return f"{self.attempt.student.username} - {self.question.id} - {self.selected_answer}"
    
    def save(self, *args, **kwargs):
        """Override save to automatically check if answer is correct"""
        self.is_correct = (self.selected_answer == self.question.correct_answer)
        super().save(*args, **kwargs)


class Result(models.Model):
    """Result model - detailed results and analytics"""
    attempt = models.OneToOneField(ExamAttempt, on_delete=models.CASCADE, related_name='result')
    total_questions = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField()
    wrong_answers = models.PositiveIntegerField()
    unanswered = models.PositiveIntegerField()
    accuracy = models.DecimalField(max_digits=5, decimal_places=2)
    rank = models.PositiveIntegerField(null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-accuracy', '-attempt__score']
    
    def __str__(self):
        return f"Result: {self.attempt.student.username} - {self.attempt.exam.title}"
    
    @staticmethod
    def generate_result(attempt):
        """Generate detailed result for an exam attempt"""
        total_questions = attempt.exam.questions.count()
        answered_questions = attempt.answers.count()
        correct_answers = attempt.answers.filter(is_correct=True).count()
        wrong_answers = answered_questions - correct_answers
        unanswered = total_questions - answered_questions
        
        accuracy = 0
        if answered_questions > 0:
            accuracy = (correct_answers / answered_questions) * 100
        
        result, created = Result.objects.update_or_create(
            attempt=attempt,
            defaults={
                'total_questions': total_questions,
                'correct_answers': correct_answers,
                'wrong_answers': wrong_answers,
                'unanswered': unanswered,
                'accuracy': accuracy
            }
        )
        
        # Calculate rank
        Result.update_ranks(attempt.exam)
        
        return result
    
    @staticmethod
    def update_ranks(exam):
        """Update ranks for all attempts of an exam"""
        attempts = ExamAttempt.objects.filter(
            exam=exam,
            status='evaluated'
        ).order_by('-score', 'end_time')
        
        rank = 1
        for attempt in attempts:
            if hasattr(attempt, 'result'):
                attempt.result.rank = rank
                attempt.result.save()
                rank += 1
