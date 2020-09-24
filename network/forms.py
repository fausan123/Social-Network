from django import forms


class CreatePost(forms.Form):
    content = forms.CharField(
        label="", widget=forms.Textarea(attrs={'rows': 3, 'id': 'create'}))
