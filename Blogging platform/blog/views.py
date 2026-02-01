from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Post, Category, Tag
from .forms import PostForm
from functools import wraps

# Decorators
def author_required(view_func):
    """Decorator for views that require author or admin role"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.profile.is_author:
            messages.error(request, 'You must be an author to access this page.')
            return redirect('blog:home')
        return view_func(request, *args, **kwargs)
    return wrapper

# Views
def home(request):
    """Homepage with recent published posts"""
    featured_post = Post.objects.filter(status='published').first()
    recent_posts = Post.objects.filter(status='published').order_by('-published_at')[:6]
    categories = Category.objects.all()[:5]
    tags = Tag.objects.all()[:8]
    
    context = {
        'featured_post': featured_post,
        'recent_posts': recent_posts,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'blog/home.html', context)

def post_list(request):
    """List all published posts with search and filters"""
    posts = Post.objects.filter(status='published').order_by('-published_at')
    
    # Search
    search_query = request.GET.get('q')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    """View single post with comments"""
    post = get_object_or_404(Post, slug=slug, status='published')
    post.increment_views()
    
    comments = post.comments.filter(approved=True)
    is_liked = False
    if request.user.is_authenticated:
        is_liked = post.likes.filter(user=request.user).exists()
    
    related_posts = Post.objects.filter(
        status='published',
        category=post.category
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required(login_url='accounts:login')
@author_required
@require_http_methods(["GET", "POST"])
def post_create(request):
    """Create new blog post (authors only)"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'Post created successfully!')
            if request.POST.get('publish'):
                post.status = 'published'
                post.save()
                messages.success(request, 'Post published!')
                return redirect('blog:post_detail', slug=post.slug)
            else:
                return redirect('blog:my_posts')
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})

@login_required(login_url='accounts:login')
@author_required
@require_http_methods(["GET", "POST"])
def post_edit(request, slug):
    """Edit blog post (author or admin only)"""
    post = get_object_or_404(Post, slug=slug)
    
    # Check permissions
    if request.user != post.author and not request.user.profile.is_admin:
        messages.error(request, 'You can only edit your own posts')
        return redirect('blog:post_detail', slug=post.slug)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})

@login_required(login_url='accounts:login')
@author_required
@require_http_methods(["GET", "POST"])
def post_delete(request, slug):
    """Delete blog post (author or admin only)"""
    post = get_object_or_404(Post, slug=slug)
    
    # Check permissions
    if request.user != post.author and not request.user.profile.is_admin:
        messages.error(request, 'You can only delete your own posts')
        return redirect('blog:post_detail', slug=post.slug)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('blog:home')
    
    return render(request, 'blog/post_delete.html', {'post': post})

def category_posts(request, slug):
    """View posts by category"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published').order_by('-published_at')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category_posts.html', context)

def tag_posts(request, slug):
    """View posts by tag"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status='published').order_by('-published_at')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    return render(request, 'blog/tag_posts.html', context)

@login_required(login_url='accounts:login')
@author_required
def my_posts(request):
    """View current user's posts"""
    posts = request.user.blog_posts.filter(status='published').order_by('-published_at')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'blog/my_posts.html', context)

@login_required(login_url='accounts:login')
@author_required
def draft_posts(request):
    """Manage draft posts"""
    posts = request.user.blog_posts.filter(status='draft').order_by('-updated_at')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'blog/draft_posts.html', context)
