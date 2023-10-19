from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("player-career/<str:pk>", views.player_career, name="player-career"),
    path("team/<str:pk>", views.team, name="team"),
    path("create-team/", views.create_team, name="create-team"),
    path("game-history/", views.game_history, name="game-history"),
    path("view-game/<str:pk>", views.view_game, name="view-game"),
    path("schedule-game/", views.schedule_game, name="schedule-game"),  # long-term game
    path("create-organization/", views.create_organization, name="create-organization"),
    path("view-organization/<str:pk>", views.view_organization, name="view-organization"),
    path("view-leaderboard/", views.view_leaderboard, name="view-leaderboard"),

    path("search/entered_query=<str:entered_query>/query_type=<str:query_type>", views.search, name="search"),
    
    path("pitch-conditions", views.pitch_conditions, name="pitch-conditions"),

    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("unauthorized/", views.unauthorized, name="unauthorized"),
    path("reset/", views.reset, name="reset"),
]