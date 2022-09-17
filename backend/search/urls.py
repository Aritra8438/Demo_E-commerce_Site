from django.urls import path
from . import views

urlpatterns = [
    path('<str:query>/', views.ProductSearchView.as_view())
]
