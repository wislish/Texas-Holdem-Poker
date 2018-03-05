from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user
from channels.sessions import channel_session
from django.shortcuts import get_object_or_404

from .models import *
import json
from channels import Channel


# Connected to websocket.connect
@channel_session_user_from_http
def ws_add(message, roomid):
    try:
        gameroom = Game.objects.get(id=roomid)

    except Game.DoesNotExist:

        message.reply_channel.send({

            "text": json.dumps({"error": "wrong id"}),
            "close": True,
        })
        return

    # Accept.
    message.reply_channel.send({"accept": True})
    message.channel_session['game_rooms'] = gameroom.id

    find_pid = gameroom.is_contain_player(message.user)

    if find_pid:
        message.channel_session['pid'] = find_pid

        # send update information to already connected players.
        gameroom.send_join(message.user)

        # add to group.
        gameroom.game_group.add(message.reply_channel)

        # single user group to accept individual message.
        gameroom.user_group(message.user).add(message.reply_channel)

        #  reconnected player.
        gameroom.send_reconnect(message.user, find_pid)
        gameroom.save()
        return

    else:
        # create new player.
        pid = gameroom.create_player(message.user)
        message.channel_session['pid'] = pid

        # send update information to already connected players.
        gameroom.send_join(message.user)

        # add to group.
        gameroom.game_group.add(message.reply_channel)

        # single user group to accept individual message.
        gameroom.user_group(message.user).add(message.reply_channel)

        # send initial information to new connected player.
        gameroom.send_init(message.user)
        gameroom.save()


@channel_session_user
def ws_message(message):
    ## copy from channels-example, redirect to other channels.
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel("game.update").send(payload)


@channel_session_user
def ws_game_start(message):
    game_id = message.channel_session.get("game_rooms")

    try:
        gameroom = Game.objects.get(id=game_id)
        gameroom.num_start += 1
        print(gameroom.num_start)
        print(gameroom.num_players())
        pid = message.channel_session['pid']
        p = get_object_or_404(Player, id=pid)

        p.is_online = True
        p.save()
        gameroom.save()

        if gameroom.num_start == gameroom.num_players() and gameroom.num_players()!= 1:
            gameroom.is_start = True
            gameroom.startGame()
            clock(30, game_id)
        else:
            gameroom.send_ready_players(message.user)

    except Game.DoesNotExist:

        message.reply_channel.send({

            "text": json.dumps({"error": "wrong id"}),
            "close": True,
        })
        return


@channel_session_user
def ws_game_update(message):
    game_id = message.channel_session.get("game_rooms")

    try:
        gameroom = Game.objects.get(id=game_id)

        stop_clock(game_id)

        is_finished = gameroom.update_user_option(message.channel_session.get("pid"), int(message['cost']), message['choice'])
        # print is_finished
        if not is_finished:
            time.sleep(1)
            clock(29, game_id)
        else:
            stop_clock(game_id)

    except Game.DoesNotExist:

        message.reply_channel.send({

            "text": json.dumps({"error": "wrong id"}),
            "close": True,
        })
        return


@channel_session_user
def ws_disconnect(message):
    try:
        game_id = message.channel_session.get("game_rooms")
        pid = message.channel_session.get("pid")

        gameroom = Game.objects.get(id=game_id)
        p = Player.objects.get(id=pid)

        p.user.profile.asset = p.user.profile.asset + p.chip_remain
        p.user.profile.save()

        # remove from Channels Group.
        gameroom.game_group.discard(message.reply_channel)
        gameroom.user_group(message.user).discard(message.reply_channel)

        # send leave message to other users.
        gameroom.send_leave(message.user)

        if gameroom.is_start:
            p.is_online = False
            p.save()
            # if the current player is leaving, move to the next player.
            if p.playername == list(gameroom.player_set.all())[gameroom.current_player].playername:
                p.state = "fold"
                p.begin_chip = 0
                p.chip_remain = 0
                p.save()
                # if only one player not offline or fold,finish the game.
                if gameroom.is_finish():
                    gameroom.game_finish()
                    gameroom.save()
                    if gameroom.num_players() == gameroom.num_offline_players() or gameroom.num_players() == 0:
                        gameroom.delete()
                    return
                # if not finish, update the betting and move on.
                gameroom.update_user_option(pid,0,"offline")
            gameroom.save()
        else:
            if p.is_online:
                gameroom.num_start -= 1
            gameroom.clear_player(pid)
            gameroom.save()
            if gameroom.num_players() == 0:
                gameroom.delete()
                return

        stop_clock(game_id)


    except Game.DoesNotExist:
        pass


def ws_clockinit(gid):
    gameroom = Game.objects.get(id=gid)
    gameroom.send_countdowninit()


def ws_clockfinish(gid):
    gameroom = Game.objects.get(id=gid)
    gameroom.send_countdownfinish()


def ws_clock(data, gid):
    gameroom = Game.objects.get(id=gid)
    gameroom.send_countdown(data)
    # gameroom.game_group.send({
    #     "text": json.dumps({'clock': "true", 'countdown': data}),
    # })


@channel_session_user
def ws_game_chat(message):
    print('chat')
    game_id = message.channel_session.get("game_rooms")
    pid = message.channel_session.get("pid")
    player = Player.objects.get(id=pid)
    # payload = json.loads(message['content'])
    payload = {}
    payload['chat'] = "true"
    payload['name'] = player.playername
    payload['ms'] = message['ms']
    gameroom = Game.objects.get(id=game_id)
    gameroom.game_group.send({'text': json.dumps(payload)})


import threading
import time


def clock(num, gid):
    start_count = int(num) - 1  # from num to 0, totally num times
    clock_dic[gid] = False
    prints = PrintThread(start_count, gid)
    prints.start()


clock_dic = {}


def stop_clock(gid):
    clock_dic[gid] = True


class PrintThread(threading.Thread):
    def __init__(self, start_count, gid):
        super(PrintThread, self).__init__()
        self.start_count = start_count
        self.gid = gid

    def run(self):
        print ("start.... %s" % (self.getName(),))
        ws_clockinit(self.gid)
        clock_dic[self.gid] = False
        for i in range(self.start_count, -1, -1):
            if clock_dic[self.gid]:
                ws_clock(self.start_count, self.gid)
                ws_clockfinish(self.gid)
                break
            time.sleep(1)
            ws_clock(i, self.gid)
            print (i)
        print ("end.... %s" % (self.getName(),))
