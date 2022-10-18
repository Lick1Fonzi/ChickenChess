from django import forms
from django.shortcuts import get_object_or_404
from .models import Pending_Game,profile
from django.db import models

class createGameForm(forms.ModelForm):
    description = 'create a new game to publish in the lobby'

    def __init__(self, *args, **kwargs):
        
        self.userid = kwargs.pop('profileid', None)
        self.profileid = profile.objects.get(id = self.userid)
        
        
        super(createGameForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('time')<0 or cleaned_data.get('increment') < 0:
            raise forms.ValidationError('Time must be positive')
        if cleaned_data.get('inviting') != self.userid:
            raise forms.ValidationError('you must be the Inviting player')

        

    class Meta:
        model = Pending_Game
        fields = ['inviting','color_inviting','time','increment']
        widgets = {'color_iniviting': forms.RadioSelect , 'time': forms.NumberInput,'increment': forms.NumberInput}