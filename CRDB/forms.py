from django.forms import ModelForm
from django_comments.models import Comment
from CRDB.models import file_converter, group_theory
from django import forms
import datetime

class CommentForm(ModelForm):
	class Meta: 
		model = Comment
		fields = ['comment','user_name']
		

class UploadFileForm(forms.Form):
    files = forms.FileField()
    info = forms.CharField(max_length=100)
    temp = forms.CharField(max_length=10)

class SuggestForm(forms.Form):
    text = forms.CharField(max_length=300)

class add_paper(forms.Form):
	name = forms.CharField(max_length=30)
	files = forms.FileField()
	description = forms.CharField(max_length=1200)
	groups = forms.CharField(max_length=100)
	# groups = forms.ModelMultipleChoiceField(queryset=None)
	published_at = forms.DateField(initial=datetime.date.today)

	# def __init__(self, *args, **kwargs):
	# 	super(add_paper, self).__init__(*args, **kwargs)
	# 	self.fields['groups'].queryset = group_theory.objects.all()