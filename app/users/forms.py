from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSignupForm(UserCreationForm):
    """Форма регистрации пользователя."""
    class Meta:
        model = User
        fields = [
            'username', 'password1', 'password2',
            'email', 'country', 'full_name'
        ]

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['password1'].widget.attrs['placeholder'] = 'password'
        self.fields['password2'].widget.attrs['placeholder'] = 'repeat password'
        self.fields['full_name'].widget.attrs['placeholder'] = 'your name'
        self.fields['email'].widget.attrs['placeholder'] = 'email address'


class UserLoginForm(AuthenticationForm):
    """Форма аутентификации пользователя."""
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['password'].widget.attrs['placeholder'] = 'password'


class UserPasswordChangeForm(PasswordChangeForm):
    """Форма смены пароля."""
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['placeholder'] = 'old password'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'new password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'repeat new password'


class ProfileDataForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'description', 'full_name', 'email', 'country')

    def __init__(self, *args, **kwargs):
        super(ProfileDataForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'profile_info_username display'
        self.fields['description'].widget.attrs['class'] = 'profile_info_description display'
        self.fields['full_name'].widget.attrs['class'] = 'profile_addinfo_right display'
        self.fields['email'].widget.attrs['class'] = 'profile_addinfo_right display'
        self.fields['country'].widget.attrs['class'] = 'profile_addinfo_right display'


class ProfileImageForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('image', )

    def __init__(self, *args, **kwargs):
        super(ProfileImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['id'] = 'fileInput'
        self.fields['image'].widget.attrs['hidden'] = True
        self.fields['image'].label = False
