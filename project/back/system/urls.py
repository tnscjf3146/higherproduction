from django.urls import path
from .views import SiteSettingAPIView

urlpatterns = [
    path('settings/', SiteSettingAPIView.as_view(), name='site_settings'),
]
