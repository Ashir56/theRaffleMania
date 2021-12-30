from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('register/', views.BuyerAPI.as_view()),
    path('card/', views.BuyerCardAPI.as_view({'post': 'post', 'get': 'get', 'delete': 'destroy', 'patch': 'patch'})),
    path('cart/', views.BuyerCartAPI.as_view({'post': 'post', 'delete': 'delete'})),
    path('email/', views.SendEmailAPI.as_view()),
    path('billing/', views.BillingAPI.as_view()),
    path('refund/', views.RefundAPI.as_view())
]

#
