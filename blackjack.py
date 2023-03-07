import random
times = 0

#draws a random card
def card():
    rand = random.randint(1,52)
    if(rand > 13 and rand < 27):
        rand = rand - 13          
    elif(rand > 26 and rand < 40):
        rand = rand - 26     
    elif(rand > 39):
        rand = rand - 39     
    if(rand > 10):
        rand = 10
    return rand
#------------------------------------------------------------------------------
#Dealer and Player cards

dealerhand = [card(),card()]
playerhand = [card(),card()]
 
#-----------------------------------------------------------------------------

#Asks the player what they want to do with their cards
def whatToDo(hand):
    if(hand[0] == hand[1] and len(hand) == 2):
        ask = input("[H]it, [S]tand, [D]ouble Down or [SP]lit:")
    else:
        ask = input("[H]it, [S]tand or [D]ouble Down: ")
    print(" ")
    
    return ask
#------------------------------------------------------------------------------

#asks player if they want to play again
def playAgain():
    tryAgain = input("Play Again? (Y/N): ")
    if(tryAgain == "Y" or tryAgain == "y"):
        #clears everthing and creates new cards for the player and dealer
        times = 0
        playerhand = [card(),card()]
        dealercards = [card(),card()]
    
        print(" ")
        print("Dealer is showing a ",dealerhand[0])
        play(playerhand,times,dealercards)
        playAgain()
    elif(tryAgain == "N" or tryAgain == "n"):
        quit()
    else:
        playAgain()
#------------------------------------------------------------------------------

#splits the first two cards into new hands and plays a new game with them
def split(playercards,timesThrough,dealercards):
    timesThrough += 1
    
    print(" ")
    print("Your cards: ",playercards," For a total of: ",sum(playercards))
    print(" ")
    
    ask = whatToDo(playerhand)
    
    if(playercards[0] == 1 and playercards[1] == 10
    or playercards[1] == 1 and playercards[0] == 10):
        print("Your cards: ", playercards,' "21 You win"')
        playAgain()
    
    elif(dealercards[0] == 1 and dealercards[1] == 10
    or dealercards[1] == 1 and dealercards[0] == 10):
        print("Dealer: ", dealercards,' "21 Dealer wins"')
        playAgain()
        
    elif(ask ==  "H" or ask == "h"):
        playercards.append(card())
        
        if(sum(playercards) > 21):
            print(" ")
            print("Your cards: ",playercards," For a total of: ",sum(playercards))
            print(" ")
            print("You busted.")
        else:
            split(playercards,timesThrough,dealercards)
            
    elif(ask == "S" or ask == "D" or ask == "s" or ask == "d"):
        
        if(ask ==  "D"):
            playercards.append(card())
            if(sum(playercards) > 21):
                print(" ")
                print("Your cards: ",playercards," For a total of: ",sum(playercards))
                print(" ")
                print("You busted.")
            else:
                print("Your cards: ",playercards," For a total of: ",sum(playercards))  
#------------------------------------------------------------------------------  
 
def play(playercards,timesThrough,dealercards):
    timesThrough += 1
    
    print(" ")
    print("Your cards: ",playercards," For a total of: ",sum(playercards))
    ask = whatToDo(playercards)
    print(" ")
    
    if(playercards[0] == 1 and playercards[1] == 10
    or playercards[1] == 1 and playercards[0] == 10):
        print("Your cards: ", playercards,' "21 You win"')
        playAgain()
    
    elif(dealercards[0] == 1 and dealercards[1] == 10
    or dealercards[1] == 1 and dealercards[0] == 10):
        print("Dealer: ", dealercards,' "21 Dealer wins"')
        playAgain()
            
    elif(ask ==  "H" or ask == "h"):
        playercards.append(card())
        if(sum(playercards) > 21):
            print(" ")            
            print("You busted.")
            print("Your cards: ",playercards," For a total of: ",sum(playercards))
            return
        else:
            play(playercards,timesThrough,dealercards)
            
    elif(ask == "S" or ask == "D" or ask == "s" or ask == "d"):
        if(ask ==  "D" or ask == "d"):
            playercards.append(card())
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
            return
            
        if(sum(playercards) <= 21 and sum(playercards) == sum(dealercards)):
            print("Your cards: ",playercards," For a total of: ",sum(playercards))
            print("Yours and the dealers scores were the same! Tie!")
            print("Dealers Cards: ",dealercards, "For a total of: ",sum(dealercards))
            return
        
        if(sum(playercards) <= 21 and sum(playercards) > sum(dealercards)):
            print("Your cards: ",playercards," For a total of: ",sum(playercards))
            print("You had a bigger score than the dealer. You won")
            print("Dealers Cards: ",dealercards, "For a total of: ",sum(dealercards))
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
        playercards = [0,1]
        
        #plays the players hand one after another
        print("Play the First hand")
        split(hand1,timesThrough,dealercards)
        print(" ")
        
        print("Play the Second hand")
        split(hand2,timesThrough,dealercards)
        print(" ")
        
        hands = [hand1,hand2]
        print (hands[0],hands[1])
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
                    
            elif(sum(hands[i]) <= 21 and sum(dealercards) == sum(hands[i])):
                print("Yours and the dealers scores were the same! Hand ",i + 1," Ties!") 
                
            elif(sum(hands[i]) <= 21 and sum(hands[i]) > sum(dealercards)):
                print("You had a bigger score than the dealer. You won Hand ",i + 1,".") 
                
            elif(sum(hands[i]) < sum(dealercards) and sum(dealercards) <= 21):
                print("Dealers score was bigger. You lost Hand ",i + 1,".")

    else:
        print("Not a valid input")
        
#------------------------------------------------------------------------------
   
print("Dealer is showing a ",dealerhand[0])
play(playerhand,times,dealerhand)
print(" ")
playAgain()
