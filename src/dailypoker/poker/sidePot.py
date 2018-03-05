def sidePot(game,winnername):
    for p in game.player_set.all():
        if p.state == "fold":
            continue

        