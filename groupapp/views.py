from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth import login
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, WorkOrder
from rest_framework.permissions import IsAuthenticated
from .permissions import CustomPermission
from django.conf import settings

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    

class RegisterView(APIView):
    def get(self, request):
        user = User.objects.all()
        serializer = RegisterSerializer(user, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer =RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            return Response({'Data Registered!!'})
        return Response(serializer.errors)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    token = get_tokens_for_user(user)
                    data = {
                        'email' : serializer.validated_data['email'],
                        'token' : token
                    }
                    return Response(data)
            return Response({'Invalid email or password!!'})
        return Response(serializer.errors)
    

class WorkorderView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.groups.filter(name='owner'):
            workorder = WorkOrder.objects.all()
            serializer = WorkOrderSerializer(workorder, many=True)
            return Response(serializer.data)
        elif request.user.groups.filter(name='manager'):
            workorder = WorkOrder.objects.filter(assigned_by=request.user)
            serializer = WorkOrderSerializer(workorder, many=True)
            return Response(serializer.data)
        elif request.user.groups.filter(name='employee'):
            workorder = WorkOrder.objects.filter(assigned_user=request.user)
            serializer = WorkOrderSerializer(workorder, many=True)
            return Response(serializer.data)
        else:
            return Response({'Access Denied!!'})
            
    def post(self, request):
        if request.user.groups.filter(name=settings.OWNER_NAME):
            serializer = OwnerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response({'Access Denied!!'})
    
    def put(self, request, pk):
        if request.user.groups.filter(name='manager'):
            work = WorkOrder.objects.get(id=pk) 
            serializer = ManagerSerializer(work, data=request.data)
            if serializer.is_valid():
                serializer.save(assigned_by=request.user)
                return Response(serializer.data)
            return Response(serializer.errors)
        elif request.user.groups.filter(name='employee'):
            work = WorkOrder.objects.get(id=pk)
            serializer = EmployeeSerializer(work, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({'Access Denied!!'})
        
    def delete(self, request, pk):
        if request.user.groups.filter(name='owner'):
            work = WorkOrder.objects.get(id=pk)
            work.delete()
            return Response({'Data Deleted!!'})
        return Response({'Access Denied!!'})
    
    
class CommentsView(APIView):
    permission_classes = [CustomPermission]
    def post(self, request):
        try:
            serializer = CommentsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(comment_by=request.user)
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            raise e