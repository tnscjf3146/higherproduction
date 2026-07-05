from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryListView, StatsAPIView, BrandClientViewSet, ProjectViewSet, WorkViewSet, CategoryViewSet, YouTubeInfoAPIView, YouTubeSearchAPIView, InquiryViewSet

router = DefaultRouter()
router.register(r'admin/brandclients', BrandClientViewSet, basename='admin-brandclient')
router.register(r'admin/projects', ProjectViewSet, basename='admin-project')
router.register(r'admin/works', WorkViewSet, basename='admin-work')
router.register(r'admin/categories', CategoryViewSet, basename='admin-category')
router.register(r'inquiries', InquiryViewSet, basename='inquiry')

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('stats/', StatsAPIView.as_view(), name='stats_api'),
    path('admin/youtube-info/', YouTubeInfoAPIView.as_view(), name='youtube_info'),
    path('admin/youtube-search/', YouTubeSearchAPIView.as_view(), name='youtube_search'),
    path('', include(router.urls)),
]
