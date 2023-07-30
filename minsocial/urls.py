from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("terms", views.terms, name="terms"),
    path("newpost", views.newPost, name="newPost"),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:group_id>/join/', views.join_group, name='join_group'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('group_post/<int:group_id>/', views.group_newPost, name='group_newPost'),
    path('group_addComment/<int:post_id>/', views.group_addComment, name='group_addComment'),
    path("post_content/<int:post_id>", views.post_content, name="post_content"),
    path("post_image/<int:post_id>", views.post_image, name="post_image"),
    path('profile_pic/<int:user_id/', views.profile_pic, name="profile_pic"),
    path('profile/<int:user_id>/', views.profile, name="profile"),
    path('edit_profile/<int:user_id>/', views.edit_profile, name="edit_profile"),
    path('addComment/<int:post_id>/', views.addComment, name='addComment'),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("like_count", views.like_count, name="like_count"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("remove_like/<int:post_id>", views.remove_like, name="remove_like"),
    path("add_like/<int:post_id>", views.add_like, name="add_like"),
    path("remove_shock/<int:post_id>", views.remove_shock, name="remove_shock"),
    path("add_shock/<int:post_id>", views.add_shock, name="add_shock"),
    path("remove_love/<int:post_id>", views.remove_love, name="remove_love"),
    path("add_love/<int:post_id>", views.add_love, name="add_love"),
    path("remove_haha/<int:post_id>", views.remove_haha, name="remove_haha"),
    path("add_haha/<int:post_id>", views.add_haha, name="add_haha"),
    path("remove_sad/<int:post_id>", views.remove_sad, name="remove_sad"),
    path("add_sad/<int:post_id>", views.add_sad, name="add_sad"),
    path("group_add_or_remove_reaction/<int:post_id>/<str:reaction_type>/", views.group_add_or_remove_reaction, name="group_add_or_remove_reaction"),
    path("login", views.login_view, name="network_login"),
    path("logout", views.logout_view, name="network_logout"),
    path("register", views.register, name="network_register"),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),



]
