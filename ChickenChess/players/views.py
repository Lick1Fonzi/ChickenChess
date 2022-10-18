
from django.shortcuts import render
from django.views.generic.list import ListView
from players.models import Game, profile
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.models import User


# Create your views here.
class ListUserView(ListView):
    model = profile
    template_name = 'players/listagiocatori.html'
    
    def get_queryset(self):
        return profile.objects.order_by('-rating')

class DetailProfileView(LoginRequiredMixin,DetailView):
    model = profile
    template_name = 'players/detailprofile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=context["object"].pk)
        ur_profile = profile.objects.get(pk=user)

        context["games"] = Game.objects.filter(White=ur_profile) | Game.objects.filter(Black=ur_profile)
        return context

