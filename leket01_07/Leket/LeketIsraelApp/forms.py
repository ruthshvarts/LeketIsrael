from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


class ExtendedUserCreationForm(UserCreationForm):
    username = forms.CharField(label="שם משתמש", max_length=30)
    password1 = forms.CharField(label="סיסמה", strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label="אימות סיסמה", widget=forms.PasswordInput, strip=False)
    email = forms.EmailField(label="אימייל", required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}),
                             help_text='Required. Enter a valid email address.')

    error_messages = {
    'password_mismatch': "הסיסמאות אינן תואמות.",
    'invalid': "הכנסת ערך לא חוקי.",
    'required': "שדה זה הינו שדה חובה.",
}

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        email_validator = EmailValidator(message="כתובת האימייל אינה תקנית.")
        self.fields['email'].validators = [email_validator]

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("כתובת האימייל שהוזנה כבר קיימת במערכת. נסו להזין כתובת אימייל אחרת.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("שם המשתמש כבר תפוס. אנא החלף שם משתמש")
        return username

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'אימייל'

    def as_view(self, *args, **kwargs):
        return super().as_view(*args, **kwargs)

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].label = _("סיסמה חדשה")
        self.fields['new_password2'].label = _("אימות סיסמה חדשה")
        self.error_messages['password_mismatch'] = _("הסיסמאות אינן תואמות.")
