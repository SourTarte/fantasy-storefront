from . import views
from django.urls import path

urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path('debug/', views.DebugList.as_view(), name='debug_list'),
    path('<str:product_name> <int:product_id>/', views.product_page, name='product_page'),
    path('<str:product_name> <int:product_id>/delete_comment/<int:review_id>', views.review_delete,
         name='review_delete'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
]