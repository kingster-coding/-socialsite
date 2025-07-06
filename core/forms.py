from django import forms
from .models import Post, Comment, Story, Reel
from .models import ResearchPaper, ResearchComment
from .models import Job, JobApplication





class ResearchCommentForm(forms.ModelForm):
    class Meta:
        model = ResearchComment
        fields = ['content']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'document']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'What’s on your mind?', 'rows': 2}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']  # ✅ matches your Post-comment model

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['media', 'caption']

class ReelForm(forms.ModelForm):
    class Meta:
        model = Reel
        fields = ['video', 'caption']


class ResearchPaperForm(forms.ModelForm):
    class Meta:
        model = ResearchPaper
        fields = ['title', 'abstract', 'pdf_file', 'allow_download']

class ResearchCommentForm(forms.ModelForm):
    class Meta:
        model = ResearchComment
        fields = ['content']



# ───────────────────────────────────────────────
# 🧱 1. Job Post Form
# ───────────────────────────────────────────────
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'location', 'salary', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


# ───────────────────────────────────────────────
# 📎 2. Job Application Form (with Resume Upload)
# ───────────────────────────────────────────────
class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['resume']

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            if not resume.name.endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed.")
            if resume.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("File size should not exceed 5MB.")
        return resume



# core/forms.py

