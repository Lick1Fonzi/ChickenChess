from players.models import *

def erase_dbs():
    print('erased DB')
    User.objects.all().delete()
    profile.objects.all().delete()

def start_dbs():

    if len(User.objects.all()) == 0:

        utenti = ["MagnoCarlo", "IlChiaroNakamura","AliceIrene_Firugia","Lenny_Bongcloud"] 
        password = ['11111111', '22222222', '33333333', '420']
        rating = [3000, 2500, 1700, 650]
        victories = [300,200,100,45]
        losses = [22,40,60,100]
        draws = [5,10,20,40]

        for i in range(len(utenti)):
            u = User.objects.create_user(utenti[i], '',password[i] )
            p = profile()
            u.save()
            p.username = u
            p.rating = rating[i]
            p.highest_rating = p.rating
            p.victories = victories[i]
            p.losses = losses[i]
            p.draws = draws[i]
            p.save()
    print('Populated DB')