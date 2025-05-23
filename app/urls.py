
from django.urls import path
from app.views import index,product_detail,order_detail,comment_create,create_product,delete_product,edit_product

urlpatterns = [
    path('home/',index,name='index'),
    path('home/category/<int:category_id>/',index,name='products_of_category'),
    path('product/detail/<int:product_id>/',product_detail,name='product_detail'),
    path('product/create/',create_product,name='create_product'),
    path('product/delete/<int:pk>/',delete_product,name='delete_product'),
    path('product/edit/<int:pk>/',edit_product,name='edit_product'),
    # order 
    path('order/detail/<int:product_id>/',order_detail,name='order_detail'),
    path('comment/create/<int:pk>/',comment_create,name='comment_create'),
    
    
]
