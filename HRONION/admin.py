# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
import HRONION.models
import CRDB.models
# Register your models here.

class UserAdmin(admin.ModelAdmin):
	list_display = (u'username', u'email')



admin.site.register(HRONION.models.users, UserAdmin)