from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('',views.base,name="base"),
    path('home/',views.userhome,name="userhome"),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_product/',views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/',views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/',views.delete_product, name='delete_product'),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name="signup"),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]
