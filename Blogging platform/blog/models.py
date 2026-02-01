from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

class Category(models.Model):
    """Blog post categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'slug': self.slug})
    
    @property
    def post_count(self):
        return self.posts.filter(status='published').count()

class Tag(models.Model):
    """Blog post tags"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:tag_posts', kwargs={'slug': self.slug})
    
    @property
    def post_count(self):
        return self.posts.filter(status='published').count()

class Post(models.Model):
    """Blog post model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    
    content = RichTextUploadingField()
    excerpt = models.TextField(max_length=300, blank=True, help_text='Brief summary of the post')
    featured_image = models.ImageField(upload_to='posts/', blank=True, null=True)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        if not self.excerpt and self.content:
            text = self.content[:300]
            self.excerpt = text.replace('<p>', '').replace('</p>', '')[:300] + '...'
        
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    @property
    def is_published(self):
        return self.status == 'published'
    
    @property
    def comment_count(self):
        return self.comments.filter(approved=True).count()
    
    @property
    def like_count(self):
        return self.likes.count()
    
    def increment_views(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])
