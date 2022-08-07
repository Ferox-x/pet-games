from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm
)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSignupForm(UserCreationForm):
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
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['password'].widget.attrs['placeholder'] = 'password'


class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['placeholder'] = 'username'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'new password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'repeat new password'
