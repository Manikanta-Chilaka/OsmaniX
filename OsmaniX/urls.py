from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from accounts import views as account_views
from posts import views as post_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', account_views.login_view, name='login'),
    path('register/', account_views.register_view, name='register'),
    path('feed/', post_views.feed, name='feed'),
    path('create_post/', post_views.create_post, name='create_post'),
    path('logout/', account_views.logout_view, name='logout'),
    path('profile/', account_views.profile_view, name='profile'),
    path('profile/edit/', account_views.edit_profile_view, name='edit_profile'),
    path('search/', account_views.search_users, name='search'),
    path('profile/<str:username>/', account_views.profile_detail, name='profile_detail'),
    path('chat/', include('chat.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)