from django import forms
from rango.models import Comment, Page, Category, UserProfile
from django.contrib.auth.models import User

class CategoryForm (forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta: 
            model = Category
            fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    tag = forms.CharField(widget=forms.HiddenInput(), initial="none")
    description = forms.CharField(widget=forms.Textarea, max_length=200, help_text="Please give a Description.")
    image = forms.ImageField(help_text="Upload a photo to help describing the page. (optional)", required=False)

    class Meta:
        model = Page
        #exclude = ('category', 'likes', 'tag')
        fields = ('title', 'url', 'description', 'image',)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        # If url is not empty and doesn't start with 'http://',
        # then prepend 'http://'.
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name','last_name')

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('level','website','picture')

class CommentForm(forms.ModelForm):
    input = forms.CharField(widget=forms.Textarea(attrs={
        'rows': '3',
    }))
    class Meta:
        model = Comment
        fields = ('input',)