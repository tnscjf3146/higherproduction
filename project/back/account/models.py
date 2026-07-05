from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have a username')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        # 유저가 생성될 때 기본 UserInfo도 함께 생성
        UserInfo.objects.create(user=user)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        user = self.create_user(username, password, **extra_fields)
        
        # 슈퍼유저는 UserInfo의 권한을 관리자로 설정
        user.userinfo.authority = True
        user.userinfo.is_staff = True
        user.userinfo.save()
        
        return user


class User(AbstractBaseUser):
    # README 요구사항에 맞춘 User 모델
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    objects = MyUserManager()

    # 아이디로 username 사용
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    # 관리자 페이지 접근 등을 위한 필수 메서드
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        # 장고 관리자 페이지 접근 권한은 UserInfo의 is_staff 필드에 따름
        if hasattr(self, 'userinfo'):
            return self.userinfo.is_staff
        return False


class UserInfo(models.Model):
    # README 요구사항에 맞춘 UserInfo 모델
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userinfo')
    company_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='회사명')
    manager = models.CharField(max_length=100, blank=True, null=True, verbose_name='담당자명')
    company_address = models.CharField(max_length=255, blank=True, null=True, verbose_name='회사 주소')
    
    authority = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    # product 앱의 Plan 모델을 바라보도록 문자열 참조 사용 (앱 생성 전이어도 오류 안 남)
    production = models.ForeignKey('product.Plan', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Info"
