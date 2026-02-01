from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Post, Category
from .models import Like
import json


class LikeModelTests(TestCase):
    """Test Like model"""
    
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
    
    def test_like_creation(self):
        """Test like is created correctly"""
        like = Like.objects.create(post=self.post, user=self.reader)
        self.assertEqual(like.post, self.post)
        self.assertEqual(like.user, self.reader)
    
    def test_like_unique_constraint(self):
        """Test only one like per user per post"""
        Like.objects.create(post=self.post, user=self.reader)
        with self.assertRaises(Exception):
            Like.objects.create(post=self.post, user=self.reader)
    
    def test_post_like_count(self):
        """Test post.like_count property"""
        Like.objects.create(post=self.post, user=self.reader)
        self.assertEqual(self.post.like_count, 1)


class LikeViewTests(TestCase):
    """Test like views"""
    
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
    
    def test_toggle_like_requires_login(self):
        """Test toggling like requires authentication"""
        response = self.client.post(
            reverse('likes:toggle_like', args=[self.post.id])
        )
        self.assertEqual(response.status_code, 302)
    
    def test_toggle_like_creates_like(self):
        """Test toggling like when not liked"""
        self.client.login(username='reader', password='testpass123')
        response = self.client.post(
            reverse('likes:toggle_like', args=[self.post.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Like.objects.filter(post=self.post, user=self.reader).exists())
    
    def test_toggle_like_removes_like(self):
        """Test toggling like when already liked"""
        Like.objects.create(post=self.post, user=self.reader)
        self.client.login(username='reader', password='testpass123')
        response = self.client.post(
            reverse('likes:toggle_like', args=[self.post.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Like.objects.filter(post=self.post, user=self.reader).exists())
    
    def test_liked_posts_view(self):
        """Test liked posts view"""
        Like.objects.create(post=self.post, user=self.reader)
        self.client.login(username='reader', password='testpass123')
        response = self.client.get(reverse('likes:liked_posts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
