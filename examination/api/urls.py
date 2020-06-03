from django.urls import path
from . import views

app_name = 'api_examination'
urlpatterns = [
    path('<int:pk>/questions/', views.QuestionsView.as_view(),
         name='exam-questions'),
    path('submit', views.submit_exam_view, name='submit-exam'),
    path('add-students/', views.create_students, name="add-students"),
    path('<int:id>/login/', views.examination_login, name="exam-login")
]
