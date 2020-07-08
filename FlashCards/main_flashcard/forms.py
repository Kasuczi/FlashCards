from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class FiszkaCategory(forms.Form):
    """
    Formularz pozwala wybrać kategorie dla wyświetlanych fiszek
    """
    CATEGORY = [
        ('Python', 'Python'),
        ('GitHub', 'GitHub'),
    ]
    category_field = forms.MultipleChoiceField(required=True,
                                               widget=forms.CheckboxSelectMultiple,
                                               choices=CATEGORY,
                                               )


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)