from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from examination.models import Examination
from user.models import Profile
from examination.exceloptr import generate_unique_id
from .serializers import ExamSerializer, AnswerSheetSerializer, AddStudentsSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_students(request):
    if request.user.profile.account_type == 1:
        serializer = AddStudentsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                exam = Examination.objects.get(pk=int(serializer.validated_data['examination_id']))
                if exam.examiner.id != request.user.id:
                    return Response({'response': 'You do not have permission to perform this action.'})                

                resp = []
                for student in serializer.validated_data["students"]:
                    uid = generate_unique_id()
                    st = User.objects.create_user(username=f"{student['first_name']}{uid}", **student)
                    Profile.objects.create(user=st, examination=exam, account_type=2, unique_id=uid)
                    Token.objects.create(user=st)
                    resp.append({ **student, 'unique_id': uid })
                
                return Response(resp)
                    
            except Examination.DoesNotExist:
                return Response({'response': 'Examination with provided id does not exist.'})
        else:
            return Response({'response': 'Invalid request format.', 'errors': serializer.errors})
        
    return Response({'response': 'You do not have permission to perform this action.'})

@api_view(["POST"])
def examination_login(request, id):
    uid = request.POST['unique_id']
    try:
        student_profile = Profile.objects.get(unique_id=uid, examination__id=id)
        t = Token.objects.get(user=student_profile.user)
        return Response({ 'token': t.key })
    
    except User.DoesNotExist:
        return Response({ 'response': 'Invalid credentials' })

class QuestionsView(generics.RetrieveAPIView):
    queryset = Examination.objects.all()
    serializer_class = ExamSerializer
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_exam_view(request):
    if request.method == 'POST':
        serializer = AnswerSheetSerializer(data=request.data)
        if serializer.is_valid():
            exam = Examination.objects.get(pk=int(serializer.validated_data["examination_id"]))
            score = exam.mark(serializer.validated_data["answers"])
            student = User.objects.get(id=int(serializer.validated_data["student_id"]))
            student.profile.score = score
            student.profile.save()
            return Response({'success': True})    
        
        return Response({'success': False, 'err': serializer.errors})  
        