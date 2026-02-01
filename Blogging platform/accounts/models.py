from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

class Profile(models.Model):
    """Extended user profile with role-based access"""
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('author', 'Author'),
        ('reader', 'Reader'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='reader')
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_author(self):
        return self.role == 'author' or self.role == 'admin'
    
    @property
    def is_reader(self):
        return self.role == 'reader'
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_picture and self.profile_picture.name:
            try:
                img = Image.open(self.profile_picture.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.profile_picture.path)
            except Exception:
                pass  # Image processing failed, skip resizing

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
