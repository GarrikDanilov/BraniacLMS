import os
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    field_order = (
        'username',
        'password1',
        'password2',
        'email',
        'first_name',
        'last_name',
        'age',
        'avatar'
    )

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'age',
            'avatar',
            'email'
        )

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age <10 or age > 100:
            raise ValidationError('Пожалуйста, введите верный возраст')
        return age


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'age',
            'avatar',
            'email'
        )

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age <10 or age > 100:
            raise ValidationError('Пожалуйста, введите верный возраст')
        return age

    def clean_avatar(self):
        arg_as_str = 'avatar'
        if arg_as_str in self.changed_data and self.instance.avatar:
            if os.path.exists(self.instance.avatar.path):
                os.remove(self.instance.avatar.path)
        return self.cleaned_data.get(arg_as_str)
