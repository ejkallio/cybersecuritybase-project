from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Note
class SignUpForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

	def clean_password1(self):
		password1 = self.cleaned_data.get('password1')
		return password1
	
class noteForm(forms.ModelForm):
	class Meta:
		model = Note
		fields = ['header', 'content']