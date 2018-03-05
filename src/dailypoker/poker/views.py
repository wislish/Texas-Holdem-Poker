from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as u_login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.db import transaction
from django.http import Http404, HttpResponse
from .models import *
import random
# from poker.comparehands import *
from itertools import combinations
from .comparehands import *
from .consumers import ws_clock, ws_clockinit, ws_clockfinish


@login_required
def home(request):
    prof = request.user.profile

    return render(request, 'index.html', {"profile":prof})


# @login_required
# def roomSelection(request):
#     errors = []
#     games = Game.objects.all()
#     # profile=Profile.objects.get(user=request.user)
#     context = {'items': games}
#     return render(request,'searchRoom.html',context)

@login_required
def game(request, gid):
    game = get_object_or_404(Game, id=gid)

    u = request.user
    players = game.player_set.all()


    find = False
    for p in players:
        if p.user.id == u.id and not p.is_online:
            # print("user already exist")
            find = True

    context = {}
    context['gid'] = gid
    context['name'] = request.user.username
    context['buyin'] = game.buyin
    if game.is_start:
        if find:
            ## re-join the game.
            print("re-join")
            return render(request, 'game.html', context)
        else:
            print("already starts.")
            ## if game starts, no new user can join in.
            raise Http404
    else:
        for p in players:
            if p.user.id == u.id:
                print("duplicate")
                raise Http404

        if u.profile.asset < game.buyin:
            error = "Not enough asset for buyin"
            return render(request, 'searchRoom.html', {'error': error,'items': Game.objects.all()})
        else:
            return render(request, 'game.html', context)

    # return render(request, 'game.html', context)


@login_required
def rank(request):
    return render(request, 'rank.html', {})


@login_required
def search(request):
    games = Game.objects.all().order_by('-id')
    # profile=Profile.objects.get(user=request.user)
    context = {'items': games}
    return render(request, 'searchRoom.html', context)


@login_required
def create(request):
    return render(request, 'creation.html', {})


def login(request):
    context = {}

    # Just display the registration and login form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'login.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'login.html', context)

    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    u_login(request, user)

    return redirect('/poker/')


def register(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'register.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'register.html', context)

    # If we get here the form data was valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email'],
                                        is_active=False)
    new_user.save()

    token = default_token_generator.make_token(new_user)

    email_body = """
            Welcome to DailyPoker! Please click the link below to 
            verify your email address and complete the registration of your account:
            http://%s%s
            """ % (request.get_host(),
                   reverse('regconfirm', args=(new_user.username, token)))

    send_mail(subject="DailyPoker - Verify your email address",
              message=email_body,
              from_email="dailypoker@cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'email_confirm.html', context)


@transaction.atomic
def registration_confirmation(request, username, token):
    user = get_object_or_404(User, username=username)

    if not default_token_generator.check_token(user, token):
        raise Http404

    user.is_active = True
    user.save()

    # create a default profile for the user
    new_profile = Profile.objects.create(user=user, asset=10000)
    new_profile.save()

    u_login(request, user)
    return redirect('/poker/')


@login_required
def game_create(request):
    error = ""
    profile = get_object_or_404(Profile, user=request.user)
    if 'buyin-select' not in request.POST or not request.POST['buyin-select']:
        return Http404
    else:
        select = request.POST['buyin-select']
        buyin = 0
        if select == '1':
            buyin = 600
        if select == '2':
            buyin = 1500
        if select == '3':
            buyin = 3000

        game = Game()
        game.buyin = buyin
        # game.is_start = False
        game.save()

        print (buyin)
        print (profile.asset)

        game.buyin = buyin
        game.save()
        # print buyin
        # print profile.asset
        # print (buyin)
        # print (profile.asset)

        if buyin > profile.asset:
            error = "Not enough asset for buyin"
            return render(request, 'creation.html', {'error': error})

    return redirect(reverse('game', kwargs={"gid": game.id}))


@csrf_exempt
@login_required
def game_init(request, gid):
    ## shuffle the cards
    allcards = []
    deck = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    s = ['H', 'D', 'C', 'S', ]
    for x in deck:
        for s in ['H', 'D', 'C', 'S']:
            index = x + s
            allcards.append(index)
    deskcards = random.sample(set(allcards), 5)
    for card in deskcards:
        allcards.remove(card)

    usercards = random.sample(set(allcards), 2)

    ## temporarily store the rival cards in the cards_remain.
    for card in usercards:
        allcards.remove(card)
    rivalcards = random.sample(set(allcards), 2)

    ## find the created game
    game = get_object_or_404(Game, id=gid)
    game.reset()
    if game.is_contain_player(request.user):
        ## no need to create new player, but must refresh.
        new_player = game.player_set.get(playername=request.user.username)
        new_player.reset()
        new_player.save()
    else:
        new_player = Player(playername=request.user.username, user=request.user, begin_chip=game.buyin,
                            card_one=usercards[0], card_two=usercards[1], chip_remain=game.buyin, game=game
                            )
        new_player.save()

    for card in deskcards:
        c = Card.objects.get(card=card)
        game.cards_on_table.add(c)

    for card in rivalcards:
        c = Card.objects.get(card=card)
        game.cards_remain.add(c)

    new_player.card_one = usercards[0]
    new_player.card_two = usercards[1]
    new_player.save()
    game.save()

    # context = {"id": new_player.id, "name": request.user.username, "BeginChip": new_player.begin_chip,
    #            "RoundBet": new_player.round_bet,
    #            "AccumBet": new_player.accum_bet, "card0": usercards[0], "card1": usercards[1],"player":new_player}

    context = {"player": new_player}
    return render(request, 'reply/player.json', context, content_type='application/json')


@csrf_exempt
def game_update(request):
    choiceForm = PlayerChoiceForm(request.POST)

    if choiceForm.is_valid():
        p = get_object_or_404(Player, id=choiceForm.cleaned_data['pid'])
        # p = Player.objects.get(id=choiceForm.cleaned_data['pid'])
        p.state = choiceForm.cleaned_data['choice']
        p.round_bet += choiceForm.cleaned_data['cost']
        p.accum_bet += choiceForm.cleaned_data['cost']
        #############################################################
        ###??? wait to see if possible, or have to store first ???###
        p.chip_remain = p.begin_chip - p.accum_bet

        p.save()
        ## deal with game state
        game = p.game

        ## emulate bot player
        ## auto bet the same size, change the pot size.
        game.pot_size += choiceForm.cleaned_data['cost']

        game.pot_size += choiceForm.cleaned_data['cost']
        game.update_max(p.round_bet)

        cards_to_send = []
        if game.round_finish():
            if game.is_finish():
                # game.clear_round_bet()
                game.save()
                return redirect(reverse('finish', kwargs={"pid": p.id}))
            else:
                game.round_status += 1
                cards_to_send = game.deal_cards()
                game.clear_round_bet()

        game.save()

        context = {"pot_size": game.pot_size, "max_bet": game.round_max_bet, "round_status": game.round_status,
                   "is_finished": game.is_finished, "desk": cards_to_send, "players": game.player_set.all()}
        return render(request, 'reply/updates.json', context, content_type='application/json')
    else:
        raise Http404


# @login_required
def game_finish(request, pid):
    user = Player.objects.get(id=pid)
    card1 = user.card_one
    card2 = user.card_two

    game = user.game
    potsize = game.pot_size

    cards = []

    for c in game.cards_on_table.all():
        cards.append(c.card)

    # print(cards)
    usercards = cards[:]
    usercards.append(card1)
    usercards.append(card2)

    # append rival's cards
    rival_hand_cards = []
    for c in game.cards_remain.all():
        rival_hand_cards.append(c.card)

    rivalcards = cards[:]
    rivalcards.append(rival_hand_cards[0])
    rivalcards.append(rival_hand_cards[1])

    usercombo = list(combinations(usercards, 5))

    maxusercombo = list(usercombo[0])
    for combo in usercombo[1:]:
        combo = list(combo)
        if getwinner(combo, maxusercombo) == combo:
            maxusercombo = combo

    rivalcombo = list(combinations(rivalcards, 5))
    maxrivalcombo = list(rivalcombo[0])
    for combo in rivalcombo[1:]:
        combo = list(combo)
        if getwinner(combo, maxrivalcombo) == combo:
            maxrivalcombo = combo

    winner = "robot"
    # user_remain = 0
    if getwinner(maxusercombo, maxrivalcombo) == maxusercombo:
        winner = user.playername
        user.chip_remain += potsize

    user_remain = user.chip_remain
    user.save()

    profile = get_object_or_404(Profile, user=request.user)
    profile.asset += potsize
    profile.save()

    context = {"winner": winner, "chips": user_remain, "last": user.accum_bet, "pot": potsize,
               "rival": game.cards_remain.all()}
    return render(request, 'reply/finishes.json', context, content_type='application/json')


def game_test(request):
    player = get_object_or_404(Player, id='1')
    print(player.html)
    context = {"test": "testtext", "player": player}
    return render(request, 'reply/player.json', context, content_type='application/json')


def game_test2(request):
    cards = []
    card1 = get_object_or_404(Card, id='1')
    cards.append(card1)
    card2 = get_object_or_404(Card, id='2')
    cards.append(card2)
    card3 = get_object_or_404(Card, id='3')
    cards.append(card3)
    card4 = get_object_or_404(Card, id='4')
    cards.append(card4)
    context = {"cards": cards}
    return render(request, 'reply/test2.json', context, content_type='application/json')


def game_websocket_test(request):
    return render(request, 'websockettest.html', {"user1": "test"})


def help(request):
    return render(request, 'help.html', {})
