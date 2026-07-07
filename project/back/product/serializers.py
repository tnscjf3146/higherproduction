from rest_framework import serializers
from .models import Plan, PlanType, Recommend, Operation, Production, Item

class PlanTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanType
        fields = ['id', 'name']

class RecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommend
        fields = ['id', 'name']

class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['id', 'name']

class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Production
        fields = ['id', 'name']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name']

class PlanSerializer(serializers.ModelSerializer):
    plan_type_name = serializers.CharField(source='plan_type.name', read_only=True)
    recommends = RecommendSerializer(many=True, read_only=True)
    operations = OperationSerializer(many=True, read_only=True)
    productions = ProductionSerializer(many=True, read_only=True)
    items = ItemSerializer(many=True, read_only=True)

    recommend_ids = serializers.PrimaryKeyRelatedField(
        queryset=Recommend.objects.all(), source='recommends', many=True, write_only=True, required=False
    )
    operation_ids = serializers.PrimaryKeyRelatedField(
        queryset=Operation.objects.all(), source='operations', many=True, write_only=True, required=False
    )
    production_ids = serializers.PrimaryKeyRelatedField(
        queryset=Production.objects.all(), source='productions', many=True, write_only=True, required=False
    )
    item_ids = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), source='items', many=True, write_only=True, required=False
    )

    class Meta:
        model = Plan
        fields = [
            'id', 'plan_type', 'plan_type_name', 'name', 'subname', 'price',
            'recommends', 'operations', 'productions', 'items',
            'recommend_ids', 'operation_ids', 'production_ids', 'item_ids',
            'created_at', 'updated_at'
        ]
