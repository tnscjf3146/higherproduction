from rest_framework import serializers
from .models import Work, MainCategory, SubCategory, BrandClient, Project, Inquiry

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
    sub_category_name = serializers.CharField(source='sub_category.name', read_only=True)
    
    class Meta:
        model = Work
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    works = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'main_category', 'order', 'is_vertical', 'is_instagram', 'works']

    def get_works(self, obj):
        works = obj.works.filter(is_visible=True).order_by('-created_at')
        return WorkSerializer(works, many=True).data

class MainCategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = MainCategory
        fields = ['id', 'name', 'order', 'sub_categories']

class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'
