from django.shortcuts import render
from django.contrib.auth import login
from django.views.generic import View
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Examination
from user.models import Profile
from .forms import ExamLoginForm
from .exceloptr import create_students, create_questions
from datetime import datetime

# Create your views here.
class ExamLoginView(View):
    def get(self, request):
        return render(request, 'examination/index.html', {'form': ExamLoginForm()})

    def post(self, request):
        loginForm = ExamLoginForm(request.POST)
        if loginForm.is_valid():
            try:
                student_profile = Profile.objects.get(
                    # Find student with provided unique_id
                    unique_id=int(loginForm.cleaned_data["unique_id"]),
                    # ...belonging to an examination with the provided name
                    examination__name=loginForm.cleaned_data['examination_name'],
                    examination__examiner__username=loginForm.cleaned_data["examiner_name"])  # ...with the examination created by the provided examiner

                student = student_profile.user
                today = datetime.now()
                exam_is_not_today = (student_profile.examination.set_date.day != today.day
                                     or student_profile.examination.set_date.month != today.month)

                if exam_is_not_today:
                    loginForm.add_error(None, "Examination is not set for today.")
                else:
                    if student_profile.score is not None:
                        loginForm.add_error(None, "You have already taken this examination")
                    else:
                        login(request, student)
                        return HttpResponseRedirect(reverse("examination:test_mode", kwargs={
                            'examination_name': student_profile.examination.name,
                            'unique_id': student_profile.unique_id
                        }))

            except User.DoesNotExist:
                loginForm.add_error(field=None, error="Invalid login credentials.")

        return render(request, 'examination/index.html', {'form': loginForm})


def test_mode(request, examination_name, unique_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("examination:index"))

    student = request.user
    if (student.profile.unique_id != unique_id
        or student.profile.examination.name != examination_name
        or student.profile.score is not None):
        return HttpResponseRedirect(reverse("examination:index"))
        
    return render(request, "examination/exam.html", {
        'student_id': student.id,
        'examination_id': student.profile.examination.id
    })
