from django import forms
from .models import Unit, Warehouse


from .models import OrderUnit, Order


class OrderUnitForm(forms.ModelForm):

    warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.all(), 
                                       empty_label=None,
                                       label='Где?'
                                       )
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), 
                                  empty_label=None,
                                  label='Что?'
                                  )
    rent_start = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'},
                                 format='%Y-%m-%d'),
                                 label='Когда?',
                                 error_messages={'required': ''})

    class Meta:
        model = OrderUnit
        fields = ['warehouse', 'unit', 'quantity', 'rent_duration', 'rent_start']

    def __init__(self, *args, **kwargs):
        category_id = kwargs.pop('category_id', None)
        super(OrderUnitForm, self).__init__(*args, **kwargs)
        # self.fields['unit'].queryset = Unit.objects.filter(category__id=category_id).order_by('name')


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['status']
