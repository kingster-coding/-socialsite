from django.urls import path
from . import views
from .views import jobs

urlpatterns = [
    # General
    path('', views.landing, name='landing'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('home/', views.home_view, name='home'),
    path('research/', views.research_papers_view, name='research_papers'),

    # Go Live redirect
    path('live/', views.live_redirect, name='live'),

    # Groups Section (group.html)
    path('groups/', views.group_list, name='group_list'),
    path('groups/create/', views.group_create, name='group_create'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/join/', views.group_join, name='group_join'),
    path('groups/<int:group_id>/leave/', views.group_leave, name='group_leave'),
    path('groups/<int:group_id>/post/', views.group_post_create, name='group_post_create'),

    # Messages / Reels / Jobs
    path('messages/', views.messages_view, name='messages'),
    path('reels/', views.reels_view, name='reels'),
    path('jobs/', jobs, name='jobs'),

    # Commenting
    path('comment/<int:post_id>/', views.comment_view, name='comment'),

    # Go Live Feature
    path('go_live/', views.create_meeting, name='create_meeting'),
    path('go_live/room/<uuid:meeting_id>/', views.go_live, name='go_live_room'),
    path('go_live/request_join/', views.request_to_join, name='request_to_join'),
    path('go_live/approve_user/', views.approve_user, name='approve_user'),
    path('go_live/upload_recording/', views.upload_recording, name='upload_recording'),


    path('profile/<str:username>/', views.profile, name='profile')


]
