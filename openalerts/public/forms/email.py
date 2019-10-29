from django import forms

class EmailSignupForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"email": "Enter your email..."}))