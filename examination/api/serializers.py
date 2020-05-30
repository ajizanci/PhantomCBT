from rest_framework import serializers
from django.contrib.auth.models import User
from examination.models import Examination, Question, Option


class AnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_option = serializers.IntegerField(allow_null=True, required=False, default=None)
    

class AnswerSheetSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    examination_id = serializers.IntegerField()
    answers = AnswerSerializer(many=True)

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_content']
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
     
class AddStudentsSerializer(serializers.Serializer):
    examination_id = serializers.IntegerField()
    students = StudentSerializer(many=True)
        
class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'content', 'options']

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Examination
        fields = ['id', 'duration', 'name', 'num_questions', 'questions']