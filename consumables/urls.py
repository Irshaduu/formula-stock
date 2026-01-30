from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('take/<int:item_id>/', views.take_item, name='take_item'),
    path('today/', views.today, name='today'),
    path('delete_consumption/<int:record_id>/', views.delete_consumption, name='delete_consumption'),
    path('stock/', views.stock_list, name='stock_list'),
    path('stock/low/', views.low_stock_list, name='low_stock_list'),
    path('stock/<int:item_id>/update/', views.update_stock, name='update_stock'),
    path('manage/categories/', views.manage_categories, name='manage_categories'),
    path('manage/categories/add/', views.add_category, name='add_category'),
    path('manage/categories/<int:category_id>/', views.category_detail, name='category_detail'),
    path('manage/categories/<int:category_id>/add_item/', views.add_item, name='add_item'),
    path('manage/items/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.profile, name='profile_view'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('manage/staff/', views.manage_staff, name='manage_staff'),
    path('manage/staff/add/', views.add_staff, name='add_staff'),
    path('manage/staff/<int:user_id>/edit/', views.edit_staff, name='edit_staff'),
    path('manage/staff/<int:user_id>/delete/', views.delete_staff, name='delete_staff'),
]