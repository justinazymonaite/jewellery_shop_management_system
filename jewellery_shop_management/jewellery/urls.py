from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.categories, name='categories'),
    # path('category/<int:category_id>/', views.category, name='category'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product'),
    path('my_orders/', views.UserOrderListView.as_view(), name='user_orders'),
]