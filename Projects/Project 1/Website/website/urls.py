from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^results[/]$', views.results, name="index"),
    url(r'^queries/1[/]$', views.query1, name="query1"),
    url(r'^queries/2[/]$', views.query2, name="query2"),
    url(r'^queries/3[/]$', views.query3, name="query3"),
    url(r'^queries/4[/]$', views.query4, name="query4"),
    url(r'^queries/5[/]$', views.query5, name="query5"),
    url(r'^queries/6[/]$', views.query6, name="query6"),
    url(r'^queries/3/1[/]$', views.part3_1, name="part3_1"),
    url(r'^queries/3/2[/]$', views.part3_2, name="part3_2"),
]
