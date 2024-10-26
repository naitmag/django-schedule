from django import forms

from users.models import Group


class CreateStudentForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    middle_name = forms.CharField(max_length=30)
    email = forms.EmailField(required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)


class CreateTeacherForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    middle_name = forms.CharField(max_length=30)
    email = forms.EmailField(required=True)
    position = forms.CharField(max_length=30)
    department = forms.CharField(max_length=80)
    faculty = forms.CharField(max_length=30)


class UploadLessons(forms.Form):
    file = forms.FileInput()
