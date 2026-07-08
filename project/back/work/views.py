from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .models import MainCategory, SubCategory, Work, BrandClient, Project, Inquiry
from .serializers import MainCategorySerializer, SubCategorySerializer, WorkSerializer, BrandClientSerializer, ProjectSerializer, InquirySerializer

class CategoryListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        categories = MainCategory.objects.all().order_by('order')
        serializer = MainCategorySerializer(categories, many=True)
        return Response(serializer.data)

class StatsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = {
            "projects_count": Project.objects.count(),
            "final_cuts_count": Work.objects.count(),
            "clients_count": BrandClient.objects.count(),
            "categories_count": MainCategory.objects.count(),
        }
        return Response(data)

import requests

class YouTubeInfoAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        url = request.query_params.get('url')
        if not url:
            return Response({"error": "URL is required"}, status=400)
            
        try:
            oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
            response = requests.get(oembed_url, timeout=5)
            if response.status_code == 200:
                return Response(response.json())
            else:
                return Response({"error": "Failed to fetch YouTube info"}, status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class YouTubeSearchAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        query = request.query_params.get('q')
        if not query:
            return Response({"error": "검색어(q)를 입력해주세요."}, status=400)
            
        import os
        from django.conf import settings
        
        # .env 파일에서 YOUTUBE_API_KEY 로드 시도
        try:
            from dotenv import load_dotenv
            load_dotenv(os.path.join(settings.BASE_DIR, '.env'))
        except ImportError:
            env_path = os.path.join(settings.BASE_DIR, '.env')
            if os.path.exists(env_path):
                with open(env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('YOUTUBE_API_KEY'):
                            val = line.split('=', 1)[1].strip(' "\'')
                            os.environ['YOUTUBE_API_KEY'] = val
            pass
            
        api_key = os.environ.get('YOUTUBE_API_KEY')
        if not api_key:
            return Response({"error": "백엔드 .env 파일에 YOUTUBE_API_KEY가 설정되지 않았습니다."}, status=500)
            
        try:
            search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults=5&key={api_key}"
            response = requests.get(search_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data.get('items', []):
                    results.append({
                        'title': item['snippet']['title'],
                        'video_id': item['id']['videoId'],
                        'thumbnail_url': item['snippet']['thumbnails']['high']['url'],
                        'youtube_link': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                    })
                return Response(results)
            else:
                return Response({"error": "YouTube API 검색에 실패했습니다."}, status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

# --- Admin CRUD ViewSets ---
class BrandClientViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdminUser] # 권한이 필요할 경우 주석 해제 (일단 테스트를 위해 AllowAny 고려)
    permission_classes = [AllowAny]
    queryset = BrandClient.objects.all().order_by('-created_at')
    serializer_class = BrandClientSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer

class WorkViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Work.objects.all().order_by('-created_at')
    serializer_class = WorkSerializer

class MainCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = MainCategory.objects.all().order_by('order')
    serializer_class = MainCategorySerializer

class SubCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = SubCategory.objects.all().order_by('main_category__order', 'order')
    serializer_class = SubCategorySerializer

class InquiryViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Inquiry.objects.all().order_by('-created_at')
    serializer_class = InquirySerializer
