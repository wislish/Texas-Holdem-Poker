from channels import route
from poker.consumers import *

channel_routing = [
    # Called when incoming WebSockets connect
    route("websocket.connect", ws_add, path=r'^/wbconnect/(?P<roomid>[0-9]+)/$'),

    route("websocket.receive", ws_message),

    # Called when the client closes the socket
    route("websocket.disconnect", ws_disconnect),

    route("game.update", ws_game_start, command="^start$"),
    route("game.update", ws_game_update, command="^update$"),
    route("game.update", ws_game_chat, command="^chat$"),
]