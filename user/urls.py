from django.urls import path
from .views import index, Login, Register, ExaminationsListView, logoutu, AddExamination, QuestionsListView, StudentsListView

app_name = 'user'
urlpatterns = [
    path('', index, name='index'),
    path('user/login', Login.as_view(), name='login'),
    path('user/logout', logoutu, name='logout'),
    path('user/register', Register.as_view(), name='register'),
    path('user/addexamination', AddExamination.as_view(), name='add'),
    path('user/<str:username>', ExaminationsListView.as_view(), name='dashboard'),
    path('user/questions/', QuestionsListView.as_view(), name='questions'),
    path('user/students/', StudentsListView.as_view(), name='students')
]