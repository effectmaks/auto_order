from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegistrationForm(UserCreationForm):
    is_superuser = forms.BooleanField(required=False, label='Superuser')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'is_superuser']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("User with this username already exists.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data:
            return cleaned_data
        is_superuser = cleaned_data.get('is_superuser')
        if is_superuser:
            user = self.save(commit=False)
            user.is_superuser = True
            user.save()
        return cleaned_data