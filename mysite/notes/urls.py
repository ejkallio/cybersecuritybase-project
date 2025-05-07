from django.urls import path

from . import views
from notes.views import index, edit, delete, signup

urlpatterns = [
	path('', index, name='index'),
	path('signup/', signup, name='signup'),
	path('edit/<int:note_id>', edit, name='edit'),
	path('delete/<int:note_id>', delete, name='delete')
]