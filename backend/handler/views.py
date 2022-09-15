from http.client import HTTPResponse
from json import JSONDecodeError
from django.shortcuts import Http404
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from .models import *


class LatestProductList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        # return JsonResponse(serializer.data,safe=False)
        return Response(serializer.data)


class ProductDetails(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except:
            return Http404

    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CategoryDetails(APIView):
    def get_object(self, category_slug):
        try:
            return Product.objects.filter(category__slug=category_slug)
        except:
            return Http404

    def get(self, request, category_slug, format=None):
        products = self.get_object(category_slug)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


def auto(request):
    if 'query' in request.GET:
        qs1 = Product.objects.filter(
            name__istartswith=request.GET.get('query'))
        qs2 = Product.objects.filter(name__icontains=request.GET.get(
            'query')).exclude(name__istartswith=request.GET.get('query'))
        titles = list()
        for product in qs1:
            titles.append(product.name)
        for product in qs2:
            titles.append(product.name)
        # print(titles)
        return JsonResponse(titles, safe=False)


@api_view(['POST'])
def search(request):
    print(request.data)
    query = request.data.get('query', '')
    print(query)
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})
