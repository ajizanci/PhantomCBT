from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import os
import cbt.settings as settings
from .forms import LoginForm, RegisterForm
from examination.exceloptr import create_students, create_questions
from examination.models import Examination, Question, Student, Option
# Create your views here.
def index(request):
    return render(request, 'user/index.html')

class Register(View):
    def get(self, request):
        return render(request, 'user/register.html', {'form': RegisterForm()})
    
    def post(self, request):
        rform = RegisterForm(request.POST)
        if rform.is_valid():
            if rform.cleaned_data["password"] == rform.cleaned_data["confirm_password"]:
                try:
                    user = User.objects.create_user(rform.cleaned_data["username"], password=rform.cleaned_data["password"])
                    login(request, user)
                    return HttpResponseRedirect(reverse("user:dashboard", kwargs={'username': user.username}))
                
                except:
                    rform.add_error(field="username", error="Username is already taken.")
            else:
                rform.add_error(field="confirm_password", error="Passowords do not match.")
            
        return render(request, 'user/register.html', {'form': rform})

class Login(View):
    def get(self, request):
        return render(request, 'user/login.html', {"form": LoginForm()})
    
    def post(self, request):
        lform = LoginForm(request.POST)
        if lform.is_valid():
            username = lform.cleaned_data["username"]
            password = lform.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("user:dashboard", kwargs={'username': user.username}))
            else:
                lform.add_error(field=None, error="Invalid login credentials")
                
        return render(request, 'user/login.html', {'form': lform})
        
class AddExamination(View):
    def get(self, request):
        return render(request, 'user/auth/add-exam.html')
    
    def post(self, request):
        name = request.POST["examination_name"]
        duration = float(request.POST["duration"])
        num_questions = int(request.POST["num_questions"])
        date = request.POST["date"]
        students_and_questions = request.FILES["students_and_questions"]
        
        exam = Examination.objects.create(
            examiner=request.user,
            name=name,
            duration=duration,
            set_date=date,
            num_questions=num_questions)
        
        file_path = os.path.join(settings.STATIC_ROOT, 'upfiles', f"{request.user.username}.xlsx")
        
        try:
            with open(file_path, 'wb+') as dest:
                for chunk in students_and_questions.chunks():
                    dest.write(chunk)
            
            if (create_questions(file_path, exam) and create_students(file_path, exam)):
                return HttpResponseRedirect(reverse("user:dashboard", kwargs={'username': request.user.username}))

        except:
            exam.delete()
            return render(request, 'user/auth/add-exam.html', {'errors': ['An error occured while processing the workbook']})

def dashboard(request, username):
    if request.user.is_authenticated and request.user.username == username:
        return render(request, 'user/auth/dashboard.html', {
            'examinations': request.user.examinations.all()
         })
    else:
        return HttpResponseRedirect(reverse("user:login"))

def questions_view(request):
    if request.user.is_authenticated:
        eid = int(request.GET["examination"])
        try:
            examination = request.user.examinations.get(pk=eid)
            questions = Question.objects.filter(examination=examination)
            qs = []
            for question in questions:
                q = {'content': question.content, 'options': []}
                for option in Option.objects.filter(question=question):
                    if option.is_correct:
                        q["correct_option"] = option.option_content
                    q["options"].append({'option_content': option.option_content})
                qs.append(q)
            
            return render(request, 'user/auth/questions.html', {'examination': examination.name, 'questions': qs})
        except:
            return HttpResponseRedirect(reverse("user:login"))
        
    else:
        return HttpResponseRedirect(reverse("user:login"))

def students_view(request):
    if request.user.is_authenticated:
        eid = int(request.GET["examination"])
        try:
            examination = request.user.examinations.get(pk=eid)
            students = Student.objects.filter(examination=examination)
            return render(request, 'user/auth/students.html', {
                'examination': examination.name,
                'students': students
            })
        except:
            return HttpResponseRedirect(reverse("user:login"))
            
    else:
        return HttpResponseRedirect(reverse("user:login"))


def logoutu(request):
    logout(request)
    return HttpResponseRedirect(reverse("user:login"))
    
