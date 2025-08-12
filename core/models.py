from django.db import models
from django.contrib.auth.models import User
import os
import uuid
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    real_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    document = models.FileField(upload_to='documents/', blank=True, null=True)

    # Profile Page Extra Fields
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    skills = models.CharField(max_length=255, blank=True, null=True)
    education = models.CharField(max_length=255, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)
    relationship_status = models.CharField(max_length=30, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    certificate = models.FileField(upload_to='certificates/', blank=True, null=True)


    def __str__(self):
        return self.user.username

# ---------------- SIGNALS ---------------- #

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()  # ✅ NOT instance.userprofile





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
    CATEGORY_CHOICES = [
        ('ai', 'Artificial Intelligence'),
        ('ml', 'Machine Learning'),
        ('cs', 'Computer Science'),
        ('bio', 'Biology'),
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('math', 'Mathematics'),
        ('engineering', 'Engineering'),
        ('medicine', 'Medicine'),
        ('psychology', 'Psychology'),
    ]

    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    email = models.EmailField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    abstract = models.TextField()
    keywords = models.CharField(max_length=255, blank=True)
    pdf = models.FileField(upload_to='research_papers/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



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

    class Meta:
        unique_together = ('meeting', 'user')  # 🚫 Prevent duplicate requests

    def __str__(self):
        return f"{self.user.username} requesting {self.meeting.meeting_id}"


class ApprovedParticipant(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('meeting', 'user')  # ✅ Ensure one-time approval per session

    def __str__(self):
        return f"{self.user.username} approved for {self.meeting.meeting_id}"


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




