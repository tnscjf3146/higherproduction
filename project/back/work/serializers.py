from rest_framework import serializers
from .models import Work, Category, BrandClient, Project, Inquiry

class BrandClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandClient
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__'

class WorkSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Work
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    works = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'subtitle', 'order', 'is_vertical', 'works']

    def get_works(self, obj):
        # 공개된 작품만 역순 정렬해서 가져오기
        works = obj.works.filter(is_visible=True).order_by('-created_at')
        return WorkSerializer(works, many=True).data

class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'
