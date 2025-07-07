from django import forms
from .models import Post, Comment, Story, Reel
from .models import ResearchPaper
from .models import Job, JobApplication



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
        fields = ['title', 'authors', 'email', 'category', 'abstract', 'keywords', 'pdf']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter research title'}),
            'authors': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter authors'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter email'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'abstract': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Write abstract', 'rows': 4}),
            'keywords': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter keywords'}),
            'pdf': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }

class ResearchPaperForm(forms.ModelForm):
    email = forms.EmailField()  # ✅ if 'email' is not in model
    class Meta:
        model = ResearchPaper
        fields = ['title', 'authors', 'email', 'category', 'keywords', 'abstract', 'pdf']



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

