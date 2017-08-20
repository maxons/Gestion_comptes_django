from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.accueil, name="accueil"),
    url(r'^form_ope/$', views.operation_form, name="form_ope"),
    url(r'^test_table/$', views.tables2_test, name="test_table"),
]


"""url(r'^date$', views.date_actuelle),
url(r'^addition/(?P<nombre1>\d+)/(?P<nombre2>\d+)/$', views.addition),
url(r'^mapage$', views.mapage),
url(r'^$', views.accueil, name='accueil'),
url(r'^article/(?P<id>\d+)-(?P<slug>.+)$', views.lire, name='lire'),
url(r'^contact/$', views.contact, name='contact'),"""
