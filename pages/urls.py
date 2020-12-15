
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
    # path('cats/', views.cats, name='cats'),
    # path('manuf/', views.manuf, name='manuf'),
    # path('itemm/', views.itemm, name='itemm'),
    # path('about/', views.about, name='about'),
    # path('contacts/', views.contacts, name='contacts'),
    # path('delivery/', views.delivery, name='delivery'),
    # path('catalog/', views.catalog, name='catalog'),
    # path('checkout/', views.checkout, name='checkout'),
    # path('manufacturers/', views.manufacturers, name='manufacturers'),
    # path('manufacturers/<slug>/', views.manufacturers_cat, name='manufacturers_cat'),
    # path('category/<category_slug>/', views.category, name='category'),
    # path('category/<category_slug>/<subcategory_slug>/', views.subcategory, name='subcategory'),
    # path('category/<category_slug>/<item_slug>', views.item_page, name='item_page'),
    # path('category/<category_slug>/<subcategory_slug>/<item_slug>', views.item_page, name='item_page'),
    # path('search/', views.search, name='search'),
    # path('sale/', views.sale, name='sale'),
    # path('login/', views.login, name='login'),
    # path('register/', views.register, name='register'),
    # path('manufactor/<manufactor_slug>', views.manufactor, name='manufactor'),

    # path('subcategory/<subcat_slug>/', views.subcategory, name='subcategory'),


]
