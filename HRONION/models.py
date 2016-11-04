# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.

class users(AbstractUser):
	Institute = models.CharField(max_length=200, blank = True, null = True) 

	class Meta:
		verbose_name = u'Пользователь'
		verbose_name_plural = u'Пользователи' 

	def __unicode__(self):
		return ('%s %s') % (self.username, self.email)
