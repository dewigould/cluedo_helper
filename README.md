# cluedo_helper
computer-assisted cluedo cheating, motivate by aggressive family games under lock-down.


## Set up.
- Code user inputs name as `user_name`, their initial cards as `user_cards` and other player names as `other_player_names`
- guests, rooms, weapons are all class variables. Change as follows to match specific version:

```
game = CluedoGame(user_name, user_cards, other_players)
game.guests = ['guest1','guest2',...]
game.weapons = ['weapon1','weapon2'...]
game.rooms = ['room1', 'room2',...]
```

## Playing the game.
The process has three key options:
- `add_definite_cards`
- `doesnt_have_cards`
- `add_options`

If another players shows you a card during your turn:
```
game.add_definite_cards("me",[the_card])
```

If a player is unable to help you, or someone else, during a turn, then you know for certain that they don't have the three cards forming the guess:
```
game.doesnt_have_cards("person",[the_cards])
```

If a player is able to help someone else, you know they must have one, two or all three of the cards forming the guess:
```
game.add_options("person",[the_cards])
```

For your turn: `game.my_turn_suggestion` will return any options you should guess that will maximise the information you will recieve during your turn. This uses the fact that there will be lots of hedges that can be solved with a single new piece of information - so we try and solve as many hedges as possible per turn.

## The algorithm.
`CluedoGame.board_tracker` keeps track of all cards: showing `0` if someone definitely doesn't have that card, `1` if they definitely do have it and `no_info` if there is no definitive information.
`CluedoGame.hedges` is the key step that will enable quicker learning -  it keeps track of all `add_options` function calls, so that new information can be used to solve earlier doubts.

For example, user1 is able to help user2 in some way - and you know that user1 must have one of two cards (as you have the third one). Later on, user1 is unable to help user3 with a guess invovling one of those two cards - you therefore know with certainty that user1 must have the other card. There are other permutations and situations here, all of which are included in this method.

