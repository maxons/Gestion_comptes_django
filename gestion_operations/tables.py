import django_tables2 as tables
from .models import Operation, Types, Compte

class OperationTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk')
    class Meta:
        model = Operation


class TypesTable(tables.Table):
    class Meta:
        model = Types


class CompteTable(tables.Table):
    class Meta:
        model = Compte
