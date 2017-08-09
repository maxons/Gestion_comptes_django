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
        """numeroCompte = form.cleaned_data['numeroCompte']
        montant = form.cleaned_data['montant']
        date = form.cleaned_data['date']
        types = form.cleaned_data['types']
        debit = form.cleaned_data['debit']
        description = form.cleaned_data['description']"""


        oper = form.save(commit=False)

        # Set values for type
        selected_type = request.POST.get("type_form")
        oper.type_0 = Types.objects.get(id = int(selected_type))
        oper.type = oper.type_0.nom

        # Set compte foreign key
        selected_compte = request.POST.get("compte_form")
        c_compte = Compte.objects.get(id = int(selected_compte))
        oper.compte = c_compte

        # computes new solde
        ancien_solde = c_compte.solde

        if oper.debit == "True":
            nouveau_solde = ancien_solde - oper.montant
        else:
            nouveau_solde = ancien_solde + oper.montant

        # update solde value in compte
        c_compte.solde = nouveau_solde

        all_operations = Operation.objects.all().order_by('-id')[:20]
        all_compte = Compte.objects.all()

        envoi = True


    return render(request, 'gestion_operations/form_ope.html', locals())
