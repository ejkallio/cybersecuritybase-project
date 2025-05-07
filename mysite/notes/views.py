from django.shortcuts import render, redirect, HttpResponse
from django.db import connection
from .models import Note
from .forms import noteForm
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def index(request):
	username = request.user.username
	query = f"SELECT * FROM notes_note WHERE user_id = (SELECT id FROM auth_user WHERE username = '{username}')"
	with connection.cursor() as cursor:
		cursor.execute(query)
		note = cursor.fetchall()

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

@csrf_exempt
def delete(request, note_id):
	note = Note.objects.get(pk=note_id)
	note.delete()
	return redirect('index')

def signup (request):
	return redirect('home')