from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from blog.models import Post
from .models import Like

@login_required(login_url='accounts:login')
@require_POST
def toggle_like(request, post_id):
    """Toggle like on a post (AJAX)"""
    post = get_object_or_404(Post, id=post_id)
    
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        # User already liked, so unlike
        like.delete()
        liked = False
    else:
        liked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX request
        return JsonResponse({
            'liked': liked,
            'like_count': post.like_count,
        })
    else:
        # Redirect fallback
        return redirect(post.get_absolute_url())

@login_required(login_url='accounts:login')
def liked_posts(request):
    """View user's liked posts"""
    liked_posts = request.user.liked_posts.all()
    from django.core.paginator import Paginator
    
    paginator = Paginator(liked_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    from django.shortcuts import render
    return render(request, 'likes/liked_posts.html', {'page_obj': page_obj})
