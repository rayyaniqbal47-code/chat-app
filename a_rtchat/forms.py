from .models import ChatGroup , GroupMessage
from django import forms


class ChatMessageCreateForm(forms.ModelForm):
    
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'add message ...' , 'class': 'p-4 text-black' , 'maxlength':'300', 'autofocus': True})
        }
    



