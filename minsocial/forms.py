from django import forms
from .models import LibraryDocument, Video, Group, User
import bleach

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']

class LibraryDocumentForm(forms.ModelForm):
    class Meta:
        model = LibraryDocument
        fields = ['title', 'category', 'file']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'file']



class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirmation = forms.CharField(widget=forms.PasswordInput)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirmation', 'profile_pic']

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return bleach.clean(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return bleach.clean(last_name)

    def clean_username(self):
        username = self.cleaned_data['username']
        return bleach.clean(username)

    def clean_email(self):
        email = self.cleaned_data['email']
        return bleach.clean(email)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirmation = cleaned_data.get('confirmation')

        # Check if the username already exists in the database
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")

        # Check if the email already exists in the database
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")

        if password and confirmation and password != confirmation:
            raise forms.ValidationError("Passwords must match.")

        return cleaned_data
