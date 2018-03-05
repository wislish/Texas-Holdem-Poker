from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from .models import Player


class PlayerChoiceForm(forms.Form):
    pid = forms.IntegerField()
    choice = forms.CharField(max_length=10)
    cost = forms.IntegerField(min_value=0)


    def clean_pid(self):

        pid = self.cleaned_data.get('pid')

        p = get_object_or_404(Player, id=pid)

        return pid

    def clean_choice(self):

        choice_set = {"check", "fold", "bet", "call"}

        c = self.cleaned_data.get('choice')

        if c not in choice_set:
            raise forms.ValidationError("Unknown user action.")
        return c

    def clean_cost(self):

        c = self.cleaned_data.get('cost')
        pid = self.cleaned_data.get('pid')
        p = get_object_or_404(Player, id=pid)

        if p.chip_remain < c:
            raise forms.ValidationError("Unvalid bet.")

        return c

# class CreateGame


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=50,
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'FirstName',
                                            'class': 'form-control'}))
    last_name = forms.CharField(max_length=50,
                                widget=forms.TextInput(
                                    attrs={'placeholder': 'LastName',
                                           'class': 'form-control'}))
    username = forms.CharField(max_length=20,
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'Username',
                                          'class': 'form-control eden-signin-form'}))
    email = forms.EmailField(max_length=100,
                             widget=forms.TextInput(
                                 attrs={'placeholder': 'Email',
                                        'class': 'form-control eden-signin-form'}))
    password = forms.CharField(max_length=200,
                               label='Password',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control eden-signin-form'}))
    conform_password = forms.CharField(max_length=200,
                                       label='Confirm password',
                                       widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                         'class': 'form-control eden-signin-form'}))

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        conform_password = cleaned_data.get('conform_password')
        email = cleaned_data.get('email')

        if not first_name:
            raise forms.ValidationError("First name is required.")
        if not last_name:
            raise forms.ValidationError("Last name is required.")
        if not email:
            raise forms.ValidationError("Email Invalid.")
        if not password:
            raise forms.ValidationError("Password is required.")
        if not conform_password:
            raise forms.ValidationError("Password Confirm is required.")

        if password and conform_password and password != conform_password:
            raise forms.ValidationError("Passwords did not match.")
        if User.objects.filter(username=username):
            raise forms.ValidationError("Username is already taken.")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20,
                               label='Username',
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'Username',
                                          'class': 'form-control mr-sm-2'}))
    password = forms.CharField(max_length=200,
                               label='Password',
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'Password',
                                          'class': 'form-control mr-sm-2'}))

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(LoginForm, self).clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username does not exist!")

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Username does not match with Password!")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data
