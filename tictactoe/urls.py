from django.contrib import admin
from django.urls import path, include
from ttt import views as ttt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ttt/', include('ttt.urls')),
    path('adduser', ttt_views.add_user, name='adduser'),
    path('verify', ttt_views.verify, name='verify'),
    path('login', ttt_views.login_user, name='login'),
    path('logout', ttt_views.logout_user, name='logout'),
    path('listgames', ttt_views.list_games, name='listgames'),
    path('getgame', ttt_views.get_game, name='getgame'),
    path('getscore', ttt_views.get_score, name='getscore'),
]
