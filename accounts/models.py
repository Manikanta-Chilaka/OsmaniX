from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField   # ✅ REQUIRED

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = CloudinaryField(
        'avatar',
        blank=True,
        null=True,
        default='avatars/default-avatar'
    )

    followers = models.ManyToManyField(
        User, related_name='followers', blank=True
    )
    following = models.ManyToManyField(
        User, related_name='following', blank=True
    )

    bio = models.CharField(max_length=255, blank=True)

    articles_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
