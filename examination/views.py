from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Examination, Student
from .forms import ExamLoginForm
from .exceloptr import create_students, create_questions
from .serializers import ExamSerializer, AnswerSheetSerializer
from datetime import datetime

# Create your views here.
class QuestionsView(generics.RetrieveAPIView):
    queryset = Examination.objects.all()
    serializer_class = ExamSerializer
    
@api_view(['POST'])
def submit_exam_view(request):
    if request.method == 'POST':
        serializer = AnswerSheetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                exam = Examination.objects.get(pk=serializer.validated_data["examination_id"])
                score = exam.mark(serializer.validated_data["answers"])
                student = Student.objects.get(pk=serializer.validated_data["student_id"])
                student.score = score
                student.save()
                return Response({'success': True})  
            except:
                return Response({'success': False})  

class ExamLoginView(View):
    def get(self, request):
        return render(request, 'examination/index.html', {'form': ExamLoginForm()})

    def post(self, request):
        loginForm = ExamLoginForm(request.POST)
        if loginForm.is_valid():
            try:
                student = Student.objects.get(
                    # Find student with provided unique_id
                    unique_id=int(loginForm.cleaned_data["unique_id"]),
                    # ...belonging to an examination with the provided name
                    examination__name=loginForm.cleaned_data['examination_name'],
                    examination__examiner__username=loginForm.cleaned_data["examiner_name"])  # ...with the examination created by the provided examiner

                today = datetime.now()
                exam_is_not_today = (student.examination.set_date.day != today.day
                                     or student.examination.set_date.month != today.month)

                if exam_is_not_today:
                    loginForm.add_error(None, "Examination is not set for today.")
                else:
                    if student.score is not None:
                        loginForm.add_error(None, "You have already taken this examination")
                    else:
                        request.session["student"] = student.id
                        return HttpResponseRedirect(reverse("examination:test_mode", kwargs={
                            'examination_name': student.examination.name,
                            'unique_id': student.unique_id
                        }))

            except Student.DoesNotExist:
                loginForm.add_error(field=None, error="Invalid login credentials.")

        return render(request, 'examination/index.html', {'form': loginForm})


def test_mode(request, examination_name, unique_id):
    if "student" not in request.session:
        return HttpResponseRedirect(reverse("examination:index"))

    student = Student.objects.get(pk=request.session["student"])
    if (student.unique_id != unique_id
        or student.examination.name != examination_name
        or student.score is not None):
        return HttpResponseRedirect(reverse("examination:index"))
        
    return render(request, "examination/exam.html", {
        'student_id': student.id,
        'examination_id': student.examination.id
    })
