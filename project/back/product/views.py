from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Plan
from .serializers import PlanSerializer

class PlanListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        plans = Plan.objects.all().order_by('price')
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)
