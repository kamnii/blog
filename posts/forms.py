from django import forms


class PostCreateForm(forms.Form):
    title = forms.CharField(min_length=10, max_length=150)
    description = forms.CharField(widget=forms.Textarea)


class CommentCreateForm(forms.Form):
    text = forms.CharField(max_length=80)
