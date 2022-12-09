from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product'),
    path('my_orders/', views.OrderListView.as_view(), name='user_orders'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order'),
]