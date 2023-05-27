from django import forms
from .models import Order, Image
from django.forms import ClearableFileInput


class ImageInlineForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
        widgets = {
            'DELETE': forms.HiddenInput(),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'description', 'quantity']

