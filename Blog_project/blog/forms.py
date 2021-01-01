from django import forms
from .models import Comment
class EmailSendForm(forms.Form):
    name=forms.CharField()
    from_email=forms.EmailField(label='From')
    to_email=forms.EmailField(label='To')
    comments=forms.CharField(widget=forms.Textarea,required=False)
    
class CommentForm(forms.Form):
    name=forms.CharField(label='Name')
    email=forms.EmailField(label='Email')
    comment=forms.CharField(label='Comments',widget=forms.Textarea)
    bot_handler=forms.CharField(label='Country',widget=forms.HiddenInput,required=False)

    def clean(self):
        cleaned_data=super().clean()
        i_bot_handler=cleaned_data['bot_handelr']
        if len(i_bot_handler)>0:
            raise forms.ValidationError('BoT Caught!!..')

class CommentModelForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['name','email','comment',]

    