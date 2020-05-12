from django import forms

class ExamLoginForm(forms.Form):
    examiner_name = forms.CharField(max_length=100, label='Examiner username') 
    examination_name = forms.CharField(max_length=100, label='Examination name') 
    unique_id = forms.IntegerField(label='Your Unique ID', max_value=999999, min_value=100000)