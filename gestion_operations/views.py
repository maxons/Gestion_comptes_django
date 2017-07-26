from django.shortcuts import render
from gestion_operations.models import Types, Compte, Operation
from .forms import OperationForm

# Create your views here.
def accueil(request):
    """ Afficher tous les articles de notre blog """
    types = Operation.objects.all()  # Nous sélectionnons tous nos articles
    return render(request, 'gestion_operations/accueil.html', {
        'Operation': types})


def operation_form(request):
    form = OperationForm(request.POST or None)
    if form.is_valid():
        numeroCompte = form.cleaned_data['numeroCompte']
        montant = form.cleaned_data['montant']
        date = form.cleaned_data['date']
        types = form.cleaned_data['types']
        debit = form.cleaned_data['debit']
        description = form.cleaned_data['description']
    return render(request, 'gestion_operations/form_ope.html', locals())
