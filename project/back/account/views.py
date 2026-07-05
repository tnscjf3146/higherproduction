from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer

# 찾기 기능용 추가 임포트
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from .models import User
from .serializers import UserSerializer, UserProfileSerializer
import re

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({"error": "아이디와 비밀번호를 모두 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)
        
        return Response({
            "message": "로그인 성공!",
            "user": serializer.data,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "아이디 또는 비밀번호가 틀렸습니다."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    # JWT 방식이므로 백엔드 로그아웃은 별도 작업 없이 성공 응답만 주고, 실제 처리는 프론트엔드 토큰 삭제로 이루어집니다.
    return Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def find_id(request):
    email = request.data.get('email')
    
    if not email:
        return Response({"error": "가입 시 입력한 이메일을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        user = User.objects.get(email=email)
        # 마스킹 처리: 앞 3자리까지만 보여주고 나머지 별표
        username = user.username
        if len(username) > 3:
            masked_username = username[:3] + '*' * (len(username) - 3)
        else:
            masked_username = username[:1] + '*' * (len(username) - 1)
            
        return Response({"message": "아이디를 찾았습니다.", "username": masked_username}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "해당 이메일로 가입된 계정이 없습니다."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset(request):
    username = request.data.get('username')
    email = request.data.get('email')
    
    if not username or not email:
        return Response({"error": "아이디와 이메일을 모두 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        user = User.objects.get(username=username, email=email)
        
        # 재설정용 일회용 토큰 및 유저 식별자 생성
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        # 프론트엔드 비밀번호 재설정 페이지 URL 조합
        reset_url = f"http://localhost:3000/account/reset-password?uid={uid}&token={token}"
        
        # settings.py의 EMAIL_BACKEND 설정에 따라 콘솔 창에 출력됨
        send_mail(
            subject='[하이어 프로덕션] 비밀번호 재설정 링크 안내',
            message=f'안녕하세요 {username}님,\n\n아래 링크를 클릭하여 비밀번호를 재설정해 주세요:\n\n{reset_url}\n\n본인이 요청하지 않았다면 이 이메일을 무시해 주세요.',
            from_email='noreply@higherproduction.com',
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        return Response({"message": "비밀번호 재설정 링크를 이메일로 발송했습니다.\n(현재 개발 환경이므로 백엔드 터미널 창을 확인하세요!)"}, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({"error": "입력하신 정보와 일치하는 계정이 없습니다."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    uidb64 = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('password')
    
    if not uidb64 or not token or not new_password:
        return Response({"error": "잘못된 요청입니다. 필요한 정보가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        # uid를 통해 유저 식별
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        # 전달받은 토큰이 이 유저에게 발급된 유효한 토큰인지 검증
        if default_token_generator.check_token(user, token):
            # 비밀번호 유효성 검사 (serializer와 동일한 규칙)
            if len(new_password) < 8 or not re.search(r'[A-Z]', new_password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
                return Response({"error": "비밀번호는 8글자 이상, 대문자 1개 이상, 특수문자 1개 이상을 포함해야 합니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            # 비밀번호 변경 및 저장 (기존 토큰은 자동 무효화됨)
            user.set_password(new_password)
            user.save()
            return Response({"message": "비밀번호가 성공적으로 변경되었습니다. 새로운 비밀번호로 로그인해 주세요."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "유효하지 않거나 이미 사용된(만료된) 링크입니다."}, status=status.HTTP_400_BAD_REQUEST)
            
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({"error": "유효하지 않은 링크 형식입니다."}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    # URL에서 pk를 받지 않고, 토큰을 통해 로그인한 유저 본인 객체를 반환
    def get_object(self):
        return self.request.user
