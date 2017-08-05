from django import forms
from .models import Operation


class OperationForm(forms.ModelForm):
    """numeroCompte = forms.CharField(widget= forms.NumberInput)
    montant = forms.CharField(widget= forms.NumberInput)
    date = forms.DateField(widget= forms.SelectDateWidget(years=range(2017, 2021)))
    types = forms.CharField(max_length=100)
    debit = forms.BooleanField()
    description = forms.CharField(widget = forms.Textarea)"""

    date_ope = forms.DateField(widget= forms.SelectDateWidget(years=range(2017, 2021)))
    description = forms.CharField(widget = forms.Textarea)

    class Meta:
        model = Operation
        #fields = '__all__'
        fields = ('compte', 'montant', 'date_ope', 'debit','type_0', 'description')
