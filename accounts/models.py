from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )

    # These are needed to avoid clashes with auth.User
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name="customuser_groups",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name="customuser_permissions",
        related_query_name="customuser",
    )

    class Meta:
        db_table = 'custom_user'
        swappable = 'AUTH_USER_MODEL'
