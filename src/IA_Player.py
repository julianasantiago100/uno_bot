import random
from Card import Card
from Player import Player

#generalist class of IA_Player

class IA_Player():
    
    def __init__(self, name, uno_machine):
        self.me_player = Player(name)
        self.UNO_MACHINE = uno_machine
        
    def get_player(self):
        return self.me_player
    
    def receive_first_hand(self,cards):
        self.me_player.my_cards = cards
        
    def throw_card_away(self,card):
        self.me_player.throw_a_card(card) #deleting in player's hand
        self.UNO_MACHINE.discart_a_card(card) #adding to the discart pile

    def draw_from_deck(self,card):
       self.me_player.take_a_new_card(card)
       
    def move(self) -> Card : # the player's move
        list_of_possible_throws = self.possible_throws()
        return_card = None
        
        if(len(list_of_possible_throws) == 0): #user takes another card
            new_card = self.UNO_MACHINE.take_new_card_from_deck()
            self.draw_from_deck(new_card)
            
            if(self.UNO_MACHINE.card_can_be_throw(new_card)):
                return_card = new_card
                self.throw_card_away(new_card)
        else:  
            aleatory_card = self.player_strategy_which_card(list_of_possible_throws)
            
            return_card =  aleatory_card[0]
            self.throw_card_away(aleatory_card[0])

        return return_card
    
    def possible_throws(self): #retorna a lista de possíveis jogadas
        list_of_possible_throws = []
        for play_card in self.me_player.my_cards:
            if(self.UNO_MACHINE.card_can_be_throw(play_card)):
                list_of_possible_throws.append(play_card)
        return list_of_possible_throws
    
    def player_strategy_which_card(self,list_of_possible_throws):
        return random.sample(list_of_possible_throws,1) #pega uma aleatória entre as possíveis
        