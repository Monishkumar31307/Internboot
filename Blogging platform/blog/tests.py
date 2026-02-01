from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Category, Tag
from .forms import PostForm


class CategoryModelTests(TestCase):
    """Test Category model"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Technology',
            description='Tech news and updates'
        )
    
    def test_category_creation(self):
        """Test category is created correctly"""
        self.assertEqual(self.category.name, 'Technology')
        self.assertEqual(self.category.slug, 'technology')
    
    def test_category_slug_auto_generated(self):
        """Test slug is auto-generated from name"""
        cat = Category.objects.create(name='Web Development')
        self.assertEqual(cat.slug, 'web-development')


class TagModelTests(TestCase):
    """Test Tag model"""
    
    def setUp(self):
        self.tag = Tag.objects.create(name='Python')
    
    def test_tag_creation(self):
        """Test tag is created correctly"""
        self.assertEqual(self.tag.name, 'Python')
        self.assertEqual(self.tag.slug, 'python')


class PostModelTests(TestCase):
    """Test Post model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Technology')
        self.post = Post.objects.create(
            title='Test Post',
            author=self.user,
            category=self.category,
            content='<p>Test content</p>',
            status='published'
        )
    
    def test_post_creation(self):
        """Test post is created correctly"""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.slug, 'test-post')
        self.assertEqual(self.post.author, self.user)
    
    def test_post_increment_views(self):
        """Test view counter increments"""
        self.assertEqual(self.post.view_count, 0)
        self.post.increment_views()
        self.post.refresh_from_db()
        self.assertEqual(self.post.view_count, 1)
    
    def test_post_published_at_set_on_publish(self):
        """Test published_at is set when status changes to published"""
        self.assertIsNotNone(self.post.published_at)


class BlogViewTests(TestCase):
    """Test blog views"""
    
    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='testpass123'
        )
        self.author.profile.role = 'author'
        self.author.profile.save()
        
        self.category = Category.objects.create(name='Technology')
        self.tag = Tag.objects.create(name='Python')
        
        self.post = Post.objects.create(
            title='Test Post',
            author=self.author,
            category=self.category,
            content='<p>Test content</p>',
            status='published'
        )
        self.post.tags.add(self.tag)
    
    def test_home_page(self):
        """Test home page loads"""
        response = self.client.get(reverse('blog:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')
    
    def test_post_list(self):
        """Test post list page"""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
    
    def test_post_detail(self):
        """Test post detail page"""
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
    
    def test_post_create_requires_author(self):
        """Test post creation requires author role"""
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)
    
    def test_post_create_by_author(self):
        """Test author can create post"""
        self.client.login(username='author', password='testpass123')
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_create.html')
    
    def test_category_posts(self):
        """Test category posts view"""
        response = self.client.get(self.category.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
    
    def test_tag_posts(self):
        """Test tag posts view"""
        response = self.client.get(self.tag.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)


class PostFormTests(TestCase):
    """Test post form"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Technology')
    
    def test_post_form_valid(self):
        """Test valid post form"""
        form_data = {
            'title': 'New Post',
            'content': '<p>Test content</p>',
            'category': self.category.id,
            'status': 'published',
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_post_form_invalid_no_title(self):
        """Test form is invalid without title"""
        form_data = {
            'content': '<p>Test content</p>',
            'category': self.category.id,
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
