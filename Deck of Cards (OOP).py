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
        self.burn_pile = []
    
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
    
    # Gives each player a specified amount of cards
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

    # Draws one or more cards to a specified player
    def draw(self, player_num: int = 0, num_cards_to_draw: int = 1, dealer=False) -> None:
        if DeckOfCards.current_players == 0:
            raise Exception(f"There are {DeckOfCards.current_players} players to draw cards.")
        
        if dealer == True:
            key = f"The Dealer"
        else:
            key = f"Player {player_num}"

        for x in range(0, num_cards_to_draw):
            self.players[key].append(self.deck[0])
            self.deck.pop(0)    
    
    # Resets the deck back to its original state 
    def reset(self) -> None:
        self.deck = DeckOfCards.original_deck

    # Returns how many cards are left in the deck
    def cards_left(self) -> int:
        for cards_left, card in enumerate(range(0, len(self.deck) + 1)):
            continue
        
        return cards_left

    # Change the deck and its original copy to something else
    def change_deck(self, new_deck: list) -> None:
        if type(new_deck) != list:
            raise Exception("change_deck() takes a list argument only.")
        else:
            DeckOfCards.original_deck = new_deck.copy()
            self.deck = new_deck
            
    # Cuts the deck at a position, cuts in a random position if not specified
    def cut(self, position=None):
        if position != None and type(position) != int:
            raise Exception("cut() takes an int argument or none at all")
        if position == None:
            position = randint(0, len(self.deck) - 1)

        for card in self.deck[0:position]:
            self.deck.append(card)
        self.deck[0:position] = ""
            

    # Removes the top card, or multiple if specified
    def burn(self, num_cards=1):
        self.burn_pile += self.deck[0:num_cards]
        self.deck[0:num_cards] = ""

    # Shows the top card, or multiple if specified
    def peek(self, num_cards=1):
        return self.deck[0]
    
    # Sorts a player's hand
    # Spades (highest)
    # Hearts
    # Diamonds
    # Clubs (lowest)
    # Joker-Ace-King or Ace-King-Joker


    def sort(self, player_num):
        self.players[f"Player {player_num}"].sort()
        print(self.players)

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
        self.players["The Dealer"] = []
        self.player_hand_value = 0
        self.dealer_hand_value = 0

    def play(self):
        print("♠ ♥ Blackjack ♦ ♣")
        command = None

        while command != "quit":
            # Player actions
            if command != "stand":
                command = input("Type hit, stand, or quit.\n").lower().strip()
                print()
            while command != "hit" and command != "stand" and command != "quit":
                command = input("Type hit, stand, or quit.\n")
                print()
            if command == "hit":
                self.hit(1)

            # Evaluates the player's hand and busts if greater than 21
            self.evaluate_hand(1)
            if self.player_hand_value > 21:
                print(self.players)
                print(f"Player has bust on {self.player_hand_value}!")
                print("The Dealer wins!\n")
                break
            
            # Dealer only hits when less than 17
            if self.dealer_hand_value < 17:
                self.hit(dealer=True)
                self.evaluate_hand(dealer=True)
            
            # Dealer busts when greater than 21
            if self.dealer_hand_value > 21:
                print(self.players)
                print(f"The Dealer has bust on {self.dealer_hand_value}!")
                print("Player wins!\n")
                break
            
            # Prints Blackjack information
            print(self.players)
            print(f"The Dealer's hand is worth {self.dealer_hand_value}.")
            print(f"Player's hand is worth {self.player_hand_value}.")

            # Dealer stands on 17 and above
            if self.dealer_hand_value >= 17:
                print("The Dealer is standing.")

                # If the dealer and player are standing, 
                # evaluate whether the hands are equal or one is closer to 21 and choose a winner
                if command == "stand":
                    print()
                    print(self.players)
                    if 21 - self.player_hand_value < 21 - self.dealer_hand_value:
                        print("Player 1 is closer to 21.")
                        print("Player 1 wins!") 
                    elif 21- self.dealer_hand_value < 21 - self.player_hand_value:
                        print("The Dealer is closer to 21.")
                        print("The Dealer wins!")
                    else:
                        print("The Dealer and Player are an equal distance from 21.")
                        print("It's a tie!")
                    break
            print()
    
    # Evaluates the value of the dealer's or player's hand
    def evaluate_hand(self, player_num: int | list = 0, dealer=False) -> int:
        values = [2, 3, 4, 5, 6, 7, 8, 9, 10]
        hand_value = 0

        if dealer == True:
            key = "The Dealer"
        else:
            key = f"Player {player_num}"
        
        for card in self.players[key]:
            for value in values:
                if str(value) in card:
                    hand_value += value
            if "J" in card:
                hand_value += 10
            elif "Q" in card:
                hand_value += 10
            elif "K" in card:
                hand_value += 10

        for card in self.players[key]:
            if "A" in card:
                if hand_value <= 10:
                    hand_value += 11
                else:
                    hand_value += 1

        # Assigns dealer and player hand values
        if dealer == True:
            self.dealer_hand_value = hand_value
        else:
            self.player_hand_value = hand_value

    # Increases the value of the dealer's or player's hand
    def hit(self, player_num: int = 0, dealer: bool = False) -> dict:
        if dealer == True:
            super().draw(dealer=dealer)
        else:
            super().draw(player_num=player_num)


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

card_template = """
___________
|XX       |
|X X X X  |
|    X    | 
|  X X X  | 
|    X    |
|  X X X X|
|       XX|
‾‾‾‾‾‾‾‾‾‾‾
"""
x_num = 1
for index, x in enumerate(card_template):
    if x == "X":
        print(f"x{x_num}= {index}")
        x_num += 1
    match index:
        case 1:
            card_template = card_template[0:14] + "A" + card_template[15:]
            card_template = card_template[0:15] + "A" + card_template[16:]

print(card_template)
# 1 = 55


# Add the possibility for more than one person to play Blackjack
# blackjack.add_players(1)
# blackjack.shuffle()
# print(blackjack.deck)
# blackjack.play()

# cards.add_players(1)
# cards.shuffle()
# cards.shuffle()
# cards.shuffle()
# cards.shuffle()
# cards.draw(1, 10)
# print(cards.players)
# cards.sort(1)


"""
3. Gameplay
At the start:
You get two cards, the dealer gets two:
One face-up
One face-down (the “hole” card)
Your options:
Hit → Take another card
Stand → Keep your total
Double Down → Double your bet, get one more card, then stand
Split → If your first two cards are the same value, you may split them into two hands
Surrender (if allowed) → Forfeit half your bet and end the hand

4. Blackjack
A “blackjack” (also called a natural) is:
Ace + 10-value card on your first two cards only
This usually pays 3:2 (though some casinos use 6:5).
A natural blackjack beats any other 21.

7. Winning
You win if:
Your total is closer to 21 than the dealer's
The dealer busts
You have a natural blackjack and the dealer doesn't
Push (tie):
If you and the dealer have the same total (except blackjack vs 21), it's a push → your bet is returned.

8. Insurance
If the dealer's face-up card is an Ace, you may buy insurance (a side bet that pays 2:1 if the dealer has blackjack).
It's almost always a bad bet strategically.

9. Splitting Rules (common)
You can split a pair to make two hands
You must bet again for the second hand
Aces often only receive one card each when split
A split Ace + 10 is not a natural blackjack—it's just 21
"""


