from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import os
import cbt.settings as settings
from .forms import LoginForm, RegisterForm
from examination.exceloptr import create_students, create_questions
from examination.models import Examination, Question, Option
from .models import Profile
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
                    Profile.objects.create(user=user, account_type='Examiner')
                    login(request, user)
                    return HttpResponseRedirect(reverse("examiner:dashboard", kwargs={'username': user.username}))
                
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
                return HttpResponseRedirect(reverse("examiner:dashboard", kwargs={'username': user.username}))
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
        
        #file_path = os.path.join(settings.STATIC_ROOT, f"{request.user.username}.xlsx")
        file_path = f"./static/upfiles/{request.user.username}.xlsx"
        
        try:
            with open(file_path, 'wb+') as dest:
                for chunk in students_and_questions.chunks():
                    dest.write(chunk)
            
            if (create_questions(file_path, exam) and create_students(file_path, exam)):
                return HttpResponseRedirect(reverse("examiner:dashboard", kwargs={'username': request.user.username}))

        except:
            pass
        
        exam.delete()
        return render(request, 'user/auth/add-exam.html', {'errors': ['An error occured while processing the workbook']})

class ExaminationsListView(ListView):
    template_name = 'user/auth/dashboard.html'
    context_object_name = 'examinations'
    
    def get_queryset(self):
        return self.request.user.examinations.all()

class StudentsListView(ListView):
    context_object_name = 'students'
    template_name = 'user/auth/students.html'
    
    def get_queryset(self):
        self.examination = get_object_or_404(Examination, examiner=self.request.user, id=int(self.request.GET["examination"]))
        query = Profile.objects.filter(account_type=2, examination=self.examination)
        
        return map(lambda x: x.user, query)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["examination"] = self.examination.name
        return context

class QuestionsListView(ListView):
    context_object_name = 'questions'
    template_name = 'user/auth/questions.html'
    
    def get_queryset(self):
        self.examination = get_object_or_404(Examination, examiner=self.request.user, id=int(self.request.GET["examination"]))
        return Question.objects.filter(examination=self.examination)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["examination"] = self.examination.name
        return context
    
def logoutu(request):
    logout(request)
    return HttpResponseRedirect(reverse("examiner:login"))
    