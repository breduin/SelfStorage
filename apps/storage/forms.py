from django import forms
from .models import Unit


from .models import OrderUnit, Order


class OrderUnitForm(forms.ModelForm):

    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), empty_label=None)
    rent_start = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'},
                                 format='%Y-%m-%d'),
                                 label='Дата начала аренды',
                                 error_messages={'required': ''})

    class Meta:
        model = OrderUnit
        fields = ['unit', 'quantity', 'rent_start', 'rent_duration']

    def __init__(self, *args, **kwargs):
        category_id = kwargs.pop('category_id', None)
        super(OrderUnitForm, self).__init__(*args, **kwargs)
        # self.fields['unit'].queryset = Unit.objects.filter(category__id=category_id).order_by('name')


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['warehouse', 'status']
