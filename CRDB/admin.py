# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from CRDB.models import (Crystal, periodic_table, #MyUser, 
	articles_about, corrode, organization, order_terms, project,
	file_converter, suggest, theory_models, group_theory)

class group_theory_admin(admin.ModelAdmin):
	list_display = ('name', 'slug') 

class theory_admin(admin.ModelAdmin):
	list_display = ('name', 'description') 

class periodic_table_admin(admin.ModelAdmin):
	list_display = ('number', 'name') 

class CrystalAdmin(admin.ModelAdmin):
	list_display = ('name', 'syngony_name') 

class articles_about_admin(admin.ModelAdmin):
	list_display = ('title', 'published_at')

class corrodeAdmin(admin.ModelAdmin):
	list_display = ('title', 'description')

class organizationAdmin(admin.ModelAdmin):
	list_display = ('name', 'city')

class order_termsAdmin(admin.ModelAdmin):
	list_display = ('crystal','corrode', 'organisation', 'price')

# class UserAdmin(admin.ModelAdmin):
# 	list_display = (u'username', u'email')

class project_Admin(admin.ModelAdmin):
	list_display = (u'project_name', u'url')

class file_converter_Admin(admin.ModelAdmin):
	list_display = (u'info',u'file_f', u'project', u'converter_result', 
		u'converter_result_2', u'converter_file_path', u'half_width_1', 
		u'half_width_2')

class suggest_Admin(admin.ModelAdmin):
	list_display = (u'project', u'text', u'executed') 

admin.site.register(group_theory, group_theory_admin)
admin.site.register(theory_models, theory_admin)
admin.site.register(suggest, suggest_Admin)
admin.site.register(project, project_Admin)
admin.site.register(Crystal, CrystalAdmin)
admin.site.register(periodic_table, periodic_table_admin)
admin.site.register(articles_about, articles_about_admin)
admin.site.register(corrode, corrodeAdmin)
admin.site.register(organization, organizationAdmin)
admin.site.register(order_terms, order_termsAdmin)
# admin.site.register(MyUser, UserAdmin)
admin.site.register(file_converter, file_converter_Admin)
