from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username'] 

class LoginForm(AuthenticationForm):
   
    # No es necesario sobreescribirlo a menos que quieras cambiar su comportamiento.
    pass

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    def clean(self):
      
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise ValidationError("La nueva contraseña y la confirmación no coinciden.")

        return cleaned_data