from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'task_name', 'task_desc', 'priority', 'status', 'assigned_user', 'assigned_by']

    
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'comment_by', 'comment', 'comment_at']