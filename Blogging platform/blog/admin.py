from django.contrib import admin
from .models import Post, Category, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'published_at', 'view_count']
    list_filter = ['status', 'category', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    fieldsets = (
        ('Post Information', {'fields': ('title', 'slug', 'author', 'category', 'tags')}),
        ('Content', {'fields': ('excerpt', 'content', 'featured_image')}),
        ('SEO', {'fields': ('meta_description', 'meta_keywords')}),
        ('Status', {'fields': ('status', 'published_at')}),
        ('Statistics', {'fields': ('view_count',), 'classes': ('collapse',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    readonly_fields = ['created_at', 'updated_at', 'view_count']
    date_hierarchy = 'published_at'
