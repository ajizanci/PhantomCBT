from django.contrib import admin
from .models import Examination, Student, Question, Option

# Register your models here.
admin.site.register(Examination)
admin.site.register(Student)
admin.site.register(Question)
admin.site.register(Option)