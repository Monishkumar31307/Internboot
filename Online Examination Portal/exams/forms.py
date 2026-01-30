from django import forms
from django.forms import modelformset_factory
from .models import Exam, Question, ExamAttempt, Answer


class ExamForm(forms.ModelForm):
    """Form for creating and editing exams"""
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    class Meta:
        model = Exam
        fields = ['title', 'description', 'duration', 'total_marks', 'passing_marks', 
                  'status', 'start_date', 'end_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        passing_marks = cleaned_data.get('passing_marks')
        total_marks = cleaned_data.get('total_marks')
        
        if start_date and end_date:
            if end_date <= start_date:
                raise forms.ValidationError('End date must be after start date.')
        
        if passing_marks and total_marks:
            if passing_marks > total_marks:
                raise forms.ValidationError('Passing marks cannot exceed total marks.')
        
        return cleaned_data


class QuestionForm(forms.ModelForm):
    """Form for creating and editing questions"""
    class Meta:
        model = Question
        fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d',
                  'correct_answer', 'marks', 'difficulty', 'explanation']
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 3}),
            'explanation': forms.Textarea(attrs={'rows': 2}),
        }


# Formset for adding multiple questions at once
QuestionFormSet = modelformset_factory(
    Question,
    form=QuestionForm,
    extra=1,
    can_delete=True
)


class AnswerForm(forms.ModelForm):
    """Form for submitting answers"""
    class Meta:
        model = Answer
        fields = ['selected_answer']
        widgets = {
            'selected_answer': forms.RadioSelect(
                choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
            )
        }
