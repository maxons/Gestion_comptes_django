from django.shortcuts import render
from gestion_operations.models import Types, Compte, Operation
from .forms import OperationForm, ModifyOperationForm, ImportCSVForm
from .tables import OperationTableWF, OperationTable
from django.contrib import messages
import numpy as np
import pandas as pd
from datetime import datetime


def accueil(request):
    all_operations = Operation.objects.all()
    return render(request, 'gestion_operations/accueil.html', {
        'Operation': all_operations})


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

        oper.debit = oper.debit.upper()

        # Set values for type
        selected_type = request.POST.get("type_form")
        oper.type_0 = Types.objects.get(id=int(selected_type))
        oper.type = oper.type_0.nom

        # Set compte foreign key
        selected_compte = request.POST.get("compte_form")
        c_compte = Compte.objects.get(id=int(selected_compte))
        oper.compte = c_compte

        # computes new solde
        ancien_solde = c_compte.solde

        if oper.debit == "TRUE":
            nouveau_solde = ancien_solde - oper.montant
        else:
            nouveau_solde = ancien_solde + oper.montant

        # update solde value in compte
        c_compte.solde = nouveau_solde

        oper.save()
        c_compte.save()

        envoi = True

    all_operations = Operation.objects.all().order_by('-id')[:20]
    all_compte = Compte.objects.all()

    return render(request, 'gestion_operations/form_ope.html', locals())


def select_ope(request):
    table = OperationTableWF(Operation.objects.all())

    # if request.method == "POST":
    #     pks = request.POST.getlist("modify")
    #     res = Operation.objects.filter(pk__in=pks)
    #     # do something with selected_objects
    # else:
    #     res = "no selection"

    friends = Types.objects.all()

    return render(request, 'gestion_operations/select_ope.html', locals())


def modify_ope(request):
    pks_modify = request.POST.getlist("modify")
    # do something with selected_objects

    pks_delete = request.POST.getlist("delete_ope")

    if pks_delete and pks_modify:
        messages.error(request, 'MODIFY AND DELETE.')
    elif pks_modify:
        some_text = "Mais oui mon gars! Ya un truc"
        oper = Operation.objects.get(id=int(pks_modify[0]))

        selected_compte = oper.compte

        oper_dict = {
                        'montant': oper.montant,
                        'date_ope': oper.date_ope,
                        'description': oper.description,
                        'type_form': oper.type_0,
                        'compte_form': oper.compte
                    }
        oper_id = oper.id
        form_modif = ModifyOperationForm(initial=oper_dict)

    elif pks_delete:
        res_delete = Operation.objects.filter(pk__in=pks_delete)
        table_to_delete = OperationTable(res_delete)
    else:
        messages.error(request, 'NOTHING')

    return render(request, 'gestion_operations/modify_ope.html', locals())


def update_op_value(request, oper_id):
    form = ModifyOperationForm(request.POST or None)
    if form.is_valid():
        corrections = form.save(commit=False)
        envoi = True

        oper = Operation.objects.get(id=oper_id)

        oper_new = Operation.objects.get(id=oper_id)

        # Set type foreign key
        selected_type = request.POST.get("type_form")
        oper_new.type_0 = Types.objects.get(id=int(selected_type))
        oper_new.type = oper_new.type_0.nom

        # Set compte foreign key
        selected_compte = request.POST.get("compte_form")
        c_compte = Compte.objects.get(id=int(selected_compte))
        oper_new.compte = c_compte

        oper_new.montant = corrections.montant

        # if the account has changed we have to udapte to solde value
        if oper_new.compte != oper.compte:

            if oper.debit == 'TRUE':
                oper.compte.solde = oper.montant + oper.compte.solde
                c_compte.solde = c_compte.solde - corrections.montant
                pb = "ok"
            elif oper.debit == 'FALSE':
                oper.compte.solde = oper.compte.solde - oper.montant
                c_compte.solde = c_compte.solde + corrections.montant
                pb = "ok"
            else:
                pb = "notok"

        # same account but different values
        elif (oper_new.compte == oper.compte) & (corrections.montant != oper.montant):
            # diff between old and new value
            diff = oper.montant - corrections.montant
            if oper_new.debit == 'TRUE':
                c_compte.solde = c_compte.solde + diff
                pb = "ok"
            elif oper_new.debit == 'FALSE':
                c_compte.solde = c_compte.solde - diff
                pb = "ok"
            else:
                pb = "notok"
        else:
            pb = "nomodif"

        # Date ope
        oper_new.date_ope = corrections.date_ope
        # Description
        oper_new.description = corrections.description

        # update operation and compte in bdd
        oper_new.save()
        c_compte.save()

    else:
        envoi = False

    return render(request, 'gestion_operations/update_op_value.html', locals())


def addition(request, nombre1, nombre2):
    total = int(nombre1) + int(nombre2)

    # Retourne nombre1, nombre2 et la somme des deux au tpl
    return render(request, 'gestion_operations/addition.html', locals())


def delete_ope(request):
    pks_delete = request.POST.getlist("delete_ope")

    if pks_delete:
        messages.success(request, 'delete')
        res_delete = Operation.objects.filter(pk__in=pks_delete)
        table_to_delete = OperationTable(res_delete)

        for to_del in res_delete:
            c_compte = to_del.compte
            if to_del.debit == "TRUE":
                c_compte.solde = c_compte.solde + to_del.montant
                c_compte.save()
                to_del.delete()
            elif to_del.debit == "FALSE":
                c_compte.solde = c_compte.solde - to_del.montant
                c_compte.save()
                to_del.delete()
            else:
                messages.error(request, 'debit of operation is not TRUE of FALSE')

        livret_jeune = Compte.objects.get(id=2)

    else:
        messages.error(request, 'NOTHING')
    return render(request, 'gestion_operations/delete_operation.html', locals())


def import_csv(request):
    form = ImportCSVForm(request.POST or None)

    if form.is_valid():
        file_csv = request.POST.get("file_path")
        data = pd.read_csv(file_csv, sep=";")

        n = data.shape[0]
        for ii in range(0, n):
            new_ope = Operation()
            c_data = data.iloc[ii, ]

            new_ope.montant = c_data.montant
            new_ope.date_ope = datetime.strptime(c_data.date, '%d/%m/%y')
            new_ope.type = c_data.type
            new_ope.debit = c_data.is_debit
            new_ope.libelle = c_data.libelle
            new_ope.details = c_data.details
            new_ope.type_0 = Types.objects.get(id=int(c_data.type_0_id))
            new_ope.compte = Compte.objects.get(id=int(1))

            new_ope.save()

    return render(request, 'gestion_operations/import_csv.html', locals())



