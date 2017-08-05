from django.db import models


class Compte(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=150)
    solde = models.DecimalField(max_digits=20, decimal_places=2)
    date_fin = models.DateField(blank=True, null=True)
    nom_proprietaire = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'compte'

    def __str__(self):
        return self.nom


class Types(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'types'

    def __str__(self):
        return self.nom


class Operation(models.Model):
    id = models.AutoField(primary_key=True)
    compte = models.ForeignKey('Compte')
    montant = models.DecimalField(max_digits=20, decimal_places=2)
    date_ope = models.DateField(blank=True, null=True)
    type = models.CharField(max_length=150, blank=True, null=True)
    debit = models.CharField(max_length=5, blank=True, null=True)
    description = models.CharField(max_length=150, blank=True, null=True)
    type_0 = models.ForeignKey('Types', verbose_name = "Type")

    class Meta:
        managed = True
        db_table = 'operation'

    def __str__(self):
        return self.description
