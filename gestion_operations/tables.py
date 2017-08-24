import django_tables2 as tables
from .models import Operation, Types, Compte

class OperationTableWF(tables.Table):

    modify = tables.TemplateColumn('<input type="radio" name="modify" value="{{ record.id }}" />', verbose_name="Modify")
    delete_ope = tables.TemplateColumn('<input type="checkbox" name="delete_ope" value="{{ record.id }}" />', verbose_name="Delete")
    class Meta:
        model = Operation

class OperationTable(tables.Table):
    delete_ope = tables.TemplateColumn('<input type="checkbox" name="delete_ope" value="{{ record.id }}" checked/>', verbose_name="Delete")
    class Meta:
        model = Operation



class TypesTable(tables.Table):
    class Meta:
        model = Types


class CompteTable(tables.Table):
    class Meta:
        model = Compte
