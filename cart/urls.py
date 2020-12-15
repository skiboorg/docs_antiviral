
from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_cart, name='show_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('delete_from_main_cart/', views.delete_from_main_cart, name='delete_from_main_cart'),
    path('use_promo/', views.use_promo, name='use_promo'),
    path('sort_filter/', views.sort_filter, name='sort_filter'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('get_cart/', views.get_cart, name='get_cart'),
    path('delete_from_cart/', views.delete_from_cart, name='delete_from_cart'),
    path('wishlist_add/', views.wishlist_add, name='wishlist_add'),
    path('wishlist_delete/', views.wishlist_delete, name='wishlist_delete'),
    path('add_to_fav/', views.add_to_fav, name='add_to_fav'),




    # path('login/', views.login, name='login'),
    # path('logout/', views.logout_page, name='logout'),
    # path('profile/<nickname_req>', views.profile, name='profile'),
    # path('del_message/', views.del_message, name='del_message'),
    # path('bonus_pack/', views.bonus_pack, name='bonus_pack'),
    # path('about_us/', views.about_us, name='about_us'),
    # path('rules/', views.rules, name='rules'),
    # path('add_to_player_balance/', views.add_to_player_balance, name='add_to_player_balance'),
    # path('about_bonus_pack/', views.about_bonus_pack, name='about_bonus_pack'),




    # path('statistic/', views.statistic, name='statistic'),

]
