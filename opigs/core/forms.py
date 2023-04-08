from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator, MaxValueValidator
from taggit.forms import TagField
from django import forms
from .models import *
import datetime
        
def validate_dept(value):
    valid_depts = ['AR', 'AE', 'AF', 'BT', 'CS', 'CE', 'CY', 'CH', 'CI', 'GG', 'HS', 'IM']
    if value.strip() not in valid_depts:
        raise ValidationError(_("Enter a valid department code."))

def validate_graduating_year(value):
    current_year = datetime.date.today().year
    if value > current_year:
        raise ValidationError(_("Graduating year cannot be in the future."))
    elif value < 1950:
        raise ValidationError(_("Graduation year is atleast 1950."))

class UserSignupForm(UserCreationForm):
    user_contact = forms.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    tags = TagField()
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'tags', 'email', 'user_contact', 'password1', 'password2')

class RoleForm(forms.ModelForm):
    ROLES = (
        ('A', 'Alumnus'),
        ('C', 'Company'),
        ('S', 'Student'),
    )

    user_role = forms.ChoiceField(choices=ROLES)

    class Meta:
        model = User
        fields = ('user_role',)

class StudentForm(forms.ModelForm):

    dept = forms.CharField(validators=[validate_dept])
    class Meta:
        model = Student
        fields = ('roll_no', 'dept', 'CV')

class AlumniForm(forms.ModelForm):

    graduating_year = forms.IntegerField(validators=[validate_graduating_year])
    dept = forms.CharField(validators=[validate_dept])
    class Meta:
        model = Alumni
        fields = ('graduating_year', 'dept')

class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('company_name', 'desc')

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('sender_mail', 'subject', 'mail_content')