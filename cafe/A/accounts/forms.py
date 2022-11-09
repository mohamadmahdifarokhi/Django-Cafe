from django import forms
from .models import User
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    p1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    p2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name')

    def clean_p2(self):
        cd = self.cleaned_data
        if cd['p1'] and cd['p2'] and cd['p1'] != cd['p2']:
            raise ValidationError('Passwords don\'t match.')
        return cd['p2']

    # commit az samt code dare bara ma miad
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['p1'])
        if commit:
            user.save()
        return user


class UserRegisterationForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(label='Full name',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label='Phone number', max_length=11,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email is already taken.')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError('This phone number is already taken.')
        return phone_number


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(label='Phone number', max_length=11,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UpdateProfileForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'w-50 form-control'}))
    full_name = forms.CharField(label='Full_name', widget=forms.TextInput(attrs={'class': 'w-50 form-control'}))
    phone_number = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={'class': 'w-50 form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'w-50 form-control'}))
