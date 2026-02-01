from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods, require_POST
from blog.models import Post
from .models import Comment
from .forms import CommentForm

@login_required(login_url='accounts:login')
@require_http_methods(["GET", "POST"])
def add_comment(request, post_id):
    """Add comment to a post"""
    post = get_object_or_404(Post, id=post_id, status='published')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been posted!')
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()
    
    return render(request, 'comments/add_comment.html', {'form': form, 'post': post})

@login_required(login_url='accounts:login')
@require_http_methods(["GET", "POST"])
def edit_comment(request, comment_id):
    """Edit own comment"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check permission
    if request.user != comment.author:
        messages.error(request, 'You can only edit your own comments')
        return redirect(comment.post.get_absolute_url())
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully')
            return redirect(comment.post.get_absolute_url())
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'comments/edit_comment.html', {'form': form, 'comment': comment})

@login_required(login_url='accounts:login')
@require_POST
def delete_comment(request, comment_id):
    """Delete own comment"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check permission
    if request.user != comment.author and not request.user.profile.is_admin:
        messages.error(request, 'You can only delete your own comments')
        return redirect(comment.post.get_absolute_url())
    
    post = comment.post
    comment.delete()
    messages.success(request, 'Comment deleted successfully')
    return redirect(post.get_absolute_url())
