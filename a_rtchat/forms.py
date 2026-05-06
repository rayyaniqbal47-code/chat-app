from .models import ChatGroup , GroupMessage
from django import forms


class ChatMessageCreateForm(forms.ModelForm):
    
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'add message ...' , 'class': 'p-4 text-black' , 'maxlength':'300', 'autofocus': True})
        }
    


class NewGroupForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name' : forms.TextInput(attrs={
                'placeholder': 'Add name ...', 
                'class': 'p-4 text-black', 
                'maxlength' : '300', 
                'autofocus': True,
                }),
        }
        
