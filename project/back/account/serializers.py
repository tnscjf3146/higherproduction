from rest_framework import serializers
from .models import User, UserInfo
from product.serializers import PlanSerializer
from work.serializers import WorkSerializer
import re # 정규식을 사용하기 위해 임포트

class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password', 'is_admin']
        extra_kwargs = {'password': {'write_only': True}}

    def get_is_admin(self, obj):
        # User와 연결된 UserInfo의 authority 값을 반환 (없으면 False)
        if hasattr(obj, 'userinfo'):
            return obj.userinfo.authority
        return False

    def validate_password(self, value):
        # 1. 길이 검사 (8자 이상)
        if len(value) < 8:
            raise serializers.ValidationError("비밀번호는 8글자 이상이어야 합니다.")
        
        # 2. 대문자 포함 여부 검사
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("비밀번호에는 최소 한 개의 대문자가 포함되어야 합니다.")
            
        # 3. 특수기호 포함 여부 검사
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("비밀번호에는 최소 한 개의 특수기호가 포함되어야 합니다.")
            
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    # 구독 중인 상품 정보를 읽기 전용으로 포함
    production = PlanSerializer(read_only=True)
    
    class Meta:
        model = UserInfo
        fields = ['company_name', 'manager', 'company_address', 'production']


class UserProfileSerializer(serializers.ModelSerializer):
    # 중첩 시리얼라이저로 UserInfo 및 Works 연결
    userinfo = UserInfoSerializer()
    works = WorkSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'userinfo', 'works']
        read_only_fields = ['username'] # 아이디는 수정 불가

    def update(self, instance, validated_data):
        # UserInfo 데이터 분리
        userinfo_data = validated_data.pop('userinfo', None)
        
        # 기본 User 정보 업데이트
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        
        # UserInfo 정보 업데이트
        if userinfo_data is not None:
            # User 생성 시 UserInfo가 무조건 같이 생성되도록 manager에 작성했으므로 instance.userinfo는 존재함
            userinfo = instance.userinfo
            userinfo.company_name = userinfo_data.get('company_name', userinfo.company_name)
            userinfo.manager = userinfo_data.get('manager', userinfo.manager)
            userinfo.company_address = userinfo_data.get('company_address', userinfo.company_address)
            userinfo.save()
            
        return instance
