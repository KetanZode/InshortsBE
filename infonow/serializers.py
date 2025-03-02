from rest_framework import serializers
from .models import *

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Article
        fields  = '__all__'

class ArticleFetchSerializer(serializers.ModelSerializer):
    image_b64 = serializers.CharField()
    class Meta:
        model   = Article
        fields  = '__all__'

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Source
        fields  = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Language
        fields  = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model   = Category
        fields  = '__all__'