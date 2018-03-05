import json
from itertools import combinations

from channels import Group
from django.contrib.auth.models import User
from django.db import models
import random
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

# from poker.comparehands import getwinner

from dailypoker.poker.comparehands import getwinner


class Profile(models.Model):
    user = models.OneToOneField(User)
    asset = models.IntegerField(default=10000)

    def __unicode__(self):
        return self.user


class Player(models.Model):
    playername = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    game = models.ForeignKey("Game")
    begin_chip = models.IntegerField(default=0)
    round_bet = models.IntegerField(default=0)
    accum_bet = models.IntegerField(default=0)
    card_one = models.CharField(max_length=10, null=True)
    card_two = models.CharField(max_length=10, null=True)

    is_online = models.BooleanField(default=False)
    state = models.CharField(max_length=10, null=True)
    is_round_play = models.BooleanField(default=False)
    seat_id = models.PositiveSmallIntegerField(null=True)
    chip_remain = models.IntegerField(default=0)

    def __unicode__(self):
        return self.playername

    def reset(self):
        self.round_bet = 0
        self.accum_bet = 0
        self.state = "action"
        self.seat_id = None
        self.begin_chip = self.chip_remain
        self.is_online = False
        self.is_round_play = False

    @property
    def html(self):
        return render_to_string("reply/usertemplate.html",
                                {"name": self.playername, "begin_chip": self.begin_chip, "round_bet": self.round_bet,
                                 "accum_bet": self.accum_bet, "card0": self.card_one, "card1": self.card_two}).replace(
            "\n", "")

    def to_dict(self):
        return model_to_dict(self,
                             fields=["playername", "begin_chip", "chip_remain", "accum_bet", "is_online", "state"])

    def show_hands(self):
        return model_to_dict(self, fields=["playername", "begin_chip", "chip_remain", "accum_bet", "state", "card_one",
                                           "card_two"])


class Card(models.Model):
    card = models.CharField(max_length=10)

    def __unicode__(self):
        return self.card

    @property
    def html(self):
        return render_to_string("reply/cardtemplate.html", {"card": self.card, "card_id": self.id}).replace("\n", "")


class Game(models.Model):
    dealer = models.SmallIntegerField(default=-1, null=True)
    current_player = models.SmallIntegerField(default=0, null=True)
    cards_on_table = models.ManyToManyField(Card, related_name="ontable")
    cards_remain = models.ManyToManyField(Card, related_name="remain")

    pot_size = models.IntegerField(default=0)
    round_max_bet = models.IntegerField(default=0)
    round_status = models.PositiveSmallIntegerField(default=0)
    is_finished = models.BooleanField(default=False)
    is_start = models.BooleanField(default=False)

    ##game property
    blind = models.IntegerField(default=10)
    bigblind = models.IntegerField(default=20)
    buyin = models.IntegerField(default=600)
    # number_of_players = models.PositiveSmallIntegerField(default=6,null=True)
    num_start = models.PositiveSmallIntegerField(default=0, null=True)

    # def to_dict(self):
    #
    #     return model_to_dict(self,fields=["pot_size","dealer",])

    def reset(self):
        self.cards_on_table.clear()
        self.cards_remain.clear()
        self.pot_size = 0
        self.round_status = 0
        self.round_max_bet = 0
        self.is_finished = False
        self.num_start = 0
        self.is_start = False

    def is_contain_player(self, user):

        for p in self.player_set.all():
            if p.user.id == user.id:
                return p.id

        return None

    def fold_player_num(self):
        num = 0
        for p in self.player_set.all():
            if p.state == "fold" or not p.is_online:
                num += 1
        return num

    def allin_player_num(self):
        num = 0
        for p in self.player_set.all():
            if p.state == "allin":
                num += 1
        return num

    def is_only_one_player_left(self):
        # print(self.num_players())
        # print(self.fold_player_num())
        return (self.num_players() - self.fold_player_num()) == 1

    def non_all_in_player_num(self):

        return (self.num_players() - self.allin_player_num())

    def is_finish(self, pid=None):
        # play to the last round
        if self.round_status == 3:
            self.is_finished = True
            return True

        # only one player leave in the game
        if self.is_only_one_player_left():
            self.is_finished = True
            return True

        # non all-in players are less than 1
        if self.non_all_in_player_num() <= 1:
            self.is_finished = True
            return True

        # online user less than one
        if self.num_players() - self.num_offline_players() <= 1:
            self.is_finished = True
            return True

        return False

    ## may need to consider all-in...
    def round_finish(self):

        ## only one effective player left
        if self.is_only_one_player_left():
            return True

        ## bet even
        for p in self.player_set.all():
            if not p.is_online or p.state == "fold" or p.state == "allin":
                continue
            if p.round_bet != self.round_max_bet:
                return False

            ## not start to play in each round
            if not p.is_round_play:
                return False

        return True

    def update_max(self, bet):

        if bet > self.round_max_bet:
            self.round_max_bet = bet

        self.save()

    ## may need to consider fold.
    def clear_round_bet(self):
        for p in self.player_set.all():
            p.round_bet = 0
            if p.state != "fold":
                p.is_round_play = False
            p.save()

        self.round_max_bet = 0

    def deal_cards(self, fixed=None):

        if fixed:
            return self.choose_cards(fixed)

        if self.round_status == 1:
            return self.choose_cards(3)

        elif self.round_status == 2:
            return self.choose_cards(4)

        elif self.round_status == 3:
            return self.choose_cards(5)

        elif self.round_status == 0:
            return []

    def choose_cards(self, size):
        card_list = list(self.cards_on_table.all())

        ## set a random seed, to get same result each time.
        random.Random(4).shuffle(card_list)
        result = []
        for i in range(size):
            result.append(card_list[i])

        return result

    def num_players(self):

        return len(self.player_set.all())

    def num_offline_players(self):

        num = 0
        for p in self.player_set.all():
            if not p.is_online:
                num += 1

        return num

    @property
    def game_group(self):

        return Group("game-%s" % self.id)

    def user_group(self, user):

        return Group("user-%s" % user.username)

    def send_init(self, user):

        init_msg = {}
        init_msg['initial'] = 'true'

        all_players = self.game_players_dict(uid=user.id)
        init_msg['players'] = all_players
        init_msg['number'] = len(all_players)

        self.user_group(user).send(
            {"text": json.dumps(init_msg)}
        )

    def send_reconnect(self, user, pid):

        p = get_object_or_404(Player, id=pid)

        msg = {}
        msg['reconnect'] = 'true'

        all_players = self.game_players_dict(uid=user.id)
        msg['players'] = all_players
        msg['number'] = len(all_players)
        msg['card0'] = p.card_one
        msg['card1'] = p.card_two
        msg['dealer'] = list(self.player_set.all())[self.dealer].playername
        msg['chip_remain'] = p.chip_remain
        msg['playername'] = p.playername
        msg['accum_bet'] = p.accum_bet
        msg['pot_size'] = self.pot_size
        msg['desk'] = [c.card for c in self.deal_cards()]
        msg['current_player'] = list(self.player_set.all())[self.current_player].playername

        p.is_online = True

        self.user_group(user).send(
            {"text": json.dumps(msg)}
        )

        p.save()

    def send_join(self, user):

        join_msg = {'join': "true", 'begin_chip': 0, 'playername': user.username}

        self.game_group.send(
            {"text": json.dumps(join_msg)}, immediately=True
        )

    def send_leave(self, user):

        msg = {'leave': "true", 'playername': user.username}

        self.game_group.send(
            {"text": json.dumps(msg)}
        )

    def send_countdown(self, data):

        self.game_group.send({
            "text": json.dumps({'clock': "true", 'countdown': data}),
        })

    def send_countdowninit(self):

        self.game_group.send({
            "text": json.dumps({'clockinit': "true"}),
        })

    def send_countdownfinish(self):

        self.game_group.send({
            "text": json.dumps({'clockfinish': "true"}),
        })

    def send_ready_players(self, user):
        msg = {'ready': "true", 'playername': user.username}

        self.game_group.send(
            {"text": json.dumps(msg)}
        )

    def clear_player(self, pid):

        p = Player.objects.get(id=pid)
        p.delete()

    def allCards(self):
        allcards = []
        deck = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
        s = ['H', 'D', 'C', 'S']
        for x in deck:
            for t in s:
                index = x + t
                allcards.append(index)

        return allcards

    def create_player(self, user):

        new_player = Player(playername=user.username, user=user, begin_chip=0,
                            chip_remain=0, game=self
                            )
        new_player.save()

        return new_player.id

    def game_players_dict(self, uid=None):

        all_players = []
        for p in self.player_set.all():
            if uid == p.user.id:
                continue
            all_players.append(p.to_dict())

        return all_players

    def startGame(self):

        allcards = self.allCards()

        deskcards = random.sample(set(allcards), 5)

        for card in deskcards:
            allcards.remove(card)

        i = 0
        self.update_dealer_pos()

        # the one next to big blind is the first one to move
        # in first round.
        self.current_player = (self.dealer + 3) % self.num_players()

        dealer = list(self.player_set.all())[self.dealer].playername

        # consider the sb, bb in the future.
        current_player = list(self.player_set.all())[self.current_player].playername

        # refill
        for player in self.player_set.all():
            # refill the chips, if empty
            print(player.playername+":"+str(player.begin_chip))
            if player.begin_chip == 0:
                player.begin_chip = self.buyin
                profile_p = player.user.profile
                profile_p.asset = profile_p.asset - self.buyin
                print("refill:" + player.playername+" left: "+str(profile_p.asset))
                profile_p.save()
                player.save()

            player.chip_remain = player.begin_chip
            player.save()


        for p in self.player_set.all():

            usercards = random.sample(set(allcards), 2)
            p.card_one = usercards[0]
            p.card_two = usercards[1]

            p_dict = p.to_dict()
            p_dict["start"] = "true"
            p_dict["card0"] = p.card_one
            p_dict["card1"] = p.card_two
            p_dict["dealer"] = dealer
            p_dict["current_player"] = current_player

            # all other player information list.
            all_players = self.game_players_dict(uid=p.user.id)
            p_dict["players"] = all_players

            if current_player == p.playername:
                p.is_round_play = True

            # p_dict["players"] = [all_players[j] for j in range(len(all_players)) if j != i]
            print(p.card_one)
            print(p.card_two)

            p.save()
            self.user_group(p.user).send({"text": json.dumps(p_dict)})

            for card in usercards:
                allcards.remove(card)

            i += 1

        for card in deskcards:
            c = Card.objects.get(card=card)
            self.cards_on_table.add(c)

        for card in allcards:
            c = Card.objects.get(card=card)
            self.cards_remain.add(c)

        self.save()

    ## update the number of max people in the future.
    def update_dealer_pos(self):
        self.dealer = (self.dealer + 1) % self.num_players()
        self.save()

    def update_current_player(self):
        self.current_player = (self.current_player + 1) % self.num_players()

        ## check if the current player is online.
        while not list(self.player_set.all())[self.current_player].is_online:
            print("find one leaving players!")
            p = list(self.player_set.all())[self.current_player]
            if p.state != "allin":
                p.state = "fold"
                p.begin_chip = 0
                p.chip_remain = 0
            p.save()

            self.current_player = (self.current_player + 1) % self.num_players()

        ## check if the online player is 'fold' or 'allin'.
        while list(self.player_set.all())[self.current_player].state == "fold" or \
                        list(self.player_set.all())[self.current_player].state == "allin":
            self.current_player = (self.current_player + 1) % self.num_players()

        self.save()

    def update_user_option(self, pid, cost, choice):

        p = get_object_or_404(Player, id=pid)

        p.is_round_play = True
        p.round_bet += cost
        p.accum_bet += cost

        # double check, can't have negative remain chip.
        p.chip_remain = max((p.begin_chip - p.accum_bet),0)
        print("bet:"+str(cost))
        # all in
        if p.chip_remain == 0:
            p.state = "allin"
        else:
            p.state = choice

        p.save()

        self.pot_size += cost
        self.update_max(p.round_bet)

        # if p.state == "fold" and p.playername == list(self.player_set.all())[self.current_player].playername:
        #     self.round_max_bet = -1

        cards_to_send = []
        if self.round_finish():
            print("Round Finish")
            if self.is_finish():
                print("finish")
                # game.clear_round_bet()
                self.save()
                self.game_finish()
                return True
            else:
                self.round_status += 1
                cards_to_send = self.deal_cards()
                self.clear_round_bet()

            self.current_player = (self.dealer) % self.num_players()

        self.update_current_player()
        self.save()

        # send data that are same for every player.
        res_dict = {}
        res_dict['update'] = "true"
        res_dict['pot_size'] = self.pot_size
        res_dict['current_player'] = list(self.player_set.all())[self.current_player].playername
        res_dict['desk'] = [c.card for c in cards_to_send]
        res_dict['round_max'] = max(self.round_max_bet, 0)

        # only update the current player info to everybody.
        res_dict['player'] = [p.to_dict()]

        # send data that are different for every player.
        for player in self.player_set.all():
            res_dict['playername'] = player.playername
            res_dict['player_min_bet'] = max(self.round_max_bet, 0) - player.round_bet
            res_dict['chip_remain'] = player.chip_remain
            self.user_group(player.user).send(
                {"text": json.dumps(res_dict)}, immediately=True
            )

        return False

    def update_user_fold(self, pid):

        p = get_object_or_404(Player, id=pid)
        p.state = "fold"
        p.is_round_play = True

        p.save()

        cards_to_send = []
        if self.round_finish():
            print("Round Finish")
            if self.is_finish():
                print("finish")
                # game.clear_round_bet()
                self.save()
                self.game_finish()
                return
            else:
                self.round_status += 1
                cards_to_send = self.deal_cards()
                self.clear_round_bet()

        self.update_current_player()
        self.save()

        res_dict = {}
        res_dict['update'] = "true"
        res_dict['pot_size'] = self.pot_size
        res_dict['current_player'] = list(self.player_set.all())[self.current_player].playername
        res_dict['desk'] = [c.card for c in cards_to_send]
        res_dict['round_max'] = max(self.round_max_bet, 0)
        res_dict['player'] = [p.to_dict()]

        for p in self.player_set.all():
            res_dict['playername'] = p.playername
            res_dict['player_min_bet'] = max(self.round_max_bet, 0) - p.round_bet

            self.user_group(p.user).send(
                {"text": json.dumps(res_dict)}, immediately=True
            )

    def game_finish(self):

        potsize = self.pot_size

        user_best_cards = []
        for p in self.player_set.all():
            ## ignore fold and off-line players
            if not p.is_online or p.state == "fold":
                continue
            card1 = p.card_one
            card2 = p.card_two

            cards = []

            for c in self.cards_on_table.all():
                cards.append(c.card)

            usercards = cards[:]
            usercards.append(card1)
            usercards.append(card2)

            usercombo = list(combinations(usercards, 5))
            maxusercombo = list(usercombo[0])
            for combo in usercombo[1:]:
                combo = list(combo)
                if getwinner(combo, maxusercombo) == combo:
                    maxusercombo = combo
            print("Player" + p.playername)
            print(maxusercombo)
            user_best_cards.append((p.playername, maxusercombo))

        winner_name = user_best_cards[0][0]
        winner_commbo = user_best_cards[0][1]

        for playername, maxcombo in user_best_cards:

            ## consider equal hands in the future.
            if getwinner(maxcombo, winner_commbo) == maxcombo:
                winner_commbo = maxcombo
                winner_name = playername

        result_dict = {}
        result_dict["finish"] = "true"
        result_dict["winner"] = winner_name
        result_dict["pot_size"] = potsize
        result_dict['desk'] = [c.card for c in self.deal_cards(fixed=5)]

        player_list = []

        ## needs to consider side pot and fold players.
        for p in self.player_set.all():
            if not p.is_online:
                self.clear_player(p.id)
                # p.delete()
                continue
            if p.playername == winner_name:
                p.chip_remain += potsize

            p.reset()
            p.save()
            player_list.append(p.show_hands())

        result_dict["players"] = player_list

        self.game_group.send(
            {"text": json.dumps(result_dict)}, immediately=True
        )

        self.reset()
        self.save()
