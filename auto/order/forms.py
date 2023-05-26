from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('description', 'product', 'quantity')

    def save(self, commit=True, user=None):
        order = super(OrderForm, self).save(commit=False)
        if user:
            order.user = user
        if commit:
            order.save()
        return order