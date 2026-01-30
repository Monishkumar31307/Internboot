from django.contrib import admin
from .models import Exam, Question, ExamAttempt, Answer, Result


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'marks', 'difficulty']


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration', 'total_marks', 'status', 'start_date', 'end_date']
    list_filter = ['status', 'start_date', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [QuestionInline]
    fieldsets = (
        ('Exam Details', {
            'fields': ('title', 'description', 'duration', 'total_marks', 'passing_marks', 'status')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'exam', 'question_text_short', 'correct_answer', 'marks', 'difficulty']
    list_filter = ['exam', 'difficulty', 'correct_answer']
    search_fields = ['question_text', 'exam__title']
    fieldsets = (
        ('Question Details', {
            'fields': ('exam', 'question_text', 'difficulty', 'marks')
        }),
        ('Options', {
            'fields': ('option_a', 'option_b', 'option_c', 'option_d')
        }),
        ('Answer', {
            'fields': ('correct_answer',)
        }),
    )
    
    def question_text_short(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question'


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'exam', 'status', 'score', 'percentage', 'start_time']
    list_filter = ['status', 'exam', 'start_time']
    search_fields = ['student__username', 'exam__title']
    readonly_fields = ['start_time', 'end_time', 'score', 'percentage']
    fieldsets = (
        ('Attempt Information', {
            'fields': ('student', 'exam', 'status')
        }),
        ('Times', {
            'fields': ('start_time', 'end_time')
        }),
        ('Scoring', {
            'fields': ('score', 'percentage')
        }),
    )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'attempt', 'question', 'selected_answer', 'is_correct', 'answered_at']
    list_filter = ['is_correct', 'answered_at', 'attempt__exam']
    search_fields = ['attempt__student__username', 'question__question_text']
    readonly_fields = ['is_correct', 'answered_at']
    fieldsets = (
        ('Answer Details', {
            'fields': ('attempt', 'question', 'selected_answer')
        }),
        ('Result', {
            'fields': ('is_correct', 'answered_at')
        }),
    )


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'attempt', 'total_questions', 'correct_answers', 'accuracy', 'rank']
    list_filter = ['generated_at', 'attempt__exam']
    search_fields = ['attempt__student__username', 'attempt__exam__title']
    readonly_fields = ['generated_at', 'total_questions', 'correct_answers', 'wrong_answers', 'accuracy', 'rank']
    fieldsets = (
        ('Attempt Reference', {
            'fields': ('attempt',)
        }),
        ('Statistics', {
            'fields': ('total_questions', 'correct_answers', 'wrong_answers', 'accuracy', 'rank')
        }),
        ('Generated', {
            'fields': ('generated_at',)
        }),
    )
