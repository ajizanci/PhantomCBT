from django.db import models
from django.contrib.auth.models import User
from examination.models import Examination

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10, choices=(
        (1, 'Examiner'),
        (2, 'Student')
    ))
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE, related_name="students", blank=True, null=True)
    unique_id = models.IntegerField(blank=True, null=True)
    score = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    