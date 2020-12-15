
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('delivery/', views.delivery, name='delivery'),
    path('partner/', views.partner, name='partner'),
    path('category/<cat_slug>/', views.category, name='category'),
    path('category/<cat_slug>/<subcat_slug>/', views.subcategory, name='subcategory'),
    path('category/<cat_slug>/<subcat_slug>/<item_slug>/', views.item, name='item'),

    path('new_order/', views.new_order, name='new_order'),
    path('order/<order_code>/', views.order, name='order'),



]
