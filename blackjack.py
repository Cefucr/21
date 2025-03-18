import random
import os

def clearTerminal(): # Terminal clearer
    if os.name == 'nt':
        os.system('CLS')
    if os.name == 'posix':
        os.system('clear')

class Card:
    def __init__(self,value,suit):
        self.value = value
        self.suit = suit
        self.face = str(value)

        if self.value == 11: self.face = "J"
        elif self.value == 12: self.face = "Q"
        elif self.value == 13: self.face = "K"
        elif self.value == 1: self.face = "A" 

class Deck:
    def __init__(self):
        self.deckCount = 4
        self.cardValues = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        self.suits = ["♥","♦","♠","♣"] 
        self.pile = []
        self.newDeck()

    def newDeck(self):
        self.pile = [Card(value,suit) for i in range(self.deckCount)for suit in self.suits for value in self.cardValues]
        random.shuffle(self.pile) # Shuffling the deck

    def drawCard(self):
        if len(self.pile) <= 30: #shuffling the deck if cards are running low
            print("Deck is running low, reshuffling...")
            self.newDeck()

        return self.pile.pop(0) #draws card from the deck

class Hand:
    def __init__(self,deck,sp):
        self.cards = []
        self.totalValue = 0
        self.isBlackJack = False
        self.isBusted = False
        if sp == False:
            for i in range(2): # If hand isn't a splitted hand then we make the hand here by drawing two cards
                self.addCard(deck.drawCard())

    def addCard(self, card): # Draw a new card to hand
        self.cards.append(card)
        self.totalCalc()
    
    def totalCalc(self):
        total = 0
        aces = 0
        
        for card in self.cards:
            if card.value > 10:
                card.value = 10
                total += 10
            elif card.value == 1:
                aces += 1
                total += 11
            else:
                total += card.value
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        
        self.total = total # Here we keep track of the sum of the hand
        self.busted()
        self.blackJack()

    def busted(self): # Check if hand busted
        if self.total > 21:
            self.isBusted = True

    def blackJack(self): # Check if hand had a blackjack
        if self.total == 21 and len(self.cards) == 2:
            self.isBlackJack = True
        return self.isBlackJack

    def showHand(self):
        return ", ".join(card.face + " " + card.suit for card in self.cards)

class Chips:
    def __init__(self):
        self.total = 0
        self.bet = 0
        self.total = self.getChips()

    def getChips(self):
        while True: # Asking the player for their chip amount then validate it
            try:
                self.total = int(input("How many chips do you have?: "))
                if self.total <= 0:
                    raise ValueError("Cant play with 0 chips!")
                break
            except ValueError as e:
                print(f"Error: {e}. Please try again")
            
        return self.total
    
    def placeBet(self):
        while True: # Asking the player for their bet then validate it
            try: 
                self.bet = int(input(f"How much do you want to bet? Your Chips {self.total}: "))
                if self.bet > self.total or self.bet < 1:
                    raise ValueError("Invalid input")
                break
            except ValueError as e:
                print(f"Error: {e}. Please try again")
        return self.bet

class Stats:
    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.ties = 0

    def updateValues(self):
        self.gamesPlayed = self.wins + self.losses + self.ties
        if self.wins <= 0: self.winrate = 0
        else: self.winrate = self.wins / self.gamesPlayed * 100

    def __str__(self):
        self.updateValues()
        return (
            "\n| Win | Tie | Loss | Winrate |\n"
            f"|  {self.wins}  |  {self.ties}  |  {self.losses}   |  {self.winrate:.2f} % |"
        )

def deal(chips,stats):
    clearTerminal() # Clear the terminal so it looks nicer

    if chips.total <= 0: #We check if player is out of chips
        print("Out of chips!")
        quit()

    chips.placeBet() # Here we ask the players bet amount

    deck = Deck() # Making a new deck 
    playerHand = Hand(deck,False) # from the deck make player and dealers hands
    dealerHand = Hand(deck,False)    

    if playerHand.isBlackJack: # Check if player or dealer had a blackjack
        print(f'Your cards: {playerHand.showHand()} "21 You win"')
        chips.total += chips.bet * 3
        stats.wins += 1
        
    elif dealerHand.isBlackJack:
        print(f'Dealer: {dealerHand.showHand()} "21 Dealer wins"')
        chips.total -= chips.bet
        stats.losses += 1

    else:
        print(f'Dealer is showing a {dealerHand.cards[0].face + " " + dealerHand.cards[0].suit}')    
        play(playerHand,True,dealerHand,deck,chips,stats)

    playAgain(chips,stats)

def whatToDo(hand, firstTime):
    choices = ["h","s"] # Default choices are hit and stand

    if firstTime:
        choices.append("d") # If it is the first hand double down is also available
        if hand.cards[0].face == hand.cards[1].face and len(hand.cards) == 2 :
            choices.append("sp") # If it is the first hand and the cards are the same split is available

    while True:
        ask = input(f"[{'],['.join(choice.upper() for choice in choices)}]: ").lower()
        if ask in choices: return ask

def checkWinner(dealerHand, playerHand, chips, stats):
    wonChips = 0
    if playerHand.isBusted: # If players cards total > 21      
        print(f"You busted.")
        stats.losses += 1
    elif dealerHand.isBusted: # If dealers cards total > 21
        wonChips = chips.bet * 2
        stats.wins += 1
        print(f"You win {wonChips} chips. Dealer Busted")
    elif(playerHand.total == dealerHand.total): # If players and dealers cards total are the same
        print("Tie!")
        stats.ties += 1
        wonChips = chips.bet
    elif playerHand.total > dealerHand.total: # If players total > dealers total but didn't bust
        wonChips = chips.bet * 2
        stats.wins += 1
        print(f"You won {wonChips} chips!")
    else:
        print("Dealer wins!")
        stats.losses += 1

    chips.total += wonChips

def playAgain(chips,stats):
    while True:
        tryAgain = input("\nPlay Again? (Y/N) Stats (S) : ").lower() #asks player if they want to play again
        if tryAgain == "y":
            deal(chips,stats) # If player wants to play again deal cards
        if tryAgain == "s":
            print(stats)
        elif tryAgain == "n":
            print(f"\nYou have quit. Your chips: {chips.total}")
            quit()

def play(playerHand, firstTime, dealerHand, deck, chips, stats):
    
    print(f"\nYour cards: {playerHand.showHand()}")
    ask = whatToDo(playerHand, firstTime).lower()

    if firstTime: chips.total -= chips.bet # If it is the first time take the bet amount from the chips
        
    if ask == "h":
        firstTime = False

        playerHand.addCard(deck.drawCard())
        if playerHand.isBusted:
            print(f"\nYou busted. Your cards: {playerHand.showHand()}")
            stats.losses += 1
            return 
        play(playerHand,firstTime,dealerHand,deck,chips,stats)
        
    elif ask == "s" or ask == "d" and chips.total >= chips.bet:
        if ask == "d": # If player doubles down adjust chips and draw a card after that stand
            playerHand.addCard(deck.drawCard())
            chips.total -= chips.bet
            chips.bet *= 2

        while dealerHand.total < 17: dealerHand.addCard(deck.drawCard())
        checkWinner(dealerHand, playerHand, chips, stats) #Checks who won the game or if they tied
        print(f"Your cards: {playerHand.showHand()}")
        print(f"Dealers Cards: {dealerHand.showHand()}")

    elif ask == "sp" and firstTime and chips.total >= chips.bet:

        chips.total -= chips.bet #Adjust bet to double 
        firstTime = False

        #makes two hands from the original hand
        hand1 = Hand(deck,True)
        hand2 = Hand(deck,True)
        hands = [hand1 , hand2]

        for hand in hands:
            hand.addCard(playerHand.cards[hands.index(hand)])
            hand.addCard(deck.drawCard())
            print(f"\nPlay the {hands.index(hand) + 1}. hand")
            play(hand, firstTime, dealerHand, deck, chips, stats) #Play the game with the two splitted hands
 
        print(f"\nFinal Hands: First hand: {hand1.showHand()}  |  Second hand: {hand2.showHand()}")

        while(dealerHand.total < 17): dealerHand.addCard(deck.drawCard()) #Dealer draw cards until dealers hand is > 17
        print(f"Dealer has: {dealerHand.showHand()}")
        
        for hand in hands:
            print(f"Hand {hands.index(hand) + 1}: ",end="")
            checkWinner(dealerHand, hand, chips, stats) #Checks who won the game or if they tied

    else:
        print("Invalid input or Insufficient Chips")
        if firstTime: chips.total += chips.bet
        play(playerHand, firstTime, dealerHand, deck, chips, stats)

stats = Stats()
chips = Chips()
deal(chips,stats)
