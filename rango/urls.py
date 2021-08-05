from django.urls import path
from rango import views

app_name='rango'

urlpatterns = [
    path('', views.index, name='index'), 
    path('about/', views.about, name='about'), 
    path('category/<slug:category_name_slug>/',views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    # path('register/', views.register, name='register'), 
    # path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    # path('logout/', views.user_logout, name='logout'),
    path('category/<slug:category_name_slug>/page/<page_title>/', views.show_page, name='show_page'),
    path('like/<int:pk>', views.like, name="like_page"),
    path('likecomment/<int:pk>', views.likecomment, name="like_comment"),
]