## Process

### Test 3000局
1. 正常玩 no accident
2. 玩第二局 play another game.
3. count down clock
4. 退出 disconnect and reconnect 
    * 还没轮到自己就赶回来 rejoin before your turn
    * 赶回来时 已经晚了 rejoin after your turn
    * 轮到自己时推出，离开 exit, never be back
    * 错过本局 无法在第二局再回来。 miss this round, can't rejoin.

      
### Bugs

1. multi winner,side-pot,~~allin~~
3. ~~每一轮开始前bet 0 （或者check），当前轮直接结束。~~
4. ~~每一个round，玩家bet不能小于当前最大值。~~ (start phase)
5. 玩家中途离开，保持用户出牌顺序的合理性。
6. ~~断线重连。~~
    * ~~断线后不回来了。~~
        * ~~庄家断线。~~
    * ~~轮到自己的时候掉线了~~   
    * ~~还没轮到自己出牌就回来,接着玩儿~~
    * ~~过了自己出牌,回来(观看比赛)~~
7. 大小盲
8. 结束时翻牌,只显示剩余玩家的手牌。
9. ~~只剩一个玩家时，游戏胜利，并结束。~~
11. ~~fold 后负数~~
12. ~~可以负数接着玩~~
13. ~~所有人退出时，无限循环。~~
14. 出牌顺序。
15. 筹码显示。每次下注，有显示。可以是一行文字。
16. ~~0块钱,自动fold. (前一把自动all-in)~~
17. ~~剩余钱不够下注，all-in 或者 fold.~~
18. After test, add gameroom.num_players()!= 1
19. 退出功能。
20. ~~all-in 后断线。其他功能测试。~~(后续测试)
21. ~~每次游戏结束，refill remain chip为0的玩家。~~
22. ~~翻盘前后玩家的游戏顺序。~~
23. 用户状态。


#### 1. User Click Creation Or join.
`Client`: establish websocket connection, through JS.

```
URL: /wbconnect/(?P<roomid>[0-9]+)/$
Data: None
```
`Server`: Add to Group, record user session. Model Operation. 

```
Accept the connection.
```

#### 2. User click start
`Client`: Send message to Server, indicating it is ready.

```
URL: None. Just send. (webSocketBridge.send({data}))
Data: {"command":"start","gid":"gameid"}
```
`Server`: Update Model, init a new game if suitable.
**Indicating users who are ready to play.**

```
{"players":[{"name":playername,"BeginChip":BeginChip},{...}]}

```

#### 3. Other Users leave or join the game room, before start.

`Client`: No need to send data, just receive.

`Server`: Send back current leaving or joining username.

```
`JOIN`:
{"join":"True","name":"playername","beginChip":beginChip}

`LEAVE`:
{"leave":"True","name":"playername"}

```

#### 4. Server Start Game
`Client`: Nothing, receive.

`Server`:

![](media/initgame.png)



#### 5. User Update (Check, call, raise, fold)
`Client`: Send Json message.

```
{"pid":pid,"choice":choice,"cost":cost}
``` 

`Server`: Update
![](media/update.png)

#### 6. User Re-Connect

Leave:
    1. Delete Group
    2. is_offline: true

Re-Join: 选择房间后／自动转入相应的游戏。
    1. see if its turn is over.
        yes, online - fold
        no, online, continue to play
    








