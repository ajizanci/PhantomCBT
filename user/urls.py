from django.urls import path
from .views import index, Login, Register, dashboard, logoutu, AddExamination, questions_view, students_view

app_name = 'user'
urlpatterns = [
    path('', index, name='index'),
    path('user/login', Login.as_view(), name='login'),
    path('user/logout', logoutu, name='logout'),
    path('user/register', Register.as_view(), name='register'),
    path('user/addexamination', AddExamination.as_view(), name='add'),
    path('user/<str:username>', dashboard, name='dashboard'),
    path('user/questions/', questions_view, name='questions'),
    path('user/students/', students_view, name='students')
]