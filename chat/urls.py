from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('start/<str:username>/', views.start_chat, name='start_chat'),
    path('messages/<int:conversation_id>/', views.fetch_messages, name='fetch_messages'),
    path('<int:conversation_id>/', views.chat_detail, name='chat_detail'),
    path('inbox-data/', views.inbox_data, name='inbox_data'),

]

