# -*- coding: utf_8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import os, sys
from django.contrib import auth
from django.core.files import File
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response, redirect
from django.template import loader, Context, RequestContext
from django.http import Http404, HttpResponse 
# from HRONION.models import users as MyUser
from CRDB.models import (periodic_table, Crystal, articles_about, project, 
	file_converter, suggest, theory_models, group_theory)
from django.contrib.auth.models import User 
from django.contrib.auth.models import User as MyUser
from django_comments.models import Comment
from forms import (CommentForm, UploadFileForm, 
	SuggestForm, add_paper)
from django.template.context_processors import csrf
from django.core.files.storage import default_storage
from datetime import date
import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
try:
	from django.utils import simplejson as json
except ImportError:
	import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core import serializers
from django.core.mail import send_mail
from tasks import PostEmail, double_KDO

def login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = auth.authenticate(username=username, password=password)
	if user is not None and user.is_active:
		# Правильный пароль и пользователь "активен"
		auth.login(request, user)
		# Перенаправление на "правильную" страницу
		return HttpResponseRedirect("/account/loggedin/")
	else:
		# Отображение страницы с ошибкой
		return HttpResponseRedirect("/account/invalid/")

def index(request):
	args = {}
	user = MyUser
	args['usera'] = user
	return render(
		request, 'CRDB/index.html',args
		)

def chem_list(request):
	all_chem = periodic_table.objects.all()[:20]
	return render(
		request, 'CRDB/chem_list.html',
		{'all_chem': all_chem}
		)


def chem_detail(request, periodic_table_number):
	try:
		chem_element = periodic_table.objects.get(number = periodic_table_number)
	except periodic_table.DoesNotExist:
		raise Http404

	return render(
		request, 'CRDB/chem_detail.html',
		{'chem_element': chem_element}
		)


def article_detail(request, satya_id):
	try:
		article = articles_about.objects.get(id = satya_id)
	except articles_about.DoesNotExist:
		raise Http404

	return render(
		request, 'CRDB/article_detail.html',
		{'article': article}
		)

def profile(request):
	comment_form = CommentForm
	file_form = UploadFileForm
	uploaded= file_converter
	suggest_form = SuggestForm
	args = {}
	args.update(csrf(request))
	args['crystal_is'] = Crystal.objects.all()[:20]
	args['comments'] = Comment.objects.filter(object_pk=1).order_by('-submit_date')[:10]
	args['projects'] = project.objects.get(project_name = 'converter')
	args['form'] = comment_form
	args['files'] = file_form
	args['uploaded'] = uploaded.objects.filter(project=1).order_by('-id')[:50]
	args['suggestions'] = suggest.objects.filter(project= project.objects.get(project_name = 'converter')).order_by('-id')
	args['suggest_form'] = suggest_form
	return render(request, 'CRDB/profile.html',args)

def converter(request):
	comment_form = CommentForm
	file_form = UploadFileForm
	uploaded= file_converter
	suggest_form = SuggestForm
	args = {}
	args.update(csrf(request))
	args['crystal_is'] = Crystal.objects.all()[:20]
	args['comments'] = Comment.objects.filter(object_pk=1).order_by('-submit_date')[:10]
	args['projects'] = project.objects.get(project_name = 'converter')
	args['form'] = comment_form
	args['files'] = file_form
	args['uploaded'] = uploaded.objects.filter(project=1).order_by('-id')
	args['suggestions'] = suggest.objects.filter(project= project.objects.get(project_name = 'converter')).order_by('-id')
	args['suggest_form'] = suggest_form
	return render(request, 'CRDB/converter.html',args)

def forbidden(request):
	comment_form = CommentForm
	file_form = UploadFileForm
	uploaded= file_converter
	suggest_form = SuggestForm
	args = {}
	args.update(csrf(request))
	args['crystal_is'] = Crystal.objects.all()[:20]
	args['comments'] = Comment.objects.filter(object_pk=2).order_by('-submit_date')[:10]
	args['projects'] = project.objects.get(project_name = 'forbidden')
	args['form'] = comment_form
	args['files'] = file_form
	args['uploaded'] = uploaded.objects.filter(project=2).order_by('-id')[:50]
	args['suggestions'] = suggest.objects.filter(project= project.objects.get(project_name = 'forbidden')).order_by('-id')
	args['suggest_form'] = suggest_form
	return render(request,'CRDB/forbidden.html',args)

def references(request):
	comment_form = CommentForm
	file_form = UploadFileForm
	uploaded= file_converter
	suggest_form = SuggestForm
	args = {}
	args.update(csrf(request))
	args['crystal_is'] = Crystal.objects.all()[:20]
	args['comments'] = Comment.objects.filter(object_pk=3).order_by('-submit_date')[:10]
	args['projects'] = project.objects.get(project_name = 'references')
	args['form'] = comment_form
	args['files'] = file_form
	args['uploaded'] = uploaded.objects.filter(project=3).order_by('-id')[:50]
	args['suggestions'] = suggest.objects.filter(project= project.objects.get(project_name = 'references')).order_by('-id')
	args['suggest_form'] = suggest_form
	return render(request,'CRDB/references.html',args)

def theory(request):
	comment_form = CommentForm
	add_paper_form = add_paper
	uploaded= file_converter
	suggest_form = SuggestForm
	args = {}
	args.update(csrf(request))
	args['groups'] = group_theory.objects.all()
	args['theory'] = theory_models.objects.all()
	args['crystal_is'] = Crystal.objects.all()[:20]
	args['projects'] = project.objects.get(project_name = 'theory')
	args['form'] = comment_form
	args['add_paper_form'] = add_paper_form
	args['uploaded'] = uploaded.objects.filter(project=5).order_by('-id')[:50]
	args['suggestions'] = suggest.objects.filter(project= project.objects.get(project_name = 'theory')).order_by('-id')
	args['suggest_form'] = suggest_form
	return render(request,'CRDB/theory.html',args)

def article_list(request):
	article = articles_about.objects.all()
	paginator = Paginator(article, 40)
	page = request.GET.get('page')

	try:
		articles = paginator.page(page)
	except PageNotAnInteger:
		articles = paginator.page(1)
	except EmptyPage:
		articles = paginator.page(paginator.num_pages)
	vars = dict(
		articles=articles,
		)
	return render(request,'CRDB/article_list.html', vars, context_instance=RequestContext(request))
add_paper

def add_paper(request):
	if request.POST:

		my_paper = theory_models.objects.create(name = request.POST['name'], 
			description = request.POST['description'])
		my_paper.files = request.FILES['files']
		my_paper.published_at = date.today()
		my_paper.save()
		for gr in request.POST.getlist('groups'):
			q = group_theory.objects.get(pk=gr) 
			q.theory.add(my_paper)
		
		

	return redirect(project.objects.get(number = 5).url)

def add_suggest(request, project_id):
	if request.POST:
		form = SuggestForm(request.POST)
		if form.is_valid():
			suggestion = suggest.objects.create(text = request.POST['text'], 
				executed = False)
			suggestion.project = project.objects.get(number = project_id)
			suggestion.save()
			object = project.objects.get(number = project_id).url
	return redirect(object)

def try_l(request):
	return render(
		request, 'CRDB/try_l.html'
		)



@login_required
@require_POST	
def like(request):
	if request.method == 'POST':
		user = request.user
		slug = request.POST.get('slug', None)
		projects = get_object_or_404(project, slug=slug)
		response_data = {}
		if projects.likes.filter(id=user.id).exists():
			# user has already liked this company
			# remove like/user
			projects.likes.remove(user)
			response_data['message'] = 'You disliked this'
		else:
			# add a new like for a company
			projects.likes.add(user)
			response_data['message'] = 'You liked this'

	response_data['likes_count'] = projects.total_likes()

	return HttpResponse(json.dumps(response_data), content_type='application/json')


def add_comment(request, project_id):
	user = request.user
	comment_user = request.POST.get('comment_user', None)
	comment_text = request.POST.get('comment_text', None)
	response_data= {}

	if request.POST:
		comment = Comment.objects.create(comment = comment_text, 
			content_type_id = 15L, site_id = 1, object_pk = project_id)
		if request.user.is_authenticated():
			comment.user = user
		else:
			comment.name = comment_user
		comment.save()
		
		objects = Comment.objects.filter(object_pk=project_id).order_by('-submit_date')[:10]

		#response_data['comments'] = serializers.serialize("json", objects)
	return HttpResponse(json.dumps(response_data), content_type='application/json')


def converter_detail(request, file_id):
	try:
		converter_d = file_converter.objects.get(id = file_id)
	except file_converter.DoesNotExist:
		raise Http404

	return render(
		request, 'CRDB/converter_detail.html',
		{'converter_d': converter_d}
		)







def file_converter_def(request, project_id):
	
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)

		if form.is_valid():
			filik = file_converter.objects.create(project = project_id, 
				file_f = request.FILES['files'])
			
			
			url = filik.file_f.url
			path = filik.file_f.path



			import matplotlib
			matplotlib.use('Agg')
			import matplotlib.pyplot as plt
			from io import BytesIO
			from PIL import Image
			import io
			from django.core.files.base import ContentFile
			from lmfit.models import VoigtModel
			import numpy as np
			mod = VoigtModel()

			f = default_storage.open(path)

			# with open(filik.file_f.path, 'r') as f:
			a = 0
			from_file = default_storage.open(path).read().split()
			method = from_file[0]
			shag = float(from_file[3])
			how_many_detectors = float(from_file[4])
			points_1 = int(from_file[5])
			points_2 = int(from_file[6])
			scan_from = float(from_file[2])
			scan_to = scan_from+(points_1-1)*shag

			t1 = []
			t2 = []

			l1 = from_file[7:7+points_1] 
			l2 = from_file[points_1+7:] 

			teta1 = []
			teta2 = []
			intens1 = []
			intens2 = []

			row = 0
			x = scan_from
			
			how_many2 = len(l2)
			how_many1 = len(l1)

			
			for row in range(how_many1):
				teta1.append(x)
				intens1.append(float(l1[row]))
				row = row + 1
				x = x + shag
			
			row = 0
			x = scan_from

			for row in range(how_many2):
				teta2.append(x)
				intens2.append(float(l2[row]))
				row = row + 1
				x = x + shag

			with open(path+'1.dat', 'w') as out:
				for i in range(len(teta1)):
					out.write('%14.8f' % teta1[i])
					out.write(' %14.8f' % intens1[i])
					out.write('\n')

			with open(path+'2.dat', 'w') as out:
				for i in range(len(teta2)):
					out.write('%14.8f' % teta2[i])
					out.write(' %14.8f' % intens2[i])
					out.write('\n')

   
			def max_in_list(lst):
				assert lst
				m = lst[0]
				for i in lst:
					if i > m:
						m = i
				return m

			def min_in_list(lst):
				assert lst
				m = lst[0]
				for i in lst:
					if i < m:
						m = i
				return m


			def null(lst):
				assert lst

				m = lst[0]
				for i in lst:
					if i > m:
						m = i
				for i in range(len(lst)):
					val = lst[i]
					if val == m:
						break

				return i

			def valueOnHalf(lst):
				assert lst
				m = lst[0]
				for i in lst:
					if i > m:
						m = i
				m = m/2
				z=0
				x1 = 0
				x2 = 1
				for i in range(len(lst)):
					val = lst[i]
					if val > m and x1 == 0:
						x1 = i
						x2 = 0
					if x2 == 0 and val < m:
						x2 = i

				
				return [x1, x2]


			max_y1 = max_in_list(intens1)
			x0_1 = teta1[null(intens1)]
			max_y2 = max_in_list(intens2)
			x0_2 = teta2[null(intens2)]

			half_max_y1 = teta1[valueOnHalf(intens1)[1]]-teta1[valueOnHalf(intens1)[0]]
			half_max_y2 = teta2[valueOnHalf(intens2)[1]]-teta2[valueOnHalf(intens2)[0]]

			y1 = np.asarray(intens1)
			x1 = np.asarray(teta1)
			pars1 = mod.guess(y1, x=x1)
			out1  = mod.fit(y1, pars1, x=x1)	
			with plt.xkcd():    
				fig = plt.figure()
				ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
				ax.spines['right'].set_color('none')
				ax.spines['top'].set_color('none')
				plt.xticks([])
				plt.yticks([])
				ax.set_ylim([0, 1.1*max_y1])
				plt.plot(x1, out1.best_fit, 'r-')
				plt.plot(teta1,intens1, 'bo')
				plt.xlabel('deviation from the Bragg angle (s)')
				plt.ylabel('intensity, counts')
				fig.text(
					0.5, 0.1,
					"Voigt model:   " +
					"[FWHM] - " + str(round(out1.params['fwhm'].value,2)) + '"'+ 
					"; [center] - " + str(round(out1.params['center'].value,2)) + '"'+ 
					"; [amplitude] - " + str(round(out1.params['amplitude'].value,0)),
					ha='center')
				imgdata = BytesIO()
				fig.savefig(imgdata, format='png')
				imgdata.seek(0)  # rewind the data
				content_file = ContentFile(imgdata.getvalue())
				filik.converter_result.save(str(request.FILES['files'])+'.png', content_file)
				plt.close()

			y2 = np.asarray(intens2)
			x2 = np.asarray(teta2)
			pars2 = mod.guess(y2, x=x2)
			out2  = mod.fit(y2, pars2, x=x2)	
			with plt.xkcd():    
				fig = plt.figure()
				ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
				ax.spines['right'].set_color('none')
				ax.spines['top'].set_color('none')
				plt.xticks([])
				plt.yticks([])
				ax.set_ylim([0, 1.1*max_y2])
				plt.plot(x2, out2.best_fit, 'r-')
				plt.plot(teta2,intens2, 'bo')
				plt.xlabel('deviation from the Bragg angle (s)')
				plt.ylabel('intensity, counts')
				fig.text(
					0.5, 0.1,
					"Voigt model:   " +
					"[FWHM] - " + str(round(out2.params['fwhm'].value,2)) + '"'+ 
					"; [center] - " + str(round(out2.params['center'].value,2)) + '"'+ 
					"; [amplitude] - " + str(round(out2.params['amplitude'].value,0)),
					ha='center')
				imgdata = BytesIO()
				fig.savefig(imgdata, format='png')
				imgdata.seek(0)  # rewind the data
				content_file = ContentFile(imgdata.getvalue())
				filik.converter_result_2.save(str(request.FILES['files'])+'.png', content_file)
				plt.close()


			filik.Voigt_model_report_1 = out1.fit_report(min_correl=0.25)
			filik.Voigt_model_report_2 = out2.fit_report(min_correl=0.25)
			filik.info = request.POST['info']
			filik.half_width_1 = str(round(out1.params['fwhm'].value,2))
			filik.half_width_2 = str(round(out2.params['fwhm'].value,2))
			filik.file_converted1 =  url+'1.dat'
			filik.file2_converted2 =  url+'2.dat'
			filik.center_1 = str(round(out1.params['center'].value,2))
			filik.center_2 = str(round(out2.params['center'].value,2))
			filik.max1 = str(round(out1.params['amplitude'].value,2))
			filik.max2 = str(round(out2.params['amplitude'].value,2))
			filik.converter_file_path = path
			filik.converter_file_URL = url
			# filik.dated = date.today()
			# filik.time = datetime.datetime.now()
			filik.temperature = float(request.POST['temp'])
			filik.save()
			if not request.POST['info']:
				filik.delete()
		return redirect('/converter/')
	else:
		filik = file_converter(project = 'error', file_f = '')
		filik.save()
	return redirect('/converter/')

def double_crystal(request):
	if request.method == 'POST':
		double_KDO.apply_async(countdown=1)
	double_crystal_form = CommentForm
	suggest_form = SuggestForm
	proj = project.objects.get(slug = 'double-crystal')
	args = {}
	args.update(csrf(request))
	args['projects'] = proj
	args['comments'] = Comment.objects.filter(object_pk=proj.number).order_by('-submit_date')[:10]
	args['suggestions'] = suggest.objects.filter(project= proj).order_by('-id')
	args['suggest_form'] = suggest_form
	return render(request, 'CRDB/double_crystal.html',args)


def scedule(request):
	return render(request,'CRDB/kongress_scedule.html')