from django.shortcuts import render
from .urls import infonowRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.core.paginator import Paginator
# Create your views here.

#Article API
@infonowRouter.route
class CreateArticle(APIView):
    def post(self, request):
        data        = request.data
        ser_data    = ArticleSerializer(data=data)
        if ser_data.is_valid(raise_exception=True):
            saved_obj = ser_data.save()
            return Response(ArticleSerializer(saved_obj).data, status=200)

@infonowRouter.route
class FetchArticle(APIView):
    # path = "info/fetcharticle/<str:query>/"
    def get(self, request):
        data    = request.data
        id      = data.get('id')
        print(request.GET.get('lang'),request.GET.get('page'),request.GET.get('id'),request.GET.get('category'),)
        page = int(request.GET.get('page',1))
        lang = request.GET.get('lang','English')
        cat  = request.GET.get('category',"")
        size = request.GET.get('size',2)
        print(cat, lang, page)
        if id is not None:
            try:
                article = Article.objects.get(id=id)
            except:
                return Response("Invalid article id", status=400)
            else:
                return Response(ArticleSerializer(article).data, status=200)
        filter = {
            "language__name":lang,
        }
        response = {}
        articles = Article.objects.filter(**filter).order_by('id')
        count    = Article.objects.filter(**filter).count()
        all_count= Article.objects.count()
        # print(size*page, size*(page-1), count)
        # if size*(page-1)>count:
        #     return Response('All the items are not fetched for this selection', status=400)
        print(page, (size*(page-1))%count) 
        paginator           = Paginator(articles, size)
        articles            = paginator.get_page((size*(page))%count)
        response["data"]    = ArticleFetchSerializer(articles, many=True).data
        response["count"]   = count
        response["all_count"]   = all_count
        return Response(response, status=200)

@infonowRouter.route
class UpdateArticle(APIView):
    def post(self, request):
        data        = request.data
        id          = data.get('id')
        try:
            article = Article.objects.get(id=id)
        except:
            return Response('Invalid Article',status=400)
        else:
            ser_data    = ArticleSerializer(article,data=data, partial=True)
            if ser_data.is_valid(raise_exception=True):
                saved_obj = ser_data.save()
                return Response(ArticleSerializer(saved_obj).data, status=200)

@infonowRouter.route
class DeleteArticle(APIView):
    def post(self, request):
        data        = request.data
        id          = data.get('id')
        try:
            article = Article.objects.get(id=id).delete()
        except:
            return Response('Invalid Article',status=400)
        else:
            return Response('Article deleted', status=200)
    
#Source API
@infonowRouter.route
class CreateSource(APIView):
    def post(self, request):
        data        = request.data
        ser_data    = SourceSerializer(data=data)
        if ser_data.is_valid(raise_exception=True):
            saved_obj = ser_data.save()
            return Response(SourceSerializer(saved_obj).data, status=200)

@infonowRouter.route
class FetchSource(APIView):
    def post(self, request):
        data    = request.data
        id      = data.get('id')
        if id is not None:
            try:
                source = Source.objects.get(id=id)
            except:
                return Response("Invalid source id", status=400)
            else:
                return Response(SourceSerializer(source).data, status=200)
        sources = Source.objects.all()
        return Response(SourceSerializer(sources, many=True).data, status=200)

@infonowRouter.route
class UpdateSource(APIView):
    def post(self, request):
        data        = request.data
        id          = data.get('id')
        try:
            source = Source.objects.get(id=id)
        except:
            return Response('Invalid Source',status=400)
        else:
            ser_data    = SourceSerializer(source, data=data, partial=True)
            if ser_data.is_valid(raise_exception=True):
                saved_obj = ser_data.save()
                return Response(SourceSerializer(saved_obj).data, status=200)

@infonowRouter.route
class DeleteSource(APIView):
    def post(self, request):
        data        = request.data
        id          = data.get('id')
        try:
            source = Source.objects.get(id=id).delete()
        except:
            return Response('Invalid Language',status=400)
        else:
            return Response('Language deleted', status=200)

#Language API
@infonowRouter.route
class CreateLanguage(APIView):
    def post(self, request):
        data        = request.data
        ser_data    = LanguageSerializer(data=data)
        if ser_data.is_valid(raise_exception=True):
            saved_obj = ser_data.save()
            return Response(LanguageSerializer(saved_obj).data, status=200)

@infonowRouter.route
class FetchLanguage(APIView):
    def post(self, request):
        data    = request.data
        id      = data.get('id')
        if id is not None:
            try:
                lang = Language.objects.get(id=id)
            except:
                return Response("Invalid Language id", status=400)
            else:
                return Response(LanguageSerializer(source).data, status=200)
        langs = Language.objects.all()
        return Response(LanguageSerializer(langs, many=True).data, status=200)

@infonowRouter.route
class UpdateLanguage(APIView):
    def post(self, request):
        data        = request.data
        id          = data.get('id')
        try:
            lang = Language.objects.get(id=id)
        except:
            return Response('Invalid Language',status=400)
        else:
            ser_data    = LanguageSerializer(lang, data=data, partial=True)
            if ser_data.is_valid(raise_exception=True):
                saved_obj = ser_data.save()
                return Response(LanguageSerializer(saved_obj).data, status=200)

@infonowRouter.route
class DeleteLanguage(APIView):
    def post(self, request):
        data        = request.data
        id          = data.get('id')
        try:
            lang = Language.objects.get(id=id).delete()
        except:
            return Response('Invalid Language',status=400)
        else:
            return Response('Language deleted', status=200)

#Category API
@infonowRouter.route
class CreateCategory(APIView):
    def post(self, request):
        data        = request.data
        ser_data    = CategorySerializer(data=data)
        if ser_data.is_valid(raise_exception=True):
            saved_obj = ser_data.save()
            return Response(CategorySerializer(saved_obj).data, status=200)

@infonowRouter.route
class FetchCategory(APIView):
    def post(self, request):
        data    = request.data
        id      = data.get('id')
        if id is not None:
            try:
                cat = Category.objects.get(id=id)
            except:
                return Response("Invalid Category id", status=400)
            else:
                return Response(CategorySerializer(cat).data, status=200)
        cats = Category.objects.all()
        return Response(CategorySerializer(cats, many=True).data, status=200)

@infonowRouter.route
class UpdateCategory(APIView):
    def post(self, request):
        data        = request.data
        id          = data.get('id')
        try:
            cat = Category.objects.get(id=id)
        except:
            return Response('Invalid Category',status=400)
        else:
            ser_data    = CategorySerializer(cat, data=data, partial=True)
            if ser_data.is_valid(raise_exception=True):
                saved_obj = ser_data.save()
                return Response(CategorySerializer(saved_obj).data, status=200)

@infonowRouter.route
class DeleteCategory(APIView):
    def post(self, request):
        data        = request.data
        id          = data.get('id')
        try:
            cat = Category.objects.get(id=id).delete()
        except:
            return Response('Invalid Category',status=400)
        else:
            return Response('Category deleted', status=200)


