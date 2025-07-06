from django.db import models
from django.contrib.auth.models import User
import os
import uuid


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    real_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    profession = models.CharField(max_length=100)
    document = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.user.username
    

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:30]

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.text[:20]}"   


class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.FileField(upload_to='stories/')  # image or video
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Story at {self.created_at}" 

    def is_video(self):
        name, extension = os.path.splitext(self.media.name)
        return extension.lower() == '.mp4'   




class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')




class Reel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.FileField(upload_to='reels/videos/')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Reel"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reel = models.ForeignKey(Reel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ReelComment(models.Model):  # 👈 new name
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reel = models.ForeignKey(Reel, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)




class ResearchPaper(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    pdf_file = models.FileField(upload_to='research_papers/')
    allow_download = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ResearchComment(models.Model):
    paper = models.ForeignKey(ResearchPaper, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ResearchLike(models.Model):
    paper = models.ForeignKey(ResearchPaper, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)



# ───────────────────────────────────────────────
# 🧠 1. Job Posting Model
# ───────────────────────────────────────────────
class Job(models.Model):
    title = models.CharField("Job Title", max_length=255)
    company = models.CharField("Company Name", max_length=255)
    location = models.CharField("Location", max_length=255)
    salary = models.CharField("Salary (optional)", max_length=100, blank=True, null=True)
    description = models.TextField("Job Description")
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    posted_at = models.DateTimeField("Posted On", auto_now_add=True)

    class Meta:
        ordering = ['-posted_at']
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self):
        return f"{self.title} at {self.company}"


# ───────────────────────────────────────────────
# 📥 2. Job Application Model
# ───────────────────────────────────────────────
class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    resume = models.FileField("Resume (PDF only)", upload_to='resumes/')
    applied_at = models.DateTimeField("Applied On", auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')  # Optional: Prevent duplicate applications
        ordering = ['-applied_at']
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"

    def __str__(self):
        return f"{self.applicant.username} applied to {self.job.title}"

# models.py



class Meeting(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    meeting_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Meeting by {self.host.username} - {self.meeting_id}"


class JoinRequest(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} requesting {self.meeting.meeting_id}"


class Recording(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='recordings/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recording for {self.meeting.meeting_id}"




# 🟩 1. Group model
class Group(models.Model):
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('hidden', 'Hidden'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    cover_photo = models.ImageField(upload_to='group_covers/', blank=True, null=True)

    def __str__(self):
        return self.name


# 🟩 2. Group Member
class GroupMember(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"


# 🟩 3. Group Post
class GroupPost(models.Model):
    FILE_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('pdf', 'PDF'),
        ('doc', 'Document'),
        ('other', 'Other'),
    ]

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    media_file = models.FileField(upload_to='group_media/', blank=True, null=True)
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return self.media_file.name.split('/')[-1]

    def __str__(self):
        return f"Post by {self.author.username} in {self.group.name}"




