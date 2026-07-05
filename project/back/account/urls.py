from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    # 아이디/비밀번호 찾기 관련 URL
    path('find-id/', views.find_id, name='find_id'),
    path('password-reset/', views.request_password_reset, name='request_password_reset'),
    path('password-reset/confirm/', views.reset_password, name='reset_password_confirm'),
    
    # 프로필 조회 및 수정
    path('profile/', views.UserProfileView.as_view(), name='profile'),
]
