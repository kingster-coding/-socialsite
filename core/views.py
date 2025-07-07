from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import ResearchPaperForm
from .models import ResearchPaper
import json
import uuid
import os

from .models import (
    Profile, Post, Comment, Story, Reel,
    ResearchPaper,
    Job, JobApplication, Meeting, JoinRequest, Recording,
    Group, GroupMember, GroupPost,

)

from .forms import (
    PostForm, CommentForm, StoryForm, ReelForm,
    ResearchPaperForm,
    JobForm, JobApplicationForm, 
)



def landing(request):
    return render(request, 'landing.html')



# views.py

# views.py

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').lower()
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        real_name = request.POST.get('real_name')
        phone = request.POST.get('phone')
        profession = request.POST.get('profession')
        document = request.FILES.get('document')

        if not all([email, pass1, pass2, real_name, phone, profession, document]):
            messages.error(request, "Please fill out all fields and upload the document.")
            return render(request, 'register.html')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'register.html')

        # ✅ Create user
        user = User.objects.create_user(username=email, email=email, password=pass1)
        
        # ✅ Update auto-created profile fields
        profile = user.profile
        profile.real_name = real_name
        profile.phone = phone
        profile.profession = profession
        profile.document = document
        profile.save()

        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email'].lower()
        password = request.POST['password']

        # Authenticate using username=email because humne username=email rakha hai
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # home page url name
        else:
            messages.error(request, "Invalid email or password")
            return render(request, 'login.html')

    return render(request, 'login.html')



# 🏠 Home View (Post + Feed)
@login_required
def home_view(request):
    from .models import Post, Story
    from .forms import PostForm, StoryForm

    posts = Post.objects.all().order_by('-created_at')
    stories = Story.objects.all().order_by('-created_at')[:20]

    post_form = PostForm()
    story_form = StoryForm()

    if request.method == 'POST':
        if 'post_submit' in request.POST:
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('home')
        elif 'story_submit' in request.POST:
            story_form = StoryForm(request.POST, request.FILES)
            if story_form.is_valid():
                story = story_form.save(commit=False)
                story.user = request.user
                story.save()
                return redirect('home')

    context = {
        'posts': posts,
        'stories': stories,
        'post_form': post_form,
        'story_form': story_form,
    }
    return render(request, 'home.html', context)

# 💬 Comment View (AJAX-style in page)
@login_required
def comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
    return redirect('home')


@login_required
def story_upload_view(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect('home')  # ya jis page pe stories dikhani ho
    else:
        form = StoryForm()

    stories = Story.objects.all().order_by('-created_at')[:20]  # recent stories

    return render(request, 'story_upload.html', {'form': form, 'stories': stories})




@login_required
def reels_view(request):
    if request.method == 'POST':
        video = request.FILES.get('video')
        caption = request.POST.get('caption')
        if video:
            Reel.objects.create(user=request.user, video=video, caption=caption)
            return redirect('reels')  # same page reload after upload

    reels = Reel.objects.all().order_by('-created_at')
    return render(request, 'reels.html', {'reels': reels})



@login_required


# ✅ Publish Research Paper (via AJAX)
@login_required
def publish_research_paper(request):
    if request.method == 'POST':
        form = ResearchPaperForm(request.POST, request.FILES)
        if form.is_valid():
            research = form.save(commit=False)
            research.user = request.user
            research.save()
            return JsonResponse({
                'status': 'success',
                'id': research.id,
                'title': research.title,
                'authors': research.authors,
                'category': research.category,
                'keywords': research.keywords,
                'abstract': research.abstract,
                'pdf_url': research.pdf.url,
                'likes': research.likes,
                'views': research.views,
            })
        else:
            print("❌ Form Errors:", form.errors)  # ⚠️ Print error in terminal
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    else:
        form = ResearchPaperForm()
    return render(request, 'research.html', {'form': form})



# ✅ Increment View Count
@csrf_exempt
def increment_view(request, id):
    if request.method == 'POST':
        try:
            paper = ResearchPaper.objects.get(id=id)
            paper.views += 1
            paper.save()
            return JsonResponse({'views': paper.views})
        except ResearchPaper.DoesNotExist:
            return JsonResponse({'error': 'Paper not found'}, status=404)


# ✅ Like Research Paper
@csrf_exempt
def like_paper(request, id):
    if request.method == 'POST':
        try:
            paper = ResearchPaper.objects.get(id=id)
            paper.likes += 1
            paper.save()
            return JsonResponse({'likes': paper.likes})
        except ResearchPaper.DoesNotExist:
            return JsonResponse({'error': 'Paper not found'}, status=404)


# ✅ Comment on Research Paper
@csrf_exempt
def comment_paper(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            comment_text = data.get('comment')
            # 👇 If you have a comment model, save it like this:
            # ResearchComment.objects.create(paper_id=id, user=request.user, comment=comment_text)

            print(f'Comment added on paper {id}: {comment_text}')  # For debugging
            return JsonResponse({'status': 'Comment added'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)




# ───────────────────────────────────────────────
# 🔥 1. Job Page (Post + List + Apply)
# ───────────────────────────────────────────────
@login_required
def jobs(request):
    job_form = JobForm()
    application_form = JobApplicationForm()

    # ───── Job Post Form ─────
    if request.method == 'POST' and 'post_job' in request.POST:
        job_form = JobForm(request.POST)
        if job_form.is_valid():
            job = job_form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, "✅ Job posted successfully!")
            return redirect('jobs')

    # ───── Apply Job Form ─────
    elif request.method == 'POST' and 'apply_job' in request.POST:
        job_id = request.POST.get('job_id')
        job = get_object_or_404(Job, id=job_id)
        application_form = JobApplicationForm(request.POST, request.FILES)

        already_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()
        if already_applied:
            messages.warning(request, f"⚠️ You have already applied to {job.title}.")
            return redirect('jobs')

        if application_form.is_valid():
            application = application_form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, f"✅ You applied to {job.title}.")
            return redirect('jobs')

    # ───── All Jobs ─────
    jobs = Job.objects.all().order_by('-posted_at')

    # ───── Recruiter Applications ─────
    my_jobs = Job.objects.filter(posted_by=request.user)
    my_applications = JobApplication.objects.filter(job__in=my_jobs)

    return render(request, 'jobs.html', {
        'job_form': job_form,
        'application_form': application_form,
        'jobs': jobs,
        'my_applications': my_applications
    })



# ✅ Central Go Live Page (no meeting_id required)
@login_required
def go_live_page(request):
    return render(request, 'go_live.html')


# ✅ Create a new meeting and return meeting_id (AJAX)
@login_required
def create_meeting(request):
    meeting = Meeting.objects.create(host=request.user)
    return JsonResponse({'meeting_id': str(meeting.meeting_id)})


# ✅ Redirect to UUID-based live room after creation (optional use)
@login_required
def live_redirect(request):
    meeting = Meeting.objects.create(host=request.user)
    return redirect('go_live_room', meeting_id=meeting.meeting_id)


# ✅ UUID-based Go Live Room (optional if not using separate room views)
@login_required
def go_live_room(request, meeting_id):
    meeting = get_object_or_404(Meeting, meeting_id=meeting_id)
    return render(request, 'go_live.html', {
        'meeting_id': meeting_id,
        'host': meeting.host,
    })


# ✅ Join request to host
@login_required
def request_to_join(request):
    if request.method == 'POST':
        meeting_id = request.POST.get('meeting_id')
        meeting = get_object_or_404(Meeting, meeting_id=meeting_id)

        _, created = JoinRequest.objects.get_or_create(
            meeting=meeting,
            user=request.user
        )
        return JsonResponse({'status': 'request_sent'})

    return JsonResponse({'error': 'Invalid request'}, status=400)


# ✅ Host approves a user
@login_required
def approve_user(request):
    if request.method == 'POST':
        meeting_id = request.POST.get('meeting_id')
        user_id = request.POST.get('user_id')
        meeting = get_object_or_404(Meeting, meeting_id=meeting_id)

        if request.user != meeting.host:
            return HttpResponseForbidden('Only host can approve users.')

        jr = get_object_or_404(JoinRequest, meeting=meeting, user__id=user_id)
        jr.approved = True
        jr.save()

        return JsonResponse({'status': 'approved'})

    return JsonResponse({'error': 'Invalid request'}, status=400)


# ✅ Upload recorded video file
@csrf_exempt
def upload_recording(request):
    if request.method == 'POST':
        meeting_id = request.POST.get('meeting_id')
        video = request.FILES.get('video')

        if not meeting_id or not video:
            return JsonResponse({'status': 'missing_data'}, status=400)

        meeting = get_object_or_404(Meeting, meeting_id=meeting_id)
        Recording.objects.create(meeting=meeting, video_file=video)

        return JsonResponse({'status': 'saved'})

    return JsonResponse({'error': 'Invalid request'}, status=400)




@login_required
def messages_view(request):
    return render(request, 'messages.html')




# 🔸 Show All Groups
@login_required
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'group.html', {'groups': groups})


# 🔸 Create a New Group
@login_required
def group_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        privacy = request.POST.get('privacy')
        cover = request.FILES.get('cover_photo')

        group = Group.objects.create(
            name=name,
            description=description,
            privacy=privacy,
            created_by=request.user,
            cover_photo=cover
        )

        # Automatically add creator as admin member
        GroupMember.objects.create(
            user=request.user,
            group=group,
            is_admin=True,
            status='approved'
        )

        return redirect('group_list')


# 🔸 Show Group Detail Page
@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    posts = GroupPost.objects.filter(group=group).order_by('-created_at')
    members = GroupMember.objects.filter(group=group, status='approved')

    is_member = GroupMember.objects.filter(
        group=group,
        user=request.user,
        status='approved'
    ).exists()

    return render(request, 'group.html', {
        'group': group,
        'posts': posts,
        'members': members,
        'is_member': is_member
    })


# 🔸 Join a Group
@login_required
def group_join(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    GroupMember.objects.get_or_create(
        user=request.user,
        group=group,
        defaults={'status': 'approved'}
    )
    return redirect('group_detail', group_id=group.id)


# 🔸 Leave a Group
@login_required
def group_leave(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    GroupMember.objects.filter(user=request.user, group=group).delete()
    return redirect('group_list')


# 🔸 Post in Group with File Upload
@login_required
def group_post_create(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if not GroupMember.objects.filter(group=group, user=request.user, status='approved').exists():
        return HttpResponseForbidden("You are not a member of this group.")

    if request.method == 'POST':
        content = request.POST.get('content')
        media = request.FILES.get('media_file')
        file_type = 'other'

        if media:
            if media.content_type.startswith('image'):
                file_type = 'image'
            elif media.content_type.startswith('video'):
                file_type = 'video'
            elif media.name.endswith('.pdf'):
                file_type = 'pdf'
            elif media.name.endswith('.doc') or media.name.endswith('.docx'):
                file_type = 'doc'

        GroupPost.objects.create(
            group=group,
            author=request.user,
            content=content,
            media_file=media,
            file_type=file_type
        )

    return redirect('group_detail', group_id=group.id)



@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    context = {
        'profile_user': user,
        'profile': profile
    }
    return render(request, 'profile.html', context)



def research_view(request):
    return render(request, 'research.html')