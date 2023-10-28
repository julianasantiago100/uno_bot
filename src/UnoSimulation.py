from dataclasses import dataclass
from src.Card import Card
from src.CircularVector import CircularVector
from src.Machine import Machine

@dataclass
class SimulationOutputData:
    winner: str
    first_players_hands: list[list[str]]
    
@dataclass
class SimulationInputData:
    bot: Machine
    round_players: CircularVector
    number_of_players: int
    players_cards: list[list[Card]]

class UnoSimulation:
    
    STATUS_CAN_PLAY = False
    IS_ANALYSING_DATA = True
     
    def __init__(self,input:SimulationInputData):
        self.bot = input.bot
        self.number_of_players = input.number_of_players
        self.verify_initial_parameters()
        
        if(self.STATUS_CAN_PLAY):
            print('iUp')
            self.IA_PLAYERS_CIRCULAR_VECTOR = input.round_players
            self.INITIAL_PLAYERS_CARDS = input.players_cards
            self.initialize_players(self.INITIAL_PLAYERS_CARDS)
    
    def verify_initial_parameters(self):
        self.STATUS_CAN_PLAY = self.bot.can_this_number_of_players_play_uno(self.number_of_players)
    
    def initialize_players(self,player_cards): 
        i = 0
        for ia_player in self.IA_PLAYERS_CIRCULAR_VECTOR.vector:
            #insert bot into ia_player
            ia_player.insert_uno_machine(self.bot)
            
            #insert cards into players
            cards = player_cards[i]
            ia_player.player.setcards(cards)
            i += 1
            
    def reset_simulation(self):
        print(len(self.INITIAL_PLAYERS_CARDS[0]))
        self.bot.reset_machine(self.INITIAL_PLAYERS_CARDS.copy())
        
        for ia_player in self.IA_PLAYERS_CIRCULAR_VECTOR.vector:
            ia_player.reset_ia_player()
            
        self.initialize_players(self.INITIAL_PLAYERS_CARDS.copy())

        self.CARD_ON_THE_TABLE = None
        self.CURRENTLY_PLAYER = []
        
    def initialize_game_with_first_card(self):
        self.CARD_ON_THE_TABLE =  self.bot.get_game_first_card()
        
    def update_currently_player(self):
        self.CURRENTLY_PLAYER = self.IA_PLAYERS_CIRCULAR_VECTOR.get_ia_player_by_index(self.bot.INDEX_WHO_IS_PLAYING)
        
    def round(self) -> SimulationOutputData:
        if self.STATUS_CAN_PLAY:
            
            self.bot.shuffle_cards()
            self.initialize_game_with_first_card()
            
            while(True):
                self.update_currently_player()
                self.bot.check_if_deck_is_empty_and_refuel_deck()
                
                ##
                next_player_number_of_cards = len(self.IA_PLAYERS_CIRCULAR_VECTOR.get_ia_player_by_index(self.bot.INDEX_WHO_IS_PLAYING+1).get_player().cards)
                self.CURRENTLY_PLAYER.get_other_players_number_of_cards(next_player_number_of_cards)
                ##
                
                card_thrown = self.CURRENTLY_PLAYER.move()
                player_passed_their_turn = card_thrown == None
                
                if not player_passed_their_turn:
                    self.CARD_ON_THE_TABLE = card_thrown
                    
                    if(self.player_has_won()): #simulation 
                        name = self.CURRENTLY_PLAYER.get_player_name()
                        return self.simulation_data(name)
                
                    card_thrown.execute_move(self.bot,self.IA_PLAYERS_CIRCULAR_VECTOR)
                          
                self.bot.INDEX_WHO_IS_PLAYING += 1
        else:
            return None
                
    def player_has_won(self):
        return self.bot.winner(self.CURRENTLY_PLAYER.get_player_cards())
                            
    def simulation_data(self,name):
        initial_hands = []
        player_h = []
        
        for player_cards in self.INITIAL_PLAYERS_CARDS:
            for card in player_cards:
                player_h.append(str(card))
            initial_hands.append(player_h)

        out = SimulationOutputData(name,initial_hands)
        self.reset_simulation() #reset the simulation
        return out

    def print_cant_run_UNO_error_message(self):
        print("Sorry. The number of players is either exceding the limit or under the minimum number")