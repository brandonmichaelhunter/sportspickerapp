from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('game/<int:game_id>/history/', views.get_game_history, name='game_history'),
    path('game/<int:game_id>/pick/', views.make_pick, name='make_pick'),
    path('chatbot/', views.chatbot_response, name='chatbot'),
]