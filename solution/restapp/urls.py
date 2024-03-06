from django.urls import path
from . import views

urlpatterns = [
    path("ping", views.ping_view, name='ping'),
    path("countries/", views.CountryList.as_view(), name="countries"),
    path("countries/<str:alpha2>/", views.CountryOne.as_view(), name="countries"),
    path("auth/register", views.UserProfile.as_view(), name="register_user"),
    path("auth/sign-in", views.SignIn.as_view(), name="user_signin"),
    path("me/profile", views.MyProfile.as_view(), name="my_profile"),
    path("me/updatePassword", views.UpdatePassword.as_view(), name="update_password"),
    path("profiles/<str:login>", views.Profiles.as_view(), name="profiles"),
    path("friends", views.FriendList.as_view(), name="friends"),
    path("friends/add", views.AddFriend.as_view(), name="add_friend"),
    path("friends/remove", views.RemoveFriend.as_view(), name="add_friend"),
    path("posts/new", views.PostCreate.as_view(), name="add_post"),
    path("posts/<str:id>", views.PostOne.as_view(), name="see_post"),
    path("posts/<str:id>/like", views.PostLike.as_view(), name="like_post"),
    path("posts/<str:id>/dislike", views.PostDislike.as_view(), name="dislike_post"),
    path("posts/feed/<str:login>", views.PostList.as_view(), name="post_list"),

]
