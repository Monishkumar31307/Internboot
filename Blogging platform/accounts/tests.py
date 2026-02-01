from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile


class ProfileModelTests(TestCase):
    """Test Profile model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_profile_created_on_user_creation(self):
        """Test that profile is auto-created with new user"""
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.role, 'reader')
        self.assertTrue(profile.is_reader)
        self.assertFalse(profile.is_author)
        self.assertFalse(profile.is_admin)
    
    def test_admin_profile_properties(self):
        """Test admin role properties"""
        self.user.profile.role = 'admin'
        self.user.profile.save()
        self.assertTrue(self.user.profile.is_admin)
        self.assertTrue(self.user.profile.is_author)
        self.assertFalse(self.user.profile.is_reader)
    
    def test_author_profile_properties(self):
        """Test author role properties"""
        self.user.profile.role = 'author'
        self.user.profile.save()
        self.assertFalse(self.user.profile.is_admin)
        self.assertTrue(self.user.profile.is_author)
        self.assertFalse(self.user.profile.is_reader)


class AccountsViewTests(TestCase):
    """Test accounts views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            password='testpass123'
        )
    
    def test_register_page_get(self):
        """Test registration page loads"""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
    
    def test_register_user_success(self):
        """Test successful user registration"""
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
        })
        self.assertEqual(User.objects.count(), 2)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_page_get(self):
        """Test login page loads"""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_login_success(self):
        """Test successful login"""
        response = self.client.post(reverse('accounts:login'), {
            'email': 'test@example.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog:home'))
    
    def test_profile_view_requires_login(self):
        """Test profile view requires authentication"""
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)
    
    def test_profile_view_get(self):
        """Test profile page loads for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
    
    def test_logout(self):
        """Test logout"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)
