from django.contrib import admin
from .models import (
    Profile, Follow, FriendRequest,
    Post, Comment, Story,
    Reel, Like, ReelComment,
    ResearchPaper,
    Job, JobApplication,
    Meeting, JoinRequest, Recording,
    Group, GroupMember, GroupPost
)

# Basic model registrations
admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(FriendRequest)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Story)
admin.site.register(Reel)
admin.site.register(Like)
admin.site.register(ReelComment)
admin.site.register(ResearchPaper)
admin.site.register(Job)
admin.site.register(JobApplication)
admin.site.register(Meeting)
admin.site.register(JoinRequest)
admin.site.register(Recording)

# Custom Admins

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'privacy', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('privacy', 'created_at')

@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'is_admin', 'is_moderator', 'status', 'joined_at')
    list_filter = ('status', 'is_admin', 'is_moderator')
    search_fields = ('user__username', 'group__name')

@admin.register(GroupPost)
class GroupPostAdmin(admin.ModelAdmin):
    list_display = ('group', 'author', 'file_type', 'created_at')
    list_filter = ('file_type', 'created_at')
    search_fields = ('content', 'author__username', 'group__name')


