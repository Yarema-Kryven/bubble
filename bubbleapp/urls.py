"""bubble URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$',views.index,name='index'),
    re_path(r'^categories/$',views.categories,name='categories'),
    re_path(r'new_category/$',views.new_category,name='new_category'),
    re_path(r'edit_category/(?P<category_id>\d+)/$', views.edit_category,name='edit_category'),
    re_path(r'edit_category/(?P<category_id>\d+)/delete/$', views.delete_category, name='delete_category'),
    re_path(r'^transactions/$',views.transactions,name='transactions'),
    re_path(r'new_transaction/(?P<transaction_id>\d+)/$',views.new_transaction,name='edit_transaction'),
    re_path(r'new_transaction/$',views.new_transaction,name='new_transaction'),
    re_path(r'new_transaction/(?P<transaction_id>\d+)/delete/$', views.delete_transaction, name='delete_transaction'),
    re_path(r'^report_form/$',views.report,name='report_form'),
    re_path(r'^about/$',views.about,name='about'),


]
