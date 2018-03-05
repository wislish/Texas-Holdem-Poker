# Product Specification

## Original Proposal

### Texas Hold'em Poker

An online Texas Hold’em Poker entertainment platform with extra features. The rules can be found at https://en.wikipedia.org/wiki/Texas_hold_%27em.

Basic functions:
The users may be able to create their account, login and start a game.
Several users input a certain room id and they will be in the same game. Different games can process concurrently.
Each user may have an initial credit for each game, and after each round of game, the credit will be updated. After all the users agreed to exit the game, a scoreboard will be posted.

Possible extra features (to be discussed):

* Credits: Redeeming coupons, recharging credits, etc.
* Social: Searching for a user, making friends, starting a game with a friend, etc.
* Online chatting: Texting, sending images, Voice2Text, voice mail, etc
* Login and registration: Changing avatar, changing passwords, Facebook Login, etc.
Ranking: Scoreboards, matching players of similar levels, etc.
* Dashboard: Checking personal history, comparing to global MAX, MEDIAN, MEAN, etc
* Game Modes: Human VS machine; matching different rooms according to initial credit(i.e. 100 credits/ 200 credits); matching different rooms according to the preferred number of players(i.e. 4P rooms/10P rooms); ...


### Feedback From Course Staff
Games generally provide a good opportunity for an excellent final project, but games also pose some risks. Specifically, ensure that your game interactions and server-side components are sufficiently complex to allow all your team members to demonstrate the fundamental learning goals of the course.

To achieve this, we recommend:

* **Include real-time interactions between the web server and between players if possible**, using a technology such as WebSockets. Do not rely on a player to reload the page to receive information about other players' turns. It's possible to mimic real-time interactions using repeated polling with Ajax -- we'll see this in class soon! -- but repeated polling with Ajax artificially delays the updates and can impose high cost on the web server, compared to true real-time technologies such as WebSockets.
* **Be sure that your server-side data representation is non-trivial**, e.g. that your application persistently stores (in the database) the game state after each player's move. Do not just implement the game as an in-memory component running at the web server. Ideally, a player should be able to rejoin the game (and see the current state) if they become disconnected from a game.

Game projects in the past have failed for various reasons. **Common problems** are:

* The team spends too many development resources on the game implementation itself, rather than on the web applications-related portions of the project. This is a serious risk because the game implementation itself is usually a substantial task, and the project usually fails if the game is inadequately implemented.
* The data model at the application server is insufficiently rich to allow all team members to demonstrate the key learning goals of the course. Do not just store simple data at the server, such as player accounts and game scores, etc. Do not try to increase the complexity of your application by adding Grumblr-like social networking features; the result would be incohesive.

To maximize your chance of success, plan your development so that you can demonstrate a fully working implementation (including interesting data interactions and real-time interactions, as possible) for portions of the game early in the project, even for Sprint 1. E.g., Have a fully-working game that allows two players to play a subset of Texas Hold'em (perhaps without betting) by Sprint 1, with the game state after each turn being stored in the database and WebSockets being used to transmit information about the other player's move. **Do not include unrelated features such as player accounts, unless the game is otherwise fully implemented.**


## Modified Proposal
### Daily Hold'em

An online Texas Hold’em Poker entertainment platform with extra features. The rules can be found at https://en.wikipedia.org/wiki/Texas_hold_%27em.

**Basic functions:**
The users may be able to create their account, login and start a game.

Several users input a certain room id and they will be in the same game. Different games can process concurrently.

Each user may have an initial credit for each game, and after each round of game, the credit will be updated.
 
We don’t need all players to establish an agreement before they leave. They can simply find a room, sit, play and leave whenever they want. Users can chat with each other in a game room.

Users can **rejoin the game** if they become disconnected. 

**Possible extra features** (to be discussed):

* **Credits**: Redeeming coupons, recharging credits, etc.
* **Social**: Searching for a user, making friends, starting a game with a friend, etc.
* **Online chatting**: Texting, sending images, Voice2Text, voice mail, etc
* **Login and registration**: Changing avatar, changing passwords, Facebook Login, etc.
Ranking: Scoreboards, matching players of similar levels, etc.
* **Dashboard**: Checking personal history, comparing to global MAX, MEDIAN, MEAN, etc
* **Game Modes**: Human VS machine; matching different rooms according to initial credit(i.e. 100 credits/ 200 credits); matching different rooms according to the preferred number of players(i.e. 4P rooms/10P rooms); ...


## Product Backlog
This section describes the initial functionality for the Scrum Daily Hold'em website. It lists everything that Scrum team feels should be included in the webapp they are developing in a Scrum environment.

Please see **ProductBacklog.xlsx** for detail information

![backlog](http://otmtp4cwc.bkt.clouddn.com/backlog.png)

## Task Distribution

### User System

* Basic UI Implementation
* Login and Registration Page
* Global Stream Page
* UI Improvement
* Home Page and Ranking Page

### PokerApp System

* Poker Rules (deck, hand evaluation and compare hands)
* Subset I of Texas Hold'em (1 vs 1, deal and act)
	* Player Action
	* UI Implementation
	* Server Action
	* Data Model
* Subset II of Texas Hold'em (Action: Fold, Call)
	* Player Action
	* UI Implementation
	* Server Action
	* Data Model
	* Autoplayer (act based on probability)
* Full Version of Texas Hold'em (Added Action: Check, Bet)
	* Player Action
	* UI Implementation
	* Server Action
	* Data Model


### Chatting System

* Online chatting by text
* Online chatting support emoticon


## Data Models

![Data Model](http://otmtp4cwc.bkt.clouddn.com/datamodel.png)

____

`Game`: We define one record of a **Game** or one object of a **Game** model as one Hold'em Poker game from players receive the cards to one or two players win the pot. 

`User`: User model records the basic account information as well as the chips or credits information.

`Players`: A Player is a user in a specific game, with some amount of chips. 

`Cards`: Cards Model records 52 kinds of card that will be used in the game. 


## Wireframes

#### Login
___
![Login](http://otmtp4cwc.bkt.clouddn.com/Login.png)

___

#### Register

![Register](http://otmtp4cwc.bkt.clouddn.com/register.png)


____


#### Rank

![rank](http://otmtp4cwc.bkt.clouddn.com/Player_Rank.png)

#### Game List

![Game List](http://otmtp4cwc.bkt.clouddn.com/game_list.png)

___

#### Create Game

![Create](http://otmtp4cwc.bkt.clouddn.com/choose_game.png)

___

#### Game
![Game](http://otmtp4cwc.bkt.clouddn.com/game_page.png)






