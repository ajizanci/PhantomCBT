from django.db import models
from django.contrib.auth.models import User
from random import randint
from datetime import datetime

# Create your models here.
class Examination(models.Model):
    examiner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='examinations')
    name = models.CharField(max_length=64)
    num_questions = models.IntegerField()
    duration = models.DecimalField(decimal_places=2, max_digits=5)
    set_date = models.DateField()
    
    def generate_random_questions(self):
        questions = list(self.questions.all())
        
        if len(questions) >= self.num_questions:
            random_questions = []
            for i in range(self.num_questions):
                r = randint(i+1, self.num_questions - 1)
                random_questions.append(questions[r])
                
            return random_questions
        
        return questions
    
    @property
    def status(self):
        if len(self.students.all()) == 0:
            return False
        
        scores = map(lambda x: x.score is not None, self.students.all())
        return all(scores)
    
    def mark(self, answers):
        score = 0
        for answer in answers:
            question = Question.objects.get(pk=answer["question_id"])
            correct_option = Option.objects.get(question=question, is_correct=True)
            if answer["selected_option"] == correct_option.id:
                score += 1
        
        return round(100 * score / self.num_questions, 2)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE, related_name='students')
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    unique_id = models.IntegerField()
    score = models.DecimalField(null=True, decimal_places=2, max_digits=5, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Question(models.Model):
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE, related_name='questions')
    content = models.TextField()

    def __str__(self):
        return self.content

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_content = models.TextField()
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.option_content
