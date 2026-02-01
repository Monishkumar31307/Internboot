from django import forms
from .models import Post, Category, Tag
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Post
        fields = ['title', 'category', 'excerpt', 'content', 'featured_image', 'tags', 'meta_description', 'meta_keywords']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post Title'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief summary'}),
            'content': CKEditorUploadingWidget(),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'meta_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'For SEO'}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma separated'}),
        }
