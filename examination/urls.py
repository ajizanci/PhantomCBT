from django.urls import path
from .views import ExamLoginView, test_mode

app_name = 'examination'
urlpatterns = [
    path('', ExamLoginView.as_view(), name='index'),
    path('<str:examination_name>/<int:unique_id>', test_mode, name='test_mode'),
]