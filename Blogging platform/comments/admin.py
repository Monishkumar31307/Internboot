from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'approved', 'created_at']
    list_filter = ['approved', 'created_at']
    search_fields = ['author__username', 'post__title', 'content']
    actions = ['approve_comments', 'reject_comments']
    readonly_fields = ['created_at', 'updated_at']
    
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = 'Approve selected comments'
    
    def reject_comments(self, request, queryset):
        queryset.update(approved=False)
    reject_comments.short_description = 'Reject selected comments'
