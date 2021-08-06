from django.urls import path
from rango import views
from django.conf.urls import url, include

app_name='rango'

urlpatterns = [
    path('', views.index, name='index'), 
    path('about/', views.about, name='about'), 
    path('category/<slug:category_name_slug>/',views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('restricted/', views.restricted, name='restricted'),
    path('category/<slug:category_name_slug>/page/<page_title>/', views.show_page, name='show_page'),
    path('like/<int:pk>', views.like, name="like_page"),
    path('likecomment/<int:pk>', views.likecomment, name="like_comment"),
    path('optional_registration/', views.register_profile, name='register_profile'),
    path('counter/<int:pk>/', views.LinkRedirectView.as_view(), name='page-counter'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('registration_completed/', views.registration_completed, name='registration_completed'),
    path('bookmark_page/<id>/', views.bookmark_page, name='bookmark_page'), 

    url(r'^ajax/like_count/$', views.like_count, name='like_count'),
    url(r'^ajax/view_count/$', views.view_count, name='view_count'),
]