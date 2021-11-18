from django import forms


from .models import OrderUnit, Order


class OrderUnitForm(forms.ModelForm):

    class Meta:
        model = OrderUnit
        fields = ['unit', 'quantity', 'rent_start', 'rent_duration']


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['warehouse', 'status']
