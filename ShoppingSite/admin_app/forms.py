from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm, PasswordResetForm

class AdminSignupForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm'}))
    password2 = forms.CharField(label="Passowrd(again)", widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm'}))
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name', 'email', 'password1', 'password2']
        labels = {'username':'Username', 'first_name':'First name', 'last_name':'Last name', 'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
                'first_name':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
                'last_name':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
                'email':forms.EmailInput(attrs={'class':'form-control form-control-sm'}),
        }

class AdminLoginForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm'}))

class EmailForForgotPassword(PasswordResetForm):
    #email = forms.CharField(label="Email")
    email = forms.CharField(label="Email", widget=forms.EmailInput(attrs={'class':'form-control form-control-sm'}))
    # class Meta:
    #     model = User
    #     fields = ['email']
    #     labels = {'Email'}
    #     widgets = {'email':forms.EmailInput(attrs={'class':'form-control form-control-sm'})}

class AdminSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm'}))
    new_password2 = forms.CharField(label="ConfirmPassword", widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm'}))

class AdminPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm'}))
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm'}))
    new_password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm'}))

class EditAdminProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        # This fields are only show for Admin
        fields = '__all__'
