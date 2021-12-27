from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('products', views.ProductAPI, basename='Product-API')

urlpatterns = [
    path('', views.ProductAPI.as_view({'post': 'post', 'get': 'get', 'delete': 'destroy', 'patch': 'patch'})),
    path('wishlist/', views.WishlistAPI.as_view({'post': 'post', 'get': 'get', 'delete': 'delete'}),
         name='Wishlist-API'),
    path('reviews/', views.ReviewAPI.as_view()),
    path('productbyprice/', views.ProductByPrice.as_view()),
    path('productbyuser/', views.ProductByUser.as_view()),
    path('product-status/', views.ProductStatus.as_view()),
    path('ticket/', views.TicketAPI.as_view()),
    path('productratingfilter/', views.ProductRatingFilter.as_view()),
    path('order/', views.OrderAPI.as_view())
]
