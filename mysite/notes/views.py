from django.shortcuts import render, redirect, HttpResponse
from django.db import connection
from .models import Note
from .forms import noteForm,SignUpForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
# Create your views here.

@login_required
@csrf_exempt
def index(request):
	username = "test' OR '1'='1" #
	#FLAW 1: SQL injection
	query = f"SELECT * FROM notes_note WHERE user_id = (SELECT id FROM auth_user WHERE username = '{username}')"
	with connection.cursor() as cursor:
		cursor.execute(query)
		note = cursor.fetchall()
	#Fix for FLAW1: use parameterized query to preven SQL injection:
	#query = f"SELECT * FROM notes_note WHERE user_id = (SELECT id FROM auth_user WHERE username = %s)"
	#with connection.cursor() as cursor:
		#cursor.execute(query, [username])
		#note = cursor.fetchall()
		
	if request.method == 'POST':
		form = noteForm(request.POST)
		if form.is_valid():
			new_note = form.save(commit=False)
			new_note.user = request.user
			new_note.save()
			return redirect('index')
		
	else:
		form = noteForm()
	
	return render(request, 'notes/notesPage.html', {'notes':note, 'form': form})

@login_required
@csrf_exempt
def edit(request, note_id):
	note = Note.objects.get(pk=note_id)
	if request.method == 'POST':
		form = noteForm(request.POST, instance=note)
		if form.is_valid():
			edited_note = form.save(commit=False)
			edited_note.user = request.user
			edited_note.save()
			return redirect('index')
	else:
		form = noteForm(instance=note)
	
	context = {
		'notes' : note,
		'form' : form
	}
	return render(request,'user/edit.html', context)

@login_required
@csrf_exempt
def delete(request, note_id):
	note = Note.objects.get(pk=note_id)
	note.delete()
	return redirect('index')

def signup (request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password = raw_password)
			login(request, user)
			return redirect('index')
	else: 
		form = SignUpForm()
	return render(request, 'notes/signup.html', {'form': form})