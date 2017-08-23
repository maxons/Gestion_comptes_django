from django import forms
from .models import Operation, Types, Compte


class OperationForm(forms.ModelForm):
    """numeroCompte = forms.CharField(widget= forms.NumberInput)
    montant = forms.CharField(widget= forms.NumberInput)
    date = forms.DateField(widget= forms.SelectDateWidget(years=range(2017, 2021)))
    types = forms.CharField(max_length=100)
    debit = forms.BooleanField()
    description = forms.CharField(widget = forms.Textarea)"""

    date_ope = forms.DateField(widget= forms.SelectDateWidget(years=range(2017, 2021)))
    description = forms.CharField(widget = forms.Textarea)

    debit = forms.BooleanField(initial = True, required = False)

    # for type in all_types:
    all_types = Types.objects.all()
    type_form = forms.ChoiceField(choices=[(o.id, o.nom) for o in all_types])
    #types_perso = forms.ModelChoiceField(all_types)

    all_comptes = Compte.objects.all()
    compte_form = forms.ChoiceField(choices=[(o.id, o.nom) for o in all_comptes])

    class Meta:
        model = Operation
        #fields = '__all__'
        fields = ['montant', 'date_ope', 'debit', 'description']



class ModifyOperationForm(forms.ModelForm):
    date_ope = forms.DateField(widget= forms.SelectDateWidget(years=range(2017, 2021)))
    description = forms.CharField(widget = forms.Textarea)

    # for type in all_types:
    all_types = Types.objects.all()
    type_form = forms.ChoiceField(choices=[(o.id, o.nom) for o in all_types])
    #types_perso = forms.ModelChoiceField(all_types)

    all_comptes = Compte.objects.all()
    compte_form = forms.ChoiceField(choices=[(o.id, o.nom) for o in all_comptes])
    #id = forms.CharField(widget = forms.NumberInput)
    class Meta:
        model = Operation
        #fields = '__all__'
        fields = ['montant', 'date_ope', 'description']







