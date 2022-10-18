from django.http import HttpResponse
import json
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from players.models import profile
from .chess_logic import board
from django.views.generic.edit import CreateView
from django.urls import reverse,reverse_lazy
from django.contrib.auth.models import User

def home(request):
    return render(request,template_name='home.html',context={})

def match(request):
    position = board()
    
    if request.GET['color'] == 'black':
        opponents_move = position.stockfish.get_best_move_time(1000)
        position.board.push(position.object_move(opponents_move))
    else:
        opponents_move = ''

    b = ''
    for piece in str(position.board):
        if piece != '\n' and piece != ' ':
            b += piece
    b = b[::-1]
    print(b)
    return render(request,template_name='stockfish.html', context={'position':b, 'moves': opponents_move+' ', 'player_color':request.GET['color']})

def getmoves(request):
    movesmade = request.GET['moves']
    movefrom = request.GET['from']
    position = board()
    if movesmade != '':
        position.update(movesmade)
    response = json.dumps(position.dictify_legal_moves(movefrom))
    return HttpResponse(response)

def makemove(request):
    position = request.GET['position']
    move = request.GET['move']
    bord = board()
    opponent_move = bord.return_updated_position_after_move(position,move)
    if opponent_move[2] == None:
        outcome = ''       #outcome
    else:
        outcome = str(opponent_move[2])
    response = {'board': opponent_move[0], 'allmoves':position+' '+move+' '+opponent_move[1], 'gameover' : outcome}
    response = json.dumps(response)
    return HttpResponse(response)

def createProfile(username):
    p = profile()
    user = User.objects.get(username=username)
    p.username = user
    p.save()

def success(request):
    return render(request, template_name='success.html')
    
class UserCreateView(CreateView):
 form_class = UserCreationForm
 template_name = "user_create.html"

 def get_success_url(self, **kwargs):
        createProfile(self.username)
        return reverse("success")

 def post(self, request, *args, **kwargs):
    self.username = request.POST['username']
    return super().post(request, *args, **kwargs) 
