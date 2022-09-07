from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    mobile_no = models.IntegerField(null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    

priority_choices = (
    ('low','low'),
    ('medium','medium'),
    ('high','high')
    )
status_chioces = (
    ('pending','pending'),
    ('inprogres','inprogres'),
    ('complete','complete')
    )
class WorkOrder(models.Model):
    task_name = models.CharField(max_length=100, blank=True, null=True)
    task_desc = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=7, choices=priority_choices, blank=True, null=True)
    status = models.CharField(max_length=10, choices=status_chioces, blank=True, null=True)
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_user', blank=True, null=True)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_by', blank=True, null=True)
    
    def __str__(self):
        return self.task_name
    
    
class Comments(models.Model):
    task = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_at = models.DateTimeField(auto_now_add=True)