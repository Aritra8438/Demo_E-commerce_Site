from django.urls import path
from .views import *

urlpatterns = [
    path('latest-products/', LatestProductList.as_view()),
    path('products/search/', search),
    path('products/<slug:category_slug>/<slug:product_slug>/',
         ProductDetails.as_view()),
    path('products/<slug:category_slug>/',
         CategoryDetails.as_view()),
    path('auto/', auto),
]
