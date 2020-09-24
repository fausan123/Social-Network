
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:id>", views.profile_view, name="profile"),
    path("following", views.following_view, name="following"),

    # API Routes
    path("posts", views.edit_post, name="editpost"),
    path("post/<int:post_id>", views.get_or_like_post, name="post"),
    path("followuser/<int:user_id>", views.follow_user, name="follow"),
    path("editbio", views.edit_bio, name="editbio")
]
