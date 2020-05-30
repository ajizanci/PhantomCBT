from django.contrib import admin
from .models import Examination, Question, Option

# Register your models here.
class ExaminationAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    
admin.site.register(Examination, ExaminationAdmin)
admin.site.register(Question)
admin.site.register(Option)