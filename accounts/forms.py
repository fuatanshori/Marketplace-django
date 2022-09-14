from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Create Password",
        widget=forms.PasswordInput(attrs={
        'id':'password',
        'placeholder':'Enter Password',
        'class':'form-control'

    }))
    confirm_password = forms.CharField(
        label="Confirmation Password",
        widget=forms.PasswordInput(
        attrs={
        'id':'password',
        'placeholder':'confirmation Password',
        'class':'form-control'
    })
    )
    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number','email','password']

    def __init__(self,*args, **kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'password does not match !'
            )
    
class FormLogin(forms.Form):
    email = forms.EmailField(
        max_length=200,
        widget=forms.EmailInput(
            attrs={
                'class':'form-control',
                'placeholder':'Enter Email Address',
            }
        )
    )
    password = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'id':'password',
                'class':'form-control',
                'placeholder':'Enter Password'
            }
        )
    )

class ForgotPassword(forms.Form):
    email = forms.EmailField(
        required=True,
        max_length=200,
        widget=forms.EmailInput(
            attrs={
                'class':'form-control',
                'placeholder':'Enter Email Address',
            }
        )
    )

class ResetPassword(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id':'password',
        'placeholder':'Create Password',
        'class':'form-control'

    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id':'confirmpassword',
        'placeholder':'confirmation Password',
        'class':'form-control'
    }))