
## Project Intro - Daily Hold'em

An online Texas Hold’em Poker entertainment platform with extra features. The rules can be found at https://en.wikipedia.org/wiki/Texas_hold_%27em.

**Basic functions:**
The users may be able to create their account, login and start a game.

Several users input a certain room id and they will be in the same game. Different games can process concurrently.

Each user may have an initial credit for each game, and after each round of game, the credit will be updated.
 
We don’t need all players to establish an agreement before they leave. They can simply find a room, sit, play and leave whenever they want. Users can chat with each other in a game room.

Users can **rejoin the game** if they become disconnected. 

**Completed extra features**:

* **Credits**: Redeeming coupons, recharging credits, etc.
* **Online chatting**: Texting.
* **Login and registration**
* **Game Modes**: Human VS machine; 
* **Sound Effect**


### Data Models(First Version)

![Data Model](http://otmtp4cwc.bkt.clouddn.com/datamodel.png)


___

## Code

1. Database Model design and implementation. (`dailypoker/poker/models.py` )
2. Respond to user requests, which means to start the game, update the game status and finish the game.(`dailypoker/poker/views.py`)
3. Websocket duplex communication, including reconnect the game if lost. (`dailypoker/poker/consumers.py`)


## Explanation

1. Group project. You can find more information at the `specification` directory. We use Scrum development to split our whole project into three Sprint. 
2. Database design. To make sure all the relevant information as to one game and one player are stored, because users can **rejoin** the game if they lost the connection. Additionally, all the necessary operations for updating one game are under the model `Game` and `Player`, improving the maintainability and readability. 
3. Build `channel` between clients and the server through the WebSocket. So, the server can actively send messages to clients. 
4. Perform extensive testing. Texas Hold’em Poker has many subtle but important rules. Once completed the basic implementation, we conducted enormous testing manually. In the future, it is a better idea to use Django test module. 



 


