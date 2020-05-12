from django.urls import path
from .views import ExamLoginView, QuestionsView, test_mode, submit_exam_view

app_name = 'examination'
urlpatterns = [
    path('', ExamLoginView.as_view(), name='index'),
    path('<str:examination_name>/<int:unique_id>', test_mode, name='test_mode'),
    path('<int:pk>', QuestionsView.as_view(), name='exam'),
    path('submit', submit_exam_view, name='submit')
]