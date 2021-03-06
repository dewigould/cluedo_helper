import pandas as pd
from collections import Counter
import numpy as np

class CluedoGame:

    guests = ["Mustard", "Plum", "Green", "Peacock", "Scarlet", "White"]
    weapons = ["Knife", "Candlestick", "Pistol", "Poison", "Trophy", "Rope", "Bat", "Axe", "Dumbbell"]
    rooms = ["Hall", "Dining Room", "Kitchen", "Patio", "Observatory", "Theatre", "Living Room", "Spa", "Guest House"]
    game_config = {'guests': guests,'weapons': weapons, 'rooms': rooms}
    num_guests = len(guests)
    num_weapons = len(weapons)
    num_rooms = len(rooms)

    def __init__(self, user_name, user_cards,  other_player_names):
    
        self.all_names = other_player_names+[user_name]
        self.num_players = len(self.all_names)
        self.set_up_board_tracker(user_name, user_cards, other_player_names)


    def set_up_board_tracker(self, user_name, user_cards, other_player_names):
        room_tracker = pd.DataFrame(zip(CluedoGame.rooms, ['room']*CluedoGame.num_rooms),columns=['cards','card_type'])
        guest_tracker = pd.DataFrame(zip(CluedoGame.guests, ['guest']*CluedoGame.num_guests),columns=['cards','card_type'])
        weapon_tracker = pd.DataFrame(zip(CluedoGame.weapons, ['weapon']*CluedoGame.num_weapons),columns=['cards','card_type'])  
        for name in self.all_names:
            room_tracker[name] = ['no_info']*CluedoGame.num_rooms
            guest_tracker[name] = ['no_info']*CluedoGame.num_guests
            weapon_tracker[name] = ['no_info']*CluedoGame.num_weapons

        guest_tracker.index = guest_tracker.cards
        del guest_tracker['cards']
        room_tracker.index = room_tracker.cards
        del room_tracker['cards']
        weapon_tracker.index = weapon_tracker.cards
        del weapon_tracker['cards']   
        self.board_tracker = pd.concat([room_tracker, guest_tracker, weapon_tracker])
        self.hedges = {i:[] for i in self.all_names}

        self.add_definite_cards(user_name, user_cards)

        cards_user_doesnt_have = [i for i in CluedoGame.guests if i not in user_cards] + \
                                 [i for i in CluedoGame.rooms if i not in user_cards] + \
                                 [i for i in CluedoGame.weapons if i not in user_cards]
        
        self.doesnt_have_cards(user_name,cards_user_doesnt_have)

    
    def add_definite_cards(self, name, cards):
        for card in cards:
            self.board_tracker.at[card,name] = 1.0
            self.remove_card_from_names_hedge(name, card)
            for other in self.all_names:
                if other != name:
                    self.board_tracker.at[card, other] = 0.0
                    self.remove_card_from_names_hedge(other, card)

    def doesnt_have_cards(self, name, cards):
        for card in cards:
            self.board_tracker.at[card,name] = 0.0
            self.remove_card_from_names_hedge(name,card)
 
    def add_options(self, name, cards):
        priors = [self.board_tracker.at[card,name] for card in cards]
        unknowns = [card for card in cards if self.board_tracker.at[card, name] == 'no_info']
        num_unknowns = priors.count("no_info")
        if num_unknowns >0 and 1.0 not in priors:
            self.hedges[name].append(unknowns)

    def remove_card_from_names_hedge(self, name, card):
        for hedge in self.hedges[name]:
            if card in hedge:
                hedge.remove(card)
            if len(hedge) == 1:
                self.board_tracker.at[hedge[0],name] = 1.0
                #Here I changed it
                for other in self.all_names:
                    if other != name:
                        self.board_tracker.at[hedge[0], other] = 0.0
                hedge.remove(hedge[0])


    def my_turn_suggestion(self):

        if len(self.check_for_certainties()[1]) == 3:
            return "Make accusation", self.check_for_certainties()[1]
         
        suggestions = []

        options = []
        all_hedges = []
        for hedges in self.hedges.values():
            all_hedges += hedges
        for hedges in all_hedges:
            options += hedges
        options = Counter(options).most_common()
        
        if len(options) == 0:
            return "Just guess a random selection of cards you don't have"

        for cards in [CluedoGame.rooms, CluedoGame.weapons, CluedoGame.guests]:
            found = False
            count = 0
            while not found and count <len(options):
                if options[count][0] in cards:
                    suggestions.append(options[count][0])
                    found = True
                else:
                    count +=1
        if len(suggestions) == 2:
            return "Go for these two & a random selection out of your knowns, or if you don't have any..the unkowns", suggestions
        return suggestions



    def check_for_certainties(self):
        output = []
        for card_type in ['room','weapon','guest']:
            subset = self.board_tracker.loc[self.board_tracker['card_type'] == card_type][self.all_names]
            m1 = subset.eq(0).all(axis=1)
            if True in m1.values:
                answer = m1[m1==True].index[0]
                output.append(answer)
        return "Answers are:", output

    def see_progress(self):
        print(self.check_for_certainties())
        return self.board_tracker









        








        

