from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Post, Category
from .models import Comment
from .forms import CommentForm


class CommentModelTests(TestCase):
    """Test Comment model"""
    
    def setUp(self):
        self.author = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='testpass123'
        )
        self.reader = User.objects.create_user(
            username='reader',
            email='reader@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Technology')
        self.post = Post.objects.create(
            title='Test Post',
            author=self.author,
            category=self.category,
            content='<p>Test content</p>',
            status='published'
        )
    
    def test_comment_creation(self):
        """Test comment is created correctly"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.reader,
            content='Great post!',
            approved=True
        )
        self.assertEqual(comment.content, 'Great post!')
        self.assertTrue(comment.approved)
        self.assertEqual(comment.author, self.reader)
    
    def test_comment_ordering(self):
        """Test comments are ordered by creation time"""
        comment1 = Comment.objects.create(
            post=self.post,
            author=self.reader,
            content='First comment'
        )
        comment2 = Comment.objects.create(
            post=self.post,
            author=self.reader,
            content='Second comment'
        )
        comments = Comment.objects.all()
        self.assertEqual(comments[0].id, comment1.id)
        self.assertEqual(comments[1].id, comment2.id)


class CommentFormTests(TestCase):
    """Test comment form"""
    
    def test_comment_form_valid(self):
        """Test valid comment form"""
        form_data = {'content': 'Great post!'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_comment_form_invalid_empty(self):
        """Test form invalid with empty content"""
        form_data = {'content': ''}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())


class CommentViewTests(TestCase):
    """Test comment views"""
    
    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='testpass123'
        )
        self.reader = User.objects.create_user(
            username='reader',
            email='reader@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Technology')
        self.post = Post.objects.create(
            title='Test Post',
            author=self.author,
            category=self.category,
            content='<p>Test content</p>',
            status='published'
        )
    
    def test_add_comment_requires_login(self):
        """Test adding comment requires authentication"""
        response = self.client.post(
            reverse('comments:add_comment', args=[self.post.id]),
            {'content': 'Test comment'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)
    
    def test_add_comment_by_reader(self):
        """Test reader can add comment"""
        self.client.login(username='reader', password='testpass123')
        response = self.client.post(
            reverse('comments:add_comment', args=[self.post.id]),
            {'content': 'Great post!'}
        )
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.content, 'Great post!')
        self.assertEqual(comment.author, self.reader)
    
    def test_edit_comment_by_owner(self):
        """Test comment author can edit"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.reader,
            content='Original comment'
        )
        self.client.login(username='reader', password='testpass123')
        response = self.client.post(
            reverse('comments:edit_comment', args=[comment.id]),
            {'content': 'Edited comment'}
        )
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Edited comment')
