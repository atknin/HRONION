#coding=utf-8

import sys, os, django

os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRDB.settings")
django.setup()
from CRDB.models import Crystal, articles_about
import random 
from datetime import date,timedelta


materials = Crystal.objects.all()
path = os.path.realpath(os.path.dirname(sys.argv[0]))+'/scripts'


#файл жаргона для заголовков
name_stat = []
with open(path+ '/title.txt', 'r') as title:
	for line in title: name_stat.append(line)	
abstract = []
with open(path+ '/abstract.txt', 'r') as abstract_f:
	while True:
		line=abstract_f.read(800)
		if not line: break
		abstract.append(line)


for i in range(1000000):


	statya = articles_about.objects.create(title = random.choice(name_stat))
	statya.published_at = (date(2016,1,1) + timedelta(days=random.randint(0,365))).isoformat()
	statya.url = 'http://www.randomwebsite.com/cgi-bin/random.pl'
	statya.abstract = random.choice(abstract)
	statya.save()

	statya.to_crystal.add(random.choice(materials))
	statya.to_crystal.add(random.choice(materials))
