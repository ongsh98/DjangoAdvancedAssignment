from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .models import CustomUser

class SignUpAPIView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        # 요청에서 사용자가 제공한 username과 password 가져오기
        username = request.data.get('username')
        password = request.data.get('password')
        
        # 사용자 인증 시도
        user = authenticate(username=username, password=password)
        
        if user:
            # 사용자가 인증되면 토큰 생성 또는 반환
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'created': created})  # 'created' 값을 함께 반환
        else:
            # 인증 실패 시 오류 응답 반환
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileAPIView(APIView):
    # 인증이 필요한 API이므로 IsAuthenticated 권한을 사용합니다.
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 요청한 사용자의 프로필 정보 가져오기
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

from django.contrib.auth import authenticate

user = authenticate(username='example_user', password='example_password')

if user is not None:
    # 인증 성공
    print("인증 성공")
else:
    # 인증 실패
    print("인증 실패")