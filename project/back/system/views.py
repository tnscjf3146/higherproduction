from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import SiteSetting
from .serializers import SiteSettingSerializer

class SiteSettingAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        setting, created = SiteSetting.objects.get_or_create(id=1)
        serializer = SiteSettingSerializer(setting)
        return Response(serializer.data)

    def patch(self, request):
        setting, created = SiteSetting.objects.get_or_create(id=1)
        serializer = SiteSettingSerializer(setting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
