
import random
chips = int(input("How many chips do you have?: "))
bet = input("How much are you willing to bet? Your chips " + str(chips) + " : ")

times = 0
startingchips = chips

#draws a random card
def card():
    rand = random.choice([1,2,3,4,5,6,7,8,9,10,11,12,13]*4)
    
    if(rand > 10):
        rand = 10
    elif(rand == 1):
        rand = 11        
    return rand
#------------------------------------------------------------------------------
#Dealer and Player cards

dealerhand = [card(),card()]
playerhand = [card(),card()]

if(sum(playerhand) == 22):
    playerhand[0] = 1
#-----------------------------------------------------------------------------

#Asks the player what they want to do with their cards
def whatToDo(hand, times, split):
            
    if(split == True):
        ask = input("[H]it, [S]tand:")
        if(ask != "H" and ask != "S" and ask != "s" and ask != "h"):
            whatToDo(hand, times, split)
    elif(hand[0] == hand[1] and len(hand) == 2 and times == 1):
        ask = input("[H]it, [S]tand, [D]ouble Down or [SP]lit:")
        if(ask != "H" and ask != "S" and ask != "D" and ask != "SP"
           and ask != "h" and ask != "s" and ask != "d" and ask != "sp" ):
            whatToDo(hand, times, split)
    else:
        ask = input("[H]it, [S]tand, [D]ouble Down:")
        if(ask != "H" and  ask != "S" and ask != "D" and ask != "h"
                    and ask != "s" and ask != "d"):
            whatToDo(hand, times, split)
    
    print(" ")
    
    return ask
#------------------------------------------------------------------------------

#asks player if they want to play again
def playAgain():
    global chips

    if(chips <= 0):
        print("Out of chips. You Lost :(")
        quit()
        
    tryAgain = input("Play Again? (Y/N): ")
    
    if(tryAgain == "Y" or tryAgain == "y"):
        #clears everthing and creates new cards for the player and dealer
        bet = input("How much are you willing to bet? Your chips " + str(chips) + " : ")
    
        if(bet.isnumeric() == False or int(bet) > chips):
            print("Not a sufficient number")
            playAgain()
        
        times = 0
        playerhand = [card(),card()]
        dealerhand = [card(),card()]
        if(sum(playerhand) == 22):
            playerhand[0] = 1
            
        print(" ")
        print("Dealer is showing a ",dealerhand[0])
        if(playerhand[0] == 11 and playerhand[1] == 10
            or playerhand[1] == 11 and playerhand[0] == 10):
            
            print("Your cards: ", playerhand,' "21 You win"')
            chips += (int(bet)*3)
            playAgain()
            
        elif(dealerhand[0] == 11 and dealerhand[1] == 10
            or dealerhand[1] == 11 and dealerhand[0] == 10):
            
            print("Dealer: ", dealerhand,' "21 Dealer wins"')
            chips -= int(bet)
            playAgain()
            
        play(playerhand,times,dealerhand,int(bet))
        playAgain()
    elif(tryAgain == "N" or tryAgain == "n"):
        print("You have quit. Your chips: ",chips,"\n")
        
        if(startingchips > chips):
            print("Sadly you lost ",startingchips - chips," chip(s). :C")
        elif(startingchips < chips):
            print("You made ",chips - startingchips,"chip(s) in profit. :D")
        elif(startingchips == chips):
            print("You didnt lose or make anything")
        exit()
        
    else:
        playAgain()
#------------------------------------------------------------------------------

#splits the first two cards into new hands and plays a new game with them
def split(playercards,timesThrough,dealercards,bets):
    timesThrough += 1
    sp = True
    hit = False
    global chips
    print(" ")
    print("Your cards: ",playercards," For a total of: ",sum(playercards))
    print(" ")
    
    ask = whatToDo(playerhand,timesThrough, sp)
        
    if(ask ==  "H" or ask == "h"):
        playercards.append(card())
        for x in range(len(playercards)):

            if(playercards[x] == 11 and sum(playercards) > 21):
                playercards[x] = 1
                hit = True
                
        if(hit == True):
            split(playercards,timesThrough,dealercards,bets)
            
        elif(sum(playercards) > 21):
            print(" ")
            print("Your cards: ",playercards," For a total of: ",sum(playercards))
            print(" ")
            print("You busted.")
        else:
            split(playercards,timesThrough,dealercards,bets)
            
    elif(ask == "S" or ask == "s"):
        
        return
#------------------------------------------------------------------------------  

def play(playercards,timesThrough,dealercards,bets):
    timesThrough += 1
    sp = False
    hit = False
    global chips
    if(timesThrough == 1):    
        chips -= bets
        
    print(" ")
    print("Your cards: ",playercards," For a total of: ",sum(playercards))
    ask = whatToDo(playercards, timesThrough, sp)
    print(" ")
            
    if(ask ==  "H" or ask == "h"):
        #gives another card and checks if you bust while Ace = 11 then the Ace will be 1
        playercards.append(card())
        for x in range(len(playercards)):
            if(playercards[x] == 11 and sum(playercards) > 21):
                playercards[x] = 1
                hit = True
                    
        if(hit == True):
            play(playercards,timesThrough,dealercards,bets)
            
        elif(sum(playercards) > 21):
            print(" ")            
            print("You busted.")
            print("Your cards: ",playercards," For a total of: ",sum(playercards))
            return 
        else:
            play(playercards,timesThrough,dealercards,bets)
        
    elif(ask == "S" or ask == "D" or ask == "s" or ask == "d"):
        
        #Checks who won and gives chips accordingly
        
        if(ask ==  "D" and chips < bets / 2 or ask ==  "d" and chips < bets / 2):
            chips += bets
            print("\nNot enough Chips to Double down.")
            playAgain()

        elif(ask ==  "D" and chips >= bets * 2 or ask == "d" and chips >= bets * 2):
            playercards.append(card())
            chips -= bets
            bets = bets * 2
            
            for x in range(len(playercards)):
                
                if(playercards[x] == 11 and sum(playercards) > 21):
                    playercards[x] = 1
        
                
            if(sum(playercards) > 21):
                print(" ")            
                print("You busted.")
                print("Your cards: ",playercards," For a total of: ",sum(playercards))
                return
        while(sum(dealercards) < 17):
            dealercards.append(card())
            
        if(sum(dealercards) > 21):
            print("You win. Dealer Busted")
            print("Dealers Cards: ",dealercards, "For a total of: ",sum(dealercards))
            chips += bets*2
            return
            
        if(sum(playercards) <= 21 and sum(playercards) == sum(dealercards)):
            print("Your cards: ",playercards," For a total of: ",sum(playercards))
            print("Yours and the dealers scores were the same! Tie!")
            print("Dealers Cards: ",dealercards, "For a total of: ",sum(dealercards))
            chips += bets
            return
        
        if(sum(playercards) <= 21 and sum(playercards) > sum(dealercards)):
            print("Your cards: ",playercards," For a total of: ",sum(playercards))
            print("You had a bigger score than the dealer. You won")
            print("Dealers Cards: ",dealercards, "For a total of: ",sum(dealercards))
            chips += bets*2
            return
        
        else:
            print("Your cards: ",playercards," For a total of: ",sum(playercards))
            print("Dealers score was bigger. You lost")
            print("Dealers Cards: ",dealercards, "For a total of: ",sum(dealercards))
            return
        
    elif(ask == "sp" and timesThrough == 1 or ask == "SP" and timesThrough == 1):
        
        #makes two hands from the original hand
        hand1 = [playercards[0],card()]
        hand2 = [playercards[1],card()]
        
        chips -= bets
        
        #plays the players hand one after another
        print("Play the First hand")
        split(hand1,timesThrough,dealercards,bets)
        print(" ")
        
        print("Play the Second hand")
        split(hand2,timesThrough,dealercards,bets)
        print(" ")
        
        hands = [hand1,hand2]
        
        print("The First hand: ",hands[0], " Totals to: ", sum(hands[0]),"  ","The Second hand: ",hands[1], " Totals to: ", sum(hands[1]))
        print(" ")
        
        #after the player hands have been played the dealer reveals their cards
        while(sum(dealercards) < 17):
            dealercards.append(card())
            
        print("Dealer has: ",dealercards, " For a sum of: ",sum(dealercards))
        print(" ")
        
        #Checks who won the game or if they tied
        for i in range(len(hands)):
            if(sum(hands[i]) > 21):         
                print("You busted. Dealer wins Hand",i + 1,".")
            elif(sum(dealercards) > 21):
                print("You win hand ",i + 1,". Dealer Busted")
                chips += (bets + bets)
                    
            elif(sum(hands[i]) <= 21 and sum(dealercards) == sum(hands[i])):
                print("Yours and the dealers scores were the same! Hand ",i + 1," Ties!") 
                chips += bets
            elif(sum(hands[i]) <= 21 and sum(hands[i]) > sum(dealercards)):
                print("You had a bigger score than the dealer. You won Hand ",i + 1,".") 
                chips += (bets + bets)
            elif(sum(hands[i]) < sum(dealercards) and sum(dealercards) <= 21):
                print("Dealers score was bigger. You lost Hand ",i + 1,".") 
    else:
        print("Not a valid input")
        
#------------------------------------------------------------------------------

#Your chips and your bet

if(bet.isnumeric() == False or int(bet) > chips):
    print("Not a sufficient number")
    quit()
    
#Checks if anyone had a natural blackjack if player had it he/her gets 3 times his/her bet
if(playerhand[0] == 11 and playerhand[1] == 10
    or playerhand[1] == 11 and playerhand[0] == 10):
    
    print("Your cards: ", playerhand,' "21 You win"')
    chips += (int(bet)*3)
    playAgain()
    
elif(dealerhand[0] == 11 and dealerhand[1] == 10
    or dealerhand[1] == 11 and dealerhand[0] == 10):
    
    print("Dealer: ", dealerhand,' "21 Dealer wins"')
    chips -= int(bet)
    playAgain()
else:
    print("Dealer is showing a ",dealerhand[0])
    play(playerhand,times,dealerhand,int(bet))
    playAgain()
    print(" ")
