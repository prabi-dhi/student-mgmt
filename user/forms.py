from django import forms
from .models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','password','email','user_type']

    def save(self, commit=True):
        user = super().save(commit=False)      
        user.set_password(self.cleaned_data['password'])      
        if commit:
            user.save()
        return user