from django.contrib import admin
from .models import Examination, Question, Option

# Register your models here.
admin.site.register(Examination)
admin.site.register(Question)
admin.site.register(Option)