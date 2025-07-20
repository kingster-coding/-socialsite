from django.urls import path
from . import views

urlpatterns = [

    # 🌐 Auth and Landing
    path('', views.landing, name='landing'),
    path('register/', views.register, name='register'),
    path('send-otp/', views.send_otp_email, name='send_otp_email'),
    path('verify-otp/', views.verify_otp_email, name='verify_otp_email'),
    path('login/', views.user_login, name='login'),

    # 🏠 Home + Feed
    path('home/', views.home_view, name='home'),
    path('comment/<int:post_id>/', views.comment_view, name='comment'),
    path('stories/upload/', views.story_upload_view, name='story_upload'),

    # 🎥 Reels
    path('reels/', views.reels_view, name='reels'),

    # 📚 Research Papers
    path('research/', views.publish_research_paper, name='research'),
    path('research/increment-view/<int:id>/', views.increment_view, name='increment_view'),
    path('research/like/<int:id>/', views.like_paper, name='like_paper'),
    path('research/comment/<int:id>/', views.comment_paper, name='comment_paper'),

    # 💼 Jobs
    path('jobs/', views.jobs, name='jobs'),

    # 🎥 Go Live
# 🎥 Go Live
    path('go-live/', views.go_live_page, name='go_live'),  # only this renders HTML
    path('go-live/create/', views.create_meeting, name='create_meeting'),
    path('go-live/redirect/', views.live_redirect, name='live_redirect'),
    path('go-live/<uuid:meeting_id>/', views.go_live_room, name='go_live_room'),
    path('go-live/join-request/', views.request_to_join, name='request_to_join'),
    path('go-live/approve/', views.approve_user, name='approve_user'),
    path('go-live/upload-recording/', views.upload_recording, name='upload_recording'),


    # 💬 Messaging
    path('messages/', views.messages_view, name='messages'),

    # 👥 Groups

    path('groups/', views.group_list, name='groups'),  # ✅ changed name
    path('groups/create/', views.group_create, name='group_create'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/join/', views.group_join, name='group_join'),
    path('groups/<int:group_id>/leave/', views.group_leave, name='group_leave'),
    path('groups/<int:group_id>/post/', views.group_post_create, name='group_post_create'),

    # 👤 Profiles
    path('profile/<str:username>/', views.profile, name='profile'),
]
