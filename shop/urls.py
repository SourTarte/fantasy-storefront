from . import views
from django.urls import path

urlpatterns = [
    path('', views.ProductList.as_view(), name='home'),
    path('debug/', views.DebugList.as_view(), name='debug_list'),
    path('<str:product_name> <int:product_id>/', views.product_page, name='product_page'),
    path('<str:product_name> <int:product_id>/delete_comment/<int:review_id>', views.review_delete,
         name='review_delete'),
]