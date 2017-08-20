import django_tables2 as tables
from .models import Operation, Types, Compte

class OperationTable(tables.Table):
    amend = tables.TemplateColumn('<input type="radio" name=test value="{{ record.pk }}" />', verbose_name="Amend")
    selection = tables.CheckBoxColumn(accessor='pk')
    class Meta:
        model = Operation


class TypesTable(tables.Table):
    class Meta:
        model = Types


class CompteTable(tables.Table):
    class Meta:
        model = Compte
