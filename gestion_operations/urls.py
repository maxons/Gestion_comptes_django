from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.accueil, name="accueil"),
    re_path(r'^form_ope/$', views.operation_form, name="form_ope"),
    re_path(r'^select_ope/$', views.select_ope, name="select_ope"),
    re_path(r'^modify_ope/$', views.modify_ope, name="modify_ope"),
    re_path(
    	r'^update_op_value/(?P<oper_id>\d+)$',
    	views.update_op_value,
    	name="update_op_value"),
    re_path(r'^addition/(?P<nombre1>\d+)/(?P<nombre2>\d+)/$', views.addition, name="add"),
    re_path(r'^delete_operation/$', views.delete_ope, name="delete_operation"),
    re_path(r'^import_csv/$', views.import_csv, name="import_csv"),
]


"""url(r'^date$', views.date_actuelle),
url(r'^addition/(?P<nombre1>\d+)/(?P<nombre2>\d+)/$', views.addition),
url(r'^mapage$', views.mapage),
url(r'^$', views.accueil, name='accueil'),
url(r'^article/(?P<id>\d+)-(?P<slug>.+)$', views.lire, name='lire'),
url(r'^contact/$', views.contact, name='contact'),"""
