from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.SellerAPI.as_view({'post': 'post', 'get': 'get', 'delete': 'destroy', 'patch': 'patch'})),
]
