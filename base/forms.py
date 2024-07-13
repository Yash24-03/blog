from django import forms
from .models import Post, Tag, Category


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'cover', 'tags', 'categories']
        widgets = {
        # Ensure the 'id' matches your TinyMCE selector
        'content': forms.Textarea(attrs={'id': 'content'}),
        }
