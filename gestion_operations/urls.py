from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.accueil, name="accueil"),
    url(r'^form_ope/$', views.operation_form, name="form_ope"),
    url(r'^select_ope/$', views.select_ope, name="select_ope"),
    url(r'^modify_ope/$', views.modify_ope, name="modify_ope"),
    url(r'^update_op_value/(?P<oper_id>\d+)$', views.update_op_value, name="update_op_value"),
    url(r'^addition/(?P<nombre1>\d+)/(?P<nombre2>\d+)/$', views.addition, name="add"),
    url(r'^delete_operation/$', views.delete_ope, name="delete_operation"),



]


"""url(r'^date$', views.date_actuelle),
url(r'^addition/(?P<nombre1>\d+)/(?P<nombre2>\d+)/$', views.addition),
url(r'^mapage$', views.mapage),
url(r'^$', views.accueil, name='accueil'),
url(r'^article/(?P<id>\d+)-(?P<slug>.+)$', views.lire, name='lire'),
url(r'^contact/$', views.contact, name='contact'),"""
