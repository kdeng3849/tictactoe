"""tictactoe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
