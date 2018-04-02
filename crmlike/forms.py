from django import forms
from crmlike.models import CustomerProfile


class LoginForm(forms.Form):
    name = forms.CharField(label='Имя пользователя')
    surname = forms.CharField(label='Фамилия')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')


class RegistrationForm(forms.Form):
    name = forms.CharField(label='Имя пользователя')
    surname = forms.CharField(label='Фамилия')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Подтверждение пароля')


class ChangeForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ('first_name', 'last_name', 'customer_avatar')
        labels = {
            'first_name': ('Имя'),
            'last_name': ('Фамилия'),
            'customer_avatar': ('Пользовательское изображение'),
        }
