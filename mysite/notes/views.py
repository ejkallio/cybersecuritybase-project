from django.shortcuts import render, redirect, HttpResponse
from django.db import connection
from .models import Note
from .forms import noteForm,SignUpForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

# FLAW 3: Insufficient monitoring and logging 
# Fix for FLAW 3: implement basic security logging
#import logging
#
#logger = logging.getLogger('django.security')

# FLAW 5: CSRF
# Fix for FLAW 5: Replace csrf_exempt with csrf_protect
# @csrf_protect
@login_required
@csrf_exempt
def index(request):
	username = request.user.username
	#FLAW 1: SQL injection
	query = f"SELECT * FROM notes_note WHERE user_id = (SELECT id FROM auth_user WHERE username = '{username}')"
	with connection.cursor() as cursor:
		cursor.execute(query)
		note = cursor.fetchall()
	#Fix for FLAW 1: Use a parameterized query to preven SQL injection:
	#query = "SELECT * FROM notes_note WHERE user_id = (SELECT id FROM auth_user WHERE username = %s)"
	#with connection.cursor() as cursor:
		#cursor.execute(query, [username])
		#note = cursor.fetchall()
		
	if request.method == 'POST':
		form = noteForm(request.POST)
		if form.is_valid():
			new_note = form.save(commit=False)
			new_note.user = request.user
			new_note.save()
			#logger.info(f"User {request.user.username} created note with the ID: {new_note.id} ")
			return redirect('index')
		
	else:
		form = noteForm()
	
	return render(request, 'notes/notesPage.html', {'notes':note, 'form': form})

# FLAW 5:
#csrf_protect
@login_required
@csrf_exempt
def edit(request, note_id):
	note = Note.objects.get(pk=note_id)
	# FLAW 2: Broken access control
	# FIX for FLAW 2: Check if the note belongs to the current user before allowing editing
	#if request.user != note.user:
		#return HttpResponse("Error: You don't have permission to edit this note.")
	if request.method == 'POST':
		form = noteForm(request.POST, instance=note)
		if form.is_valid():
			edited_note = form.save(commit=False)
			edited_note.user = request.user
			edited_note.save()

			#logger.info(f"User {request.user.username} edited note with the ID: {edited_note.id} ")
			return redirect('index')
	else:
		form = noteForm(instance=note)
	
	context = {
		'notes' : note,
		'form' : form
	}
	return render(request,'user/edit.html', context)

# FLAW 5:
# csrf_protect
@login_required
@csrf_exempt
def delete(request, note_id):
	note = Note.objects.get(pk=note_id)
	#logger.info(f"User {request.user.username} deleted note with the ID: {note.id} ")
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