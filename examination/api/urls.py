from django.urls import path
from . import views

app_name = 'api_examination'
urlpatterns = [
    path('<int:pk>', views.QuestionsView.as_view(), name='exam'),
    path('submit', views.submit_exam_view, name='submit'),
    path('add-students', views.create_students, name="add-students")
]