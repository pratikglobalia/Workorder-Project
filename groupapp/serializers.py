from rest_framework import serializers
from .models import Comments, User, WorkOrder
from django.contrib.auth.models import Group

class RegisterSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(many=True, slug_field="name", queryset=Group.objects.all())
    mobile_no = serializers.IntegerField(required=True)
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'mobile_no', 'groups']


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    
    
class CommentsSerializer(serializers.ModelSerializer):
    comment_by = serializers.CharField(read_only=True)
    class Meta:
        model = Comments
        fields = ['task', 'comment', 'comment_at', 'comment_by']
        read_only_fields = ['comment_at']

    
class WorkOrderSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()
    assigned_user = serializers.StringRelatedField()
    assigned_by = serializers.StringRelatedField()
    def get_comment(self, obj):
        comment = Comments.objects.filter(task=obj)
        return CommentsSerializer(comment, many=True).data
    
    class Meta:
        model = WorkOrder
        fields = ['task_name', 'task_desc', 'priority', 'status', 'assigned_user', 'assigned_by', 'comment']
        
        
class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = ['task_name', 'task_desc', 'priority', 'status']


class ManagerSerializer(serializers.ModelSerializer):
    task_name = serializers.ReadOnlyField()
    assigned_by = serializers.ReadOnlyField(source='name')
    class Meta:
        model = WorkOrder
        fields = ['task_name', 'priority', 'assigned_user', 'assigned_by']
        

class EmployeeSerializer(serializers.ModelSerializer):
    task_name = serializers.ReadOnlyField()
    class Meta:
        model =WorkOrder
        fields = ['task_name', 'status']