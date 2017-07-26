from django import forms

class OperationForm(forms.Form):
    numeroCompte = forms.CharField(widget= forms.NumberInput)
    montant = forms.CharField(widget= forms.NumberInput)
    date = forms.DateField(widget= forms.SelectDateWidget(years=range(2017, 2021)))
    types = forms.CharField(max_length=100)
    debit = forms.BooleanField()
    description = forms.CharField(widget = forms.Textarea)

