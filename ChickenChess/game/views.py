from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import render,redirect
from django.views.generic import ListView, CreateView
from game.models import Pending_Game
from players.models import profile
from .forms import createGameForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse,reverse_lazy
from django.contrib.auth.models import User

# Create your views here.
@login_required
def game(request,inviting,color):
    pending = Pending_Game.objects.get(inviting=inviting)
    time = pending.time
    increment = pending.increment
    return render(request, template_name='game/game.html', context={
        'inviting':inviting,
        'color':color,
        'white' : 'white',
        'black':'black',
        'time' : time*60,
        'increment' : increment,
        })

class LobbyView(LoginRequiredMixin,ListView):
    model = Pending_Game
    template_name = 'game/LobbyList.html'


'''class creategameView(LoginRequiredMixin,CreateView):
    model = Pending_Game
    template_name = 'game/creategameView.html'
    form_class = createGameForm
    success_url = reverse_lazy('game:lobby')    #aspetta dentro il wschannel aperto'''

class creategameView(LoginRequiredMixin,CreateView):
    model = Pending_Game
    template_name = 'game/creategameView.html'
    form_class = createGameForm
    success_url = reverse_lazy('game:lobby')

    def get_context_data(self, **kwargs):
        #Use this to add extra context.#
        context = super(creategameView, self).get_context_data(**kwargs)
        form = self.form_class(profileid=self.request.user)
        #form.instance.User = User.objects.get(id=self.request.user.id)
        #self.request.session['user_id'] = self.request.user.id

        return context

@login_required
def creategame(request):
    if request.method =='GET':
        try:
            invited =  request.GET['invited']
        except:
            invited = ''
        return render(request,template_name='game/creategameView.html',context = {'invited': invited})
    if request.method == 'POST':
        try:
            if int(request.POST['time']) <= 0 or int(request.POST['increment']) < 0:
                return Http404("Time and increment cannot be negative")
        except:
            return Http404("time and increment must be numeric values")
        p = Pending_Game()
        p.inviting = request.user.username
        p.time = request.POST['time']
        p.increment = request.POST['increment']
        p.color_inviting = request.POST['color_inviting']
        if len(request.POST['invited']) > 1:
            p.invited = request.GET['invited']
        p.save()
        return redirect(reverse('game:game',kwargs = {'inviting':p.inviting,'color':p.color_inviting}))
