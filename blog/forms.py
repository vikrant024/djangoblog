from django import forms

from blog.models import Comment

# creating a form
class ContactForm(forms.Form):

	name = forms.CharField(max_length = 200)
	phone_number= forms.IntegerField()
	email = forms.EmailField(max_length = 150)
	comment = forms.CharField(widget = forms.Textarea, max_length = 2000)
	
class NewCommentForm(forms.ModelForm):

  class Meta:
    model = Comment
    fields = ['name','body']
