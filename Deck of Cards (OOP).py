from random import randint
class DeckOfCards:
    original_deck = None
    current_players = 0

    def __init__(self, deck: list) -> None:
        if type(deck) != list:
            raise Exception("'deck' argument must be a list.")
        
        self.deck = deck
        DeckOfCards.original_deck = deck.copy()
        self.players = {}
     
    def add_players(self, num_players: int) -> None:
        for x in range(DeckOfCards.current_players + 1, DeckOfCards.current_players + num_players + 1):
            DeckOfCards.current_players += 1
            self.players[f"Player {x}"] = []

    # num_of_players can be an int or list
    # int will remove that many players
    # list will remove a specific set of players
    def remove_players(self, num_of_players: int | list) -> dict:
        if type(num_of_players) == int:
            for x in range(0, num_of_players):
                self.players.popitem()

        if type(num_of_players) ==  list:
            for player_num in num_of_players:
                self.players.pop(f"Player {player_num}")

        return self.players
    
    # Fisher–Yates shuffle
    # https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle#Python_implementation:~:text=H%20B%20F.-,Python%20implementation,-%5Bedit%5D
    def shuffle(self) -> None:
        for i in range(len(self.deck) - 1, 0, -1):
            j = randint(0, i)
            self.deck[i], self.deck[j] = self.deck[j], self.deck[i]
    
    def deal(self, cards_per_player: int) -> None:
        if DeckOfCards.current_players == 0:
            raise Exception(f"There are {DeckOfCards.current_players} players to deal cards to.")

        if DeckOfCards.current_players * cards_per_player > len(self.deck):
            raise Exception(f"Not enough cards for {DeckOfCards.current_players} players.")
 
        # Assigns each key a card once, then repeats for cards_per_player  
        for x in range(cards_per_player):
            for player in self.players:
                self.players[player].append(self.deck[0])
                self.deck.pop(0)

    def draw(self, player_num: int = 0, num_cards_to_draw: int = 1, dealer=False) -> None:
        if DeckOfCards.current_players == 0:
            raise Exception(f"There are {DeckOfCards.current_players} players to draw cards.")
        
        if dealer == True:
            key = f"Dealer"
        else:
            key = f"Player {player_num}"

        for x in range(0, num_cards_to_draw):
            self.players[key].append(self.deck[0])
            self.deck.pop(0)    
    
    def reset(self) -> None:
        self.deck = DeckOfCards.original_deck

    def cards_left(self) -> int:
        for cards_left, card in enumerate(range(0, len(self.deck) + 1)):
            continue
        
        return cards_left

    def change_deck(self, new_deck: list) -> None:
        if type(new_deck) != list:
            raise Exception("change_deck() takes a list argument only.")
        else:
            DeckOfCards.original_deck = new_deck.copy()
            self.deck = new_deck
            
    # Cuts the deck at a position, cuts in a random position if not specified
    def cut(self, position=None):
        print('cut')

    # Removes the top card, or multiple if specified
    def burn(self, num_cards=1):
        pass
    
    # Shows the top card, or multiple if specified
    def peek(self, num_cards=1):
        pass

    # Sorts a player's hand
    def sort(self, player_num):
        pass

    # Returns a player's cards to the bottom of the deck
    def return_player_cards(self):
        pass

    # Return the value of a player's hand
    def hand_value(self):
        pass

    # Compare two or more player's hand and return the player with the highest
    def compare_hands(self):
        pass


class Blackjack(DeckOfCards):
    def __init__(self, deck):
        super().__init__(deck)
        self.players["Dealer"] = []
    
    def play(self):
        print("♠ ♥ Blackjack ♦ ♣")
        command = None

        while command != "quit":
            command = input("Type hit, stand, or quit.\n").lower().strip()
       
            while command != "hit" and command != "stand" and command != "quit":
                command = input("Type hit, stand, or quit.\n")
            if command == "hit":
                print(self.hit(1))
                print(self.evaluate_hand(1))
            
            # -1 = Dealer
            print(self.hit(dealer=True))
            print(self.evaluate_hand(dealer=True))

    # player_num can be an int or list
    def evaluate_hand(self, player_num: int | list = 0, dealer=False) -> str:
        if dealer == True:
            hand_value = 0
            for card in self.players["Dealer"]:
                if "2" in card:
                    hand_value += 2
                elif "3" in card:
                    hand_value += 3
                elif "4" in card:
                    hand_value += 4
                elif "5" in card:
                    hand_value += 5
                elif "6" in card:
                    hand_value += 6
                elif "7" in card:
                    hand_value += 7
                elif "8" in card:
                    hand_value += 8
                elif "9" in card:
                    hand_value += 9
                elif "10" in card:
                    hand_value += 10
                elif "J" in card:
                    hand_value += 10
                elif "Q" in card:
                    hand_value += 10
                elif "K" in card:
                    hand_value += 10

            for card in self.players["Dealer"]:
                if "A" in card:
                    if hand_value <= 10:
                        hand_value += 11
                    else:
                        hand_value += 1
            
            result = f"Dealer's hand is currently worth {hand_value}."

        elif type(player_num) == int:
            hand_value = 0
            for card in self.players[f"Player {player_num}"]:
                if "2" in card:
                    hand_value += 2
                elif "3" in card:
                    hand_value += 3
                elif "4" in card:
                    hand_value += 4
                elif "5" in card:
                    hand_value += 5
                elif "6" in card:
                    hand_value += 6
                elif "7" in card:
                    hand_value += 7
                elif "8" in card:
                    hand_value += 8
                elif "9" in card:
                    hand_value += 9
                elif "10" in card:
                    hand_value += 10
                elif "J" in card:
                    hand_value += 10
                elif "Q" in card:
                    hand_value += 10
                elif "K" in card:
                    hand_value += 10
            
            for card in self.players[f"Player {player_num}"]:
                if "A" in card:
                    if hand_value <= 10:
                        hand_value += 11
                    else:
                        hand_value += 1

            result = f"Player {player_num}'s hand is currently worth {hand_value}."
        
        elif type(player_num) == list:
            result = []
            for player in player_num:
                hand_value = 0
                for card in self.players[f"Player {player}"]:
                    if "2" in card:
                        hand_value += 2
                    elif "3" in card:
                        hand_value += 3
                    elif "4" in card:
                        hand_value += 4
                    elif "5" in card:
                        hand_value += 5
                    elif "6" in card:
                        hand_value += 6
                    elif "7" in card:
                        hand_value += 7
                    elif "8" in card:
                        hand_value += 8
                    elif "9" in card:
                        hand_value += 9
                    elif "10" in card:
                        hand_value += 10
                    elif "J" in card:
                        hand_value += 10
                    elif "Q" in card:
                        hand_value += 10
                    elif "K" in card:
                        hand_value += 10

                for card in self.players[f"Player {player}"]:
                    if "A" in card:
                        if hand_value <= 10:
                            hand_value += 11
                        else:
                            hand_value += 1
                
                result.append(f"Player {player}'s hand is currently worth {hand_value}.")
            result = "\n".join(result)

        if hand_value > 21 and type(player_num) == int:
            return self.players[f"Player {player_num} bust with a {card} on {hand_value}!"]
        elif hand_value > 21 and type(player_num) == list:
            return self.players[f"Player {player} bust with a {card} on {hand_value}!"]
        else:
            return result
    
    def hit(self, player_num: int = 0, dealer=False) -> dict:
        if dealer == True:
            super().draw(dealer=dealer)
        else:
            super().draw(player_num=player_num)
        return self.players

# Figure out how much an ace is worth 1 or 11
cards = DeckOfCards(["SA", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", 
    "S10", "SJ", "SQ", "SK", "HA", "H2", "H3", "H4", "H5", "H6", 
    "H7", "H8", "H9", "H10", "HJ", "HQ", "HK", "DA", "D2", "D3", 
    "D4", "D5", "D6", "D7", "D8", "D9", "D10", "DJ", "DQ", "DK", 
    "CA", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", 
    "CJ", "CQ", "CK"])

blackjack = Blackjack(["SA", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", 
    "S10", "SJ", "SQ", "SK", "HA", "H2", "H3", "H4", "H5", "H6", 
    "H7", "H8", "H9", "H10", "HJ", "HQ", "HK", "DA", "D2", "D3", 
    "D4", "D5", "D6", "D7", "D8", "D9", "D10", "DJ", "DQ", "DK", 
    "CA", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", 
    "CJ", "CQ", "CK"])
blackjack.add_players(2)
blackjack.shuffle()
print(blackjack.deck)
print(blackjack.play())



    
