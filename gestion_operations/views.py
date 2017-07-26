from django.shortcuts import render
from gestion_operations.models import Types, Compte, Operation

# Create your views here.
def accueil(request):
    """ Afficher tous les articles de notre blog """
    types = Operation.objects.all()  # Nous sélectionnons tous nos articles
    return render(request, 'gestion_operations/accueil.html', {
        'Operation': types})

