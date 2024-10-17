from django import forms

from users.models import Group


class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    middle_name = forms.CharField(max_length=30)
    email = forms.EmailField(required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)