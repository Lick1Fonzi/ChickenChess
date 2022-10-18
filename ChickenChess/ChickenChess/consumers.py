import json
from traceback import print_stack
from channels.generic.websocket import AsyncWebsocketConsumer
from ChickenChess.chess_logic import board
from game.models import Pending_Game
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from players.models import profile, Game
from colorama import Fore
import traceback

class WSConsumerChess(AsyncWebsocketConsumer):
    async def connect(self):
        inviting = self.scope['url_route']['kwargs']['inviting']
        self.inviting = inviting
        inviting_color = self.scope['url_route']['kwargs']['color']
        self.username = self.scope['user'].username
        self.increment = 0
        
        #self.room_name = self.scope['url_route']['kwargs']['white'] +'-'+ self.scope['url_route']['kwargs']['black']
        self.room_name = inviting+inviting_color
        self.room_group_name = 'game' + self.room_name

        self.white_player = ''
        self.black_player = ''
        self.set_users_and_colors(inviting,inviting_color)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        if len(self.channel_layer.groups.get(self.room_group_name, {}).items()) > 2:
            return 
        
        '''if len(self.channel_layer.groups.get(self.room_group_name, {}).items()) > 1:
            try:
                await self.delete_pending()
            except Exception as e:
                print("error in deleting pending game: ",e)'''

        await self.accept()

    async def receive(self, text_data):
        print(Fore.GREEN + f"{self.username} is receiving:"+ Fore.WHITE)
        
        if 'connected' in text_data:
            if self.username != self.inviting:
                await self.channel_layer.group_send(
                    self.room_group_name,
                        {
                            'type' : 'connected',
                            'connected' : 'connected'
                        }
                    )
            return

        text_data_json = json.loads(text_data)

        for field in json.loads(text_data):
            print(f"{field}: "+str(text_data_json[field]))

        outcome = text_data_json['outcome']
        allmoves = text_data_json['allmoves']
        position = text_data_json['position']

        try:
            if len(text_data_json['black_player']) > 1:
                self.black_player = text_data_json['black_player']
            if len(text_data_json['black_player']) > 1:
                self.white_player = text_data_json['white_player']
        except:
            pass


        
        
        

        #print('ricevo '+self.scope['user'].username, self.white_player, self.black_player, 'dati ingresso:'+text_data_json['white_player']+text_data_json['black_player'])


        if outcome != '':
            print('ciclo resign')
            await self.channel_layer.group_send(
                self.room_group_name,
                    {
                        'type' : 'endgame',
                        'allmoves' : allmoves,
                        'outcome' : text_data_json['outcome'],
                        'position' : position
                    }
                )
            return

        
        last_move = text_data_json['last_move']
        turn = text_data_json['turn']
        white_time = text_data_json['white_time']
        black_time = text_data_json['black_time']

        bord = board()
        esito = bord.move_online(allmoves,last_move)
        outcome = esito[1]
        position = esito[0]

        

        if esito[1] != '':
            print('ciclo checkmate',outcome)
            await self.channel_layer.group_send(
                self.room_group_name,
                    {
                        'type' : 'endgame',
                        'allmoves' : allmoves+' '+last_move,
                        'outcome' : outcome,
                        'position' : position
                    }
                )
            return
        
        if 1:

            self.time = int(text_data_json['time'])
            self.increment = int(text_data_json['increment'])

            print(f'ciclo fai una mossa di {self.username}:',text_data_json['white_player'] ,text_data_json['black_player'] )

            if len(text_data_json['black_player']) > 1:
                self.black_player = text_data_json['black_player']
            if len(text_data_json['black_player']) > 1:
                self.white_player = text_data_json['white_player']

            await self.channel_layer.group_send(
                self.room_group_name,
                    {
                        'type' : 'move_piece',
                        'position' : position,
                        'allmoves' : allmoves,
                        'last_move' : last_move,
                        'turn' : turn,
                        'outcome' : '',
                        'white_time' : white_time,
                        'black_time' : black_time,
                        'white_player' : self.white_player,
                        'black_player' : self.black_player

                    }
                )

    async def connected(self,event):
        await self.send('connected')

    async def endgame(self,event):
        outcome = event['outcome']
        allmoves = event['allmoves']
        position = event['position']

        await self.send(text_data=json.dumps(
            {
                'position' : position,
                'allmoves' : allmoves,
                'outcome' : outcome,
            })
        )

        if self.username == self.inviting:
            await self.save_game(allmoves,outcome)


        await self.disconnect("WebSocket Disconnected: Game Ended")
        


    async def move_piece(self,event):
        position = event['position']
        turn = event['turn']
        allmoves = event['allmoves']
        last_move = event['last_move']
        white_time = event['white_time']
        black_time = event['black_time']
        outcome = event['outcome']
        black_player = event['black_player']
        white_player = event['white_player']

        if(int(turn)%2==0):
            white_time += self.increment
        else:
            black_time += self.increment

        print(Fore.GREEN+ f"{self.username} is sending"+ Fore.WHITE)
        text_data = json.dumps(
            {
                'position' : position,
                'allmoves' : allmoves+' '+last_move,
                'turn' : str(int(turn) + 1),
                'outcome' : outcome,
                'white_time' : white_time,
                'black_time' : black_time,
                'white_player' : white_player,
                'black_player' : black_player
            })
        print(text_data)
        
        await self.send(text_data=json.dumps(
            {
                'position' : position,
                'allmoves' : allmoves+' '+last_move,
                'turn' : str(int(turn) + 1),
                'outcome' : outcome,
                'white_time' : white_time,
                'black_time' : black_time,
                'white_player' : white_player,
                'black_player' : black_player
            })
        )


    @sync_to_async
    def get_pending(self):
        result = list(Pending_Game.objects.filter(inviting=self.username))
        for g in result:
            print(g)
            g.delete()
    async def delete_pending(self): 
        await self.get_pending()

    @sync_to_async
    def save_game(self,allmoves,outcome):
        try:
            white_user = User.objects.get(username=self.white_player)
            black_user = User.objects.get(username=self.black_player)
            white_profile = profile.objects.get(username=white_user)
            black_profile = profile.objects.get(username=black_user)

            game_to_save = Game()
            game_to_save.time = self.time
            game_to_save.increment = self.increment
            game_to_save.moves = allmoves
            game_to_save.outcome = outcome
            game_to_save.White = white_profile
            game_to_save.Black = black_profile

            self.update_profile_after_game(white_profile,black_profile,outcome)

            game_to_save.save()

        except Exception as e:
            print(f"error occurred while saving game on {self.username} side: ",e)
            traceback.print_exc()

    async def disconnect(self, code):
        try:
            await self.delete_pending()
        except Exception as e:
            print("error in deleting pending game: ",e)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        

    def set_users_and_colors(self,inviting,color_inviting):
        self.black_player = ''
        self.white_player = ''
        if color_inviting == 'white':
            self.white_player = inviting
            if inviting == self.username:
                self.black_player = ''
            else:
                self.black_player = self.username
        else:
            if inviting == self.username:
                self.white_player = ''
            else:
                self.white_player = self.username
            self.black_player = inviting
        
    def update_profile_after_game(self,white,black,outcome):
        if outcome == '1-0':
            winner = white
            loser = black
        elif outcome == '0-1':
            winner = black
            loser = white
        elif outcome == '1/2-1/2':
            white_draw = white.draws + 1
            black_draw = black.draws + 1
            white.draws = white_draw
            black.draws = black_draw
            white.save()
            black.save()
            return

        w_rating = winner.rating + 5
        if w_rating > winner.highest_rating:
            h_rating = w_rating
        else:
            h_rating = winner.highest_rating

        b_rating = loser.rating - 3
        if b_rating < loser.lowest_rating:
            l_rating = b_rating
        else:
            l_rating = loser.lowest_rating

        wins = winner.victories + 1
        loss = loser.losses + 1

        winner.victories = wins 
        winner.rating = w_rating
        winner.highest_rating = h_rating
        loser.losses = loss
        loser.lowest_rating = l_rating
        loser.rating = b_rating
        winner.save()
        loser.save()

        #winner.update_or_create(victories=wins,rating=w_rating, highest_rating=h_rating )
        #loser.update_or_create(losses=loss, rating=b_rating, lowest_rating=l_rating)

