import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_platform.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post, Category, Tag
from accounts.models import Profile
from likes.models import Like
from comments.models import Comment
from django.utils import timezone
from datetime import timedelta

def create_sample_data():
    print("Creating sample data...")
    
    # Delete existing data
    User.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()
    
    # Create users
    admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    admin_user.first_name = 'Admin'
    admin_user.last_name = 'User'
    admin_user.save()
    admin_user.profile.role = 'admin'
    admin_user.profile.bio = 'I am the platform administrator'
    admin_user.profile.save()
    
    authors = []
    for i in range(1, 4):
        user = User.objects.create_user(f'author{i}', f'author{i}@example.com', 'pass123')
        user.first_name = f'Author'
        user.last_name = f'{i}'
        user.save()
        user.profile.role = 'author'
        user.profile.bio = f'I am a professional author and writer. Welcome to my blog!'
        user.profile.location = f'City {i}'
        user.profile.save()
        authors.append(user)
    
    readers = []
    for i in range(1, 4):
        user = User.objects.create_user(f'reader{i}', f'reader{i}@example.com', 'pass123')
        user.first_name = f'Reader'
        user.last_name = f'{i}'
        user.save()
        user.profile.role = 'reader'
        user.profile.bio = f'Passionate reader and commenter'
        user.profile.save()
        readers.append(user)
    
    # Create categories
    categories = []
    category_names = ['Technology', 'Lifestyle', 'Business', 'Health', 'Travel']
    for name in category_names:
        cat = Category.objects.create(name=name, description=f'{name} related articles and insights')
        categories.append(cat)
    
    # Create tags
    tags = []
    tag_names = ['python', 'django', 'web', 'tips', 'tutorial', 'news', 'review', 'howto']
    for name in tag_names:
        tag = Tag.objects.create(name=name)
        tags.append(tag)
    
    # Create posts
    posts = []
    post_titles = [
        'Getting Started with Django',
        'Python Tips and Tricks',
        'Web Development Best Practices',
        'Building REST APIs',
        'Database Design Patterns',
        'CSS Grid vs Flexbox',
        'JavaScript Async/Await Guide',
        'Docker for Beginners',
        'Git Workflow Best Practices',
        'Testing in Django',
        'Security in Web Applications',
        'Performance Optimization',
        'Mobile First Design',
        'Machine Learning Basics',
        'Cloud Deployment Guide'
    ]
    
    for idx, title in enumerate(post_titles):
        post = Post.objects.create(
            title=title,
            author=authors[idx % len(authors)],
            category=categories[idx % len(categories)],
            content=f'''
            <p>This is a detailed blog post about <strong>{title}</strong>.</p>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
            <h3>Main Points:</h3>
            <ul>
                <li>First important point about the topic</li>
                <li>Second key insight</li>
                <li>Third consideration</li>
            </ul>
            <p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
            <pre><code>code example here</code></pre>
            <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p>
            ''',
            excerpt=f'Learn about {title} - a comprehensive guide with tips and best practices.',
            status='published',
            published_at=timezone.now() - timedelta(days=idx),
            meta_description=f'Blog post about {title}',
            meta_keywords=title.lower()
        )
        post.tags.set(tags[idx % len(tags):idx % len(tags) + 2])
        posts.append(post)
    
    #Create comments
    for post in posts[:5]:
        for reader in readers:
            Comment.objects.create(
                post=post,
                author=reader,
                content=f'Great post about {post.title}! Really helpful information.',
                approved=True
            )
    
    # Create likes
    for post in posts:
        for reader in readers:
            if (hash(f"{post.id}{reader.id}")) % 2:  # Random likes
                Like.objects.create(post=post, user=reader)
    
    print(f"✓ Created {len(authors)} authors")
    print(f"✓ Created {len(readers)} readers")
    print(f"✓ Created {len(categories)} categories")
    print(f"✓ Created {len(tags)} tags")
    print(f"✓ Created {len(posts)} posts")
    print("✓ Created comments and likes")
    print("\nSample data created successfully!")

if __name__ == '__main__':
    create_sample_data()
