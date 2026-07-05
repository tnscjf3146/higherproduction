from rest_framework import serializers
from .models import Plan, Recommend, Operation, Production, Item

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
    recommends = RecommendSerializer(many=True, read_only=True)
    operations = OperationSerializer(many=True, read_only=True)
    productions = ProductionSerializer(many=True, read_only=True)
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Plan
        fields = [
            'id', 'plan_type', 'name', 'subname', 'price',
            'recommends', 'operations', 'productions', 'items',
            'created_at', 'updated_at'
        ]
