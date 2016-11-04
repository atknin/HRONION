#coding=utf-8

import sys, os, django
import xlrd

os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRDB.settings")
django.setup()

from CRDB.models import periodic_table


#for e in organization.objects.all(): print e.name

# db = MySQLdb.connect(host="localhost",user="root", passwd="vfntvfnbrf43",db="myproject_database") 
# cursor = db.cursor()


path = os.path.realpath(os.path.dirname(sys.argv[0]))+'/scripts/'
rb = xlrd.open_workbook(path + 'chem.xls',formatting_info=True)
sheet = rb.sheet_by_index(0)
# periodic_table.objects.create(number=200, name = 'oppened by self', abbriviation = 'My',
# 	group = '69', period = '69', atomic_weight = '0', density = '0', 
# 	observed_el_configure = 'compilicated', atomic_radius = '0', crystal_structure = 'amorph')

for rownum in range(sheet.nrows):
	row = sheet.row_values(rownum)
	number = int(row[0])
	name = row[4]
	abbrev = row[1]
	group = row[2]
	period = row[3]
	weight = row[5]
	rho = row[8]
	el_conf = row[9]
	rad = row[10]
	struct = row[11]

	periodic_table.objects.create(number=number, name = name, abbriviation = abbrev,
		group = group, period = period, atomic_weight = weight, density = rho, 
		observed_el_configure = el_conf, atomic_radius = rad, crystal_structure = struct)
	 
