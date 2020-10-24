from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following_index, name="following_index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    re_path(r"^(?P<username>[^/]+)$", views.user_profile, name="user_profile"),
    # API Routes
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("likes/<int:post_id>/<int:user_id>", views.likes, name="likes"),
]
