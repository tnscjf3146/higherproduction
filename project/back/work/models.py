from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='카테고리명')
    subtitle = models.CharField(max_length=100, blank=True, null=True, verbose_name='카테고리 소제목')
    order = models.IntegerField(default=0, verbose_name='노출 순서(낮을수록 먼저 보임)')
    is_vertical = models.BooleanField(default=False, verbose_name='세로형(쇼츠) 여부')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Work(models.Model):
    STATUS_CHOICES = (
        ('IN_PROGRESS', '작업중'),
        ('COMPLETED', '완료됨'),
    )
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='works', verbose_name='카테고리')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='works', verbose_name='관련 고객')
    title = models.CharField(max_length=255, verbose_name='작품명')
    youtube_link = models.URLField(verbose_name='영상 링크', blank=True, null=True)
    content = models.TextField(verbose_name='게시글 내용', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS', verbose_name='진행 상태')
    is_visible = models.BooleanField(default=True, verbose_name='공개 여부')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class BrandClient(models.Model):
    name = models.CharField(max_length=255, verbose_name='브랜드명')
    subtitle = models.CharField(max_length=255, blank=True, null=True, verbose_name='부가설명')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    
    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=255, verbose_name='프로젝트명')
    subtitle = models.CharField(max_length=255, blank=True, null=True, verbose_name='부가설명')
    client = models.ForeignKey(BrandClient, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects', verbose_name='브랜드 클라이언트')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    
    def __str__(self):
        return self.title

class Inquiry(models.Model):
    STATUS_CHOICES = (
        ('UNPROCESSED', '미접수'),
        ('IN_PROGRESS', '처리 중'),
        ('COMPLETED', '처리 완료'),
    )
    title = models.CharField(max_length=255, verbose_name='제목')
    name = models.CharField(max_length=100, verbose_name='성함')
    company = models.CharField(max_length=100, blank=True, null=True, verbose_name='회사명')
    phone = models.CharField(max_length=20, verbose_name='연락처')
    email = models.EmailField(blank=True, null=True, verbose_name='이메일')
    category = models.CharField(max_length=100, blank=True, null=True, verbose_name='카테고리')
    budget = models.CharField(max_length=100, blank=True, null=True, verbose_name='예산')
    details = models.TextField(blank=True, null=True, verbose_name='상세 요청사항')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    is_read = models.BooleanField(default=False, verbose_name='확인 여부')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNPROCESSED', verbose_name='처리 상태')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.title}"
