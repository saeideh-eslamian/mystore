from django import forms
from .models import ShippinAddress
    


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50,required=True)
    last_name = forms.CharField(max_length=50,required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(),required=True)


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippinAddress
        exclude = ['customer',]
