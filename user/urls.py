from django.urls import path
from . import views

app_name = 'examiner'
urlpatterns = [
    path('', views.index, name='index'),
    path('examiner/login', views.Login.as_view(), name='login'),
    path('examiner/logout', views.logoutu, name='logout'),
    path('examiner/register', views.Register.as_view(), name='register'),
    path('examiner/addexamination', views.AddExamination.as_view(), name='add'),
    path('examiner/<str:username>', views.ExaminationsListView.as_view(), name='dashboard'),
    path('examiner/questions/', views.QuestionsListView.as_view(), name='questions'),
    path('examiner/students/', views.StudentsListView.as_view(), name='students')
]