from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('workorder/', views.WorkorderView.as_view(), name='workorder'),
    path('workorder/<int:pk>/', views.WorkorderView.as_view(), name='workorder'),
    path('comment/', views.CommentsView.as_view(), name='comment'),
]