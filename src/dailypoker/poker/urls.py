
from django.conf.urls import url
from django.contrib import admin
from . import views as poker_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', poker_views.home, name="home"),
    url(r'^game/(?P<gid>\d+)$', poker_views.game, name="game"),
    url(r'^rank/?$', poker_views.rank, name="rank"),
    url(r'^search/?$', poker_views.search, name="join"),
    url(r'^create/?$', poker_views.create,name="create"),
    url(r'^login/', poker_views.login, name='login'),
    url(r'^logout/?$', auth_views.logout_then_login, name="logout"),
    url(r'^register/', poker_views.register, name='register'),
    # url(r'^test/', poker_views.test, name='test'),
    url(r'^registration_confirmation/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',
        poker_views.registration_confirmation, name='regconfirm'),

    url(r'^game/create/?$', poker_views.game_create,name='newgame'),
    url(r'^game/init/?$', poker_views.game_init),
    url(r'^game/update/?$', poker_views.game_update),
    url(r'^game/finish/(?P<pid>\d+)$', poker_views.game_finish, name='finish'),
    url(r'^game/init/(?P<gid>\d+)$', poker_views.game_init),

    url(r'^game/test/',poker_views.game_websocket_test),

    url(r'^help/',poker_views.help,name='help'),
]
