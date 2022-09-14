from django import forms

# create your class forms

class Checkout(forms.Form):
    first_name = forms.CharField(
        required=True,
        label='First Name',
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )  
    )
    last_name = forms.CharField(
        required=True,
        label="Last Name",
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )   
    )
    email = forms.CharField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class':'form-control'
            }
        )   
    )
    phone_number = forms.CharField(
        required=True,
        label="Phone Number",
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )   
    )
    address_line_1 = forms.CharField(
        label="Address Line 1",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )   
    )
    address_line_2 = forms.CharField(
        label="Address Line 2",
        widget=forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )   
    )
    city = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )   
    )
    state = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )   
    )
    country = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )   
    )
    order_note = forms.CharField(
        label="Order Note",
        required=True,
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'rows':'3'
            }
        )   
    )
    
