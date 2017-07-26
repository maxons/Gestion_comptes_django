from django import forms

class OperationForm(form.Form):
    numeroCompte = forms.NumberInput()
    montant = forms.NumberInput()
    date = forms.DateInput()
    types = forms.CharField()
    debit = forms.BooleanField()
    description = forms.Textarea()


