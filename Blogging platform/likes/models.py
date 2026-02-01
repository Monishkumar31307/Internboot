from django.db import models
from django.contrib.auth.models import User
from blog.models import Post

class Like(models.Model):
    """Like model for blog posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['post', 'user']  # One like per user per post
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'
