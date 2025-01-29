from rest_framework.response import Response
from handler.serializers import ProductSerializer
from handler.document import ProductDocument
from elasticsearch_dsl import Q
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.


def hi(request):
    return HttpResponse("Hi")


class ProductSearchView(APIView):
    def get(self, request, query):
        q = Q(
            'multi_match',
            query=query,
            fields=[
                'name',
                'description',
                'category',
            ],
            fuzziness='auto')
        search = ProductDocument.search().query(q)
        response = search.execute()

        qs = search.to_queryset()
        serializer = ProductSerializer(qs, many=True)

        return Response(serializer.data)
