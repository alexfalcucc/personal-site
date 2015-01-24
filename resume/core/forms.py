# coding: utf-8
from django import forms
from resume.core.models import Article, Contact


class ArticleForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'P'}))
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'required'}),
        max_length=255)
    picture = forms.FileField(widget=forms.FileInput(
        attrs={'class': 'required'}),
        max_length=255)
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'required'}),
        max_length=10000000)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'required'}),
                           max_length=255,
                           required=False,
                           help_text='Use spaços para separar suas tags.')
    url_download = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'required'}),
        max_length=255)
    url_preview = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'required'}),
        max_length=255)
    url_github = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'required'}),
        max_length=255)

    class Meta:
        model = Article
        fields = ['title', 'content', 'picture', 'tags',
                  'url_download', 'url_preview', 'url_github', 'status']


class ContactForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Nome', 'required': 'required'}), max_length=100)

    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            'placeholder': 'Email', 'required': 'required'}), max_length=100)

    message = forms.CharField(widget=forms.Textarea(
        attrs={
            'placeholder': 'Mensagem', 'rows': '3', 'required': 'required'}),
        max_length=40000)

    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
