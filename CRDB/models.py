# -*- coding: utf_8 -*-
from __future__ import unicode_literals
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from unidecode import unidecode

class group_theory(models.Model):
	name = models.CharField(max_length=300, blank=True, null=True)
	slug = models.SlugField(blank = True, null =  True)
	theory = models.ManyToManyField('CRDB.theory_models', blank=True,  default='No')

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(unidecode(self.name))
			super(group_theory, self).save(*args, **kwargs)

	class Meta:
		verbose_name = u'Какие разделы (theory)'
	def __str__(self):
		return self.name.encode('utf8')

class theory_models(models.Model):
	name = models.CharField(max_length=30, blank=True, null=True) 
	files = models.FileField(blank=True, null=True, upload_to='theory') 
	description = models.CharField(max_length=1200, blank=True, null=True) 
	published_at = models.DateField(verbose_name=u'Date of publishing', blank=True, null=True) 

	class Meta:
		ordering = ('published_at',)
		verbose_name = u'Теория'
		verbose_name_plural = u'Теория' 

	def __unicode__(self):
		return ('%s. %s') % (self.name, self.description)


class suggest(models.Model):
	text = models.CharField(max_length=300, blank=True, null=True) 
	executed = models.BooleanField()
	project = models.ForeignKey('CRDB.project', on_delete=models.CASCADE, blank=True, null=True) 
	class Meta:
		verbose_name = u'suggestion'
		verbose_name_plural = u'suggestions' 
	def __str__(self):
		return self.text.encode('utf8')

class project(models.Model):
	project_name = models.CharField(max_length=100) 
	slug = models.SlugField(blank = True, null =  True)
	likes = models.ManyToManyField('HRONION.users', related_name='likes')
	number = models.IntegerField(unique=True)
	url = models.URLField(verbose_name='URL', max_length=300, blank=True, null=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.project_name)
		super(project, self).save(*args, **kwargs)

	def total_likes(self):
		return int(self.likes.count())

	class Meta:
		ordering = ('project_name', )
		verbose_name = u'project'
		verbose_name_plural = u'projects' 
	def __str__(self):
		return self.project_name

# class MyUser(AbstractUser):
# 	organisations = models.ManyToManyField(to = 'CRDB.organization', blank=True) 
# 	articles = models.ManyToManyField(to = 'CRDB.articles_about', blank=True,  default='No') 

# 	class Meta:
# 		verbose_name = u'Пользователь'
# 		verbose_name_plural = u'Пользователи' 

# 	def __unicode__(self):
# 		return ('%s %s') % (self.username, self.email)


class organization(models.Model):
	name = models.CharField(max_length=200) 
	city = models.CharField(max_length=100) 
	adress = models.CharField(max_length=400)
	e_mail = models.EmailField(max_length=254)
	phone_number = models.CharField(max_length=10)
	crystal =  models.ManyToManyField('CRDB.Crystal', through='order_terms')
	corrode =  models.ManyToManyField('CRDB.corrode', through='order_terms')
	class Meta:
		ordering = ('name', )
		verbose_name = u'organization'
		verbose_name_plural = u'organizations' 
	def __str__(self):
		return self.name



class order_terms(models.Model):
	crystal = models.ForeignKey('CRDB.Crystal', on_delete=models.CASCADE, blank=True, null=True) 
	corrode = models.ForeignKey('CRDB.corrode', on_delete=models.CASCADE, blank=True, null=True) 
	organisation = models.ForeignKey(organization, on_delete=models.CASCADE) 
	#availability = models.BooleanField(blank=True)
	price = models.DecimalField(verbose_name=u'цена, rubles', max_digits = 7, decimal_places=1)

	class Meta:
		ordering = ('price', )
		verbose_name = u'order_terms'
		verbose_name_plural = u'order_terms' 

	def __str__(self):
		return str(self.price)
		

#---------------------------------хим элементы-----------------------------------------
class periodic_table(models.Model):
	number = models.IntegerField(blank = True, null =  True)
	name = models.CharField(max_length=20, blank = True, null = True) 
	abbriviation = models.CharField(max_length=20, blank = True, null = True)
	group = models.CharField(max_length=20, blank = True, null = True) 
	period = models.IntegerField(blank = True, null =  True)
	atomic_weight =  models.DecimalField(verbose_name=u'g/mole', max_digits = 9, decimal_places=6, blank = True, null =  True)
	density = models.DecimalField(verbose_name=u'g/cm3', max_digits = 12, decimal_places=7, blank = True, null =  True)
	observed_el_configure = models.CharField(max_length=50, blank = True, null =  True)
	atomic_radius = models.DecimalField(verbose_name=u'radius, A', max_digits = 6, decimal_places=3, blank = True, null =  True)
	crystal_structure = models.CharField(max_length=100, blank = True, null =  True)
	

	
	class Meta:
		ordering = ('number',)
		verbose_name = u'chemical element'
		verbose_name_plural = u'chemical elements' 
	def __str__(self):
		return self.name	


#---------------------------------соединения-----------------------------------------
class Crystal(models.Model):
	SYNGONY_CHOICES = (
		(u'Triclinic', u'Triclinic'),
		(u'Monoclinic', u'Monoclinic'),
		(u'Orthorhombic', u'Orthorhombic'),
		(u'Tetragonal', u'Tetragonal'),
		(u'Trigonal', u'Trigonal'),
		(u'Hexagonal', u'Hexagonal'),
		(u'Cubic', u'Cubic'),
	)
	
	name = models.CharField(verbose_name=u'which crystal', max_length=200)
	syngony_name = models.CharField(max_length=15, choices=SYNGONY_CHOICES,default='indefinited')

	a_parametr =  models.DecimalField(verbose_name=u'a, angrtem', max_digits = 7, decimal_places=4)
	b_parametr =  models.DecimalField(verbose_name=u'b, angrtem', max_digits = 7, decimal_places=4)
	c_parametr =  models.DecimalField(verbose_name=u'c, angrtem', max_digits = 7, decimal_places=4)
	alfa = models.DecimalField(verbose_name=u'alfa, degrees', max_digits = 5, decimal_places=2, blank=True, null=True)
	beta = models.DecimalField(verbose_name=u'beta, degrees', max_digits = 5, decimal_places=2, blank=True, null=True)
	gamma = models.DecimalField(verbose_name=u'gamma, degrees', max_digits = 5, decimal_places=2, blank=True, null=True)
	rho = models.DecimalField(verbose_name=u'density, gr/cm3', max_digits = 5, decimal_places=2, blank=True, null=True)
	file_f = models.FileField(blank=True, null=True, upload_to='article') 
	
	chem_elements = models.ManyToManyField(periodic_table)

	created_at = models.DateField(verbose_name=u'when it created')
	
	class Meta:
		ordering = ('created_at', )
		verbose_name = u'Crystal'
		verbose_name_plural = u'Crystals' 
	def __str__(self):
		return ('%s %s') % (self.name, self.syngony_name)


#---------------------------------статьи на тему-----------------------------------------
class articles_about(models.Model):
	title = models.CharField(max_length=100) 
	published_at = models.DateField(verbose_name=u'Date of publishing', blank=True, null=True) 
	to_crystal = models.ManyToManyField(Crystal)
	url = models.URLField(verbose_name='URL', max_length=300, blank=True, null=True)
	abstract = models.CharField(max_length=1000, blank=True, null=True)
	
	
	class Meta:
		ordering = ('published_at',)
		verbose_name = u'artilce'
		verbose_name_plural = u'articles' 
	def __unicode__(self):
		return self.title	



#---------------------------------травители-----------------------------------------
class corrode(models.Model):
	title = models.CharField(max_length=100, default='default') 
	to_crystal = models.ManyToManyField(Crystal)
	composition = models.ManyToManyField(to = periodic_table,verbose_name=u'composition')
	description = models.CharField(max_length=200, blank=True, null=True, default='nobady wrote yet') 


	class Meta:
		verbose_name = u'etching agent'
		verbose_name_plural = u'etching agents' 
	def __str__(self):
		return self.title	

class file_converter(models.Model):
	file_f = models.FileField(blank=True, null=True, upload_to='some') 
	info  = models.CharField(max_length=200, blank=True, null=True) 
	project = models.CharField(max_length=10) 
	converter_result = models.ImageField(blank=True, null=True, upload_to='some/converter') 
	converter_result_2 = models.ImageField(blank=True, null=True, upload_to='some/converter') 
	converter_file_path = models.CharField(max_length=50, blank=True, null=True) 
	converter_file_URL = models.URLField(verbose_name='URL', max_length=300, blank=True, null=True)
	half_width_1 = models.CharField(blank=True, null=True, max_length=10) 
	half_width_2 = models.CharField(blank=True, null=True, max_length=10) 
	center_1 = models.CharField(blank=True, null=True, max_length=10) 
	center_2 = models.CharField(blank=True, null=True, max_length=10) 
	max1 = models.CharField(blank=True, null=True, max_length=10) 
	max2 = models.CharField(blank=True, null=True, max_length=10) 
	Voigt_model_report_1 = models.CharField(blank=True, null=True, max_length=500) 
	Voigt_model_report_2 = models.CharField(blank=True, null=True, max_length=500) 
	file_converted1 = models.FileField(blank=True, null=True, upload_to='some/converter')
	file2_converted2 = models.FileField(blank=True, null=True, upload_to='some/converter')
	dated = models.DateField(verbose_name=u'dated', blank=True, null=True) 
	time = models.DateTimeField(verbose_name=u'timed', blank=True, null=True) 
	temperature = models.DecimalField(verbose_name=u'g/cm3', max_digits = 4, decimal_places=2, blank = True, null =  True)
	class Meta:
		verbose_name = u'converter_file'
		verbose_name_plural = u'converter_files' 
	def __str__(self):
		return self.file_f.name	

			

