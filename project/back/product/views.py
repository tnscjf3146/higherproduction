from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Plan, PlanType, Recommend, Operation, Production, Item
from .serializers import PlanSerializer, PlanTypeSerializer, RecommendSerializer, OperationSerializer, ProductionSerializer, ItemSerializer

class PlanTypeViewSet(viewsets.ModelViewSet):
    queryset = PlanType.objects.all()
    serializer_class = PlanTypeSerializer
    permission_classes = [AllowAny]

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all().order_by('price')
    serializer_class = PlanSerializer
    permission_classes = [AllowAny]

class RecommendViewSet(viewsets.ModelViewSet):
    queryset = Recommend.objects.all()
    serializer_class = RecommendSerializer
    permission_classes = [AllowAny]

class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    permission_classes = [AllowAny]

class ProductionViewSet(viewsets.ModelViewSet):
    queryset = Production.objects.all()
    serializer_class = ProductionSerializer
    permission_classes = [AllowAny]

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]
