from django.conf.urls import url
from CRDB.views import (chem_list, chem_detail, index, 
    converter, article_list, try_l, add_comment, article_detail)


urlpatterns = [ 
	url(r'^chem_list/', chem_list, name = 'chem_list'),
    url(r'^chem_detail/(?P<periodic_table_number>\d+)/', chem_detail, name = 'chem_detail'),
    url(r'^article_detail/(?P<satya_id>\d+)/', article_detail, name = 'article_detail'),
    url(r'^add_comment/(?P<project_id>\d+)/', add_comment, name = 'add_comment'),
    url(r'^converter/', converter, name = 'converter'),
    url(r'^article_list/', article_list, name = 'article_list'),
    url(r'^donot/', try_l, name = 'try_l'),



]