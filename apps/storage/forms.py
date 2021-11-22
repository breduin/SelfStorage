from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import escape
from .models import Unit, Warehouse


from .models import OrderUnit, Order

class UnitSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            if value.instance.id == 5:
                option['attrs']['data-icon'] = '&#9975;' # лыжи
            elif value.instance.id == 2:
                option['attrs']['data-icon'] = '&#9923;' # шины
            elif value.instance.id == 4:
                option['attrs']['data-icon'] = '&#127938;' # сноуборд
            elif value.instance.id == 3:
                option['attrs']['data-icon'] = '&#128690;' # велосипед
            else:
                option['attrs']['data-icon'] = '&#9635;' # бокс и всё остальное

        option['attrs']['class'] = 'unit-options'
        return option


class OrderUnitForm(forms.ModelForm):

    warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.all(), 
                                       empty_label=None,
                                       label='Где?'
                                       )
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), 
                                  empty_label=None,
                                  label='Что?',
                                  widget=UnitSelect,
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


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['status']
