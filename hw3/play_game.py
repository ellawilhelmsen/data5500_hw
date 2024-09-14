
from DeckOfCards import *


# function to check for aces
def check_ace(card_face, ace_count):
    if card_face == "Ace":
        ace_count += 1
    return ace_count   

# play again function
def play_again_function():
    while True:
        response = input("Would you like to play again? (y/n)").lower()
        if response == 'y' or response == 'n':
            break
        else:
            print('Please enter y or n')
    return response


# main game loop
play_again = 'y'

while play_again == 'y':
     
    # create a deck of cards   
    deck = DeckOfCards()
    print()
    print('Deck of Cards:')
    deck.print_deck()
    print()

    # shuffle the deck
    deck.shuffle_deck()
    print('Shuffled Deck of Cards:')
    deck.print_deck()
    print()


    # set up for ace value adjustment
    aces = 0
    dealer_aces = 0


    # deal two cards to the user and check for aces
    card = deck.get_card()
    aces = check_ace(card.face, aces)

    card2 = deck.get_card()
    aces = check_ace(card2.face, aces)


    # deal two cards to the dealer and check for aces
    dealer_card = deck.get_card()
    dealer_aces = check_ace(dealer_card.face, dealer_aces)

    dealer_card2 = deck.get_card()
    dealer_aces = check_ace(dealer_card2.face, dealer_aces)


    # set up scores for user and dealer
    score = 0
    dealer_score = 0


    # calculate the user's and dealer's hand score
    score += card.val
    score += card2.val

    dealer_score += dealer_card.val
    dealer_score += dealer_card2.val


    # print users cards and score
    print()
    print(f'Card one: {card}')
    print(f'Card two: {card2}')
    print()
    print("Your score is: ", score)


    # set up for user to take a hit
    cont = 0


    # blackjack check
    if score == 21:
        print("Blackjack! You win!")
        play_again = play_again()

    # user turn
    else:
        while cont == 0:
            # ask user if the want to take a hit
            hit = input("Would you like a hit? (y/n)").lower()

            if hit == 'y':
                # deal another card to the user, check for aces, calculate score
                card3 = deck.get_card()
                aces = check_ace(card3.face, aces)
                score += card3.val
                print(f'New Card: {card3}')

                if score > 21 and aces > 0:
                    # adjust score for aces
                    score -= 10
                    aces -= 1

                elif score > 21:
                    # check for a bust
                    print("You busted. You lose.")
                    print()
                    # ask user if they want to play again
                    play_again = play_again_function()
                    cont = 1

                # print new score
                print("New Score: ", score)
                
            elif hit == 'n':
                # end users turn
                print("Your final score is: ", score)  
                cont = 1

                # calculate the dealer's hand score
                print()
                print("Dealer's Turn:")
                print(f'Dealer card one: {dealer_card}')
                print(f'Dealer card two: {dealer_card2}')
                print()

                if dealer_score == 21:
                    # check for dealer blackjack
                    print("Dealer has blackjack, and wins.")
                    print()
                    # ask user if they want to play again
                    play_again = play_again_function()
                    break
                else:
                    while dealer_score < 17:
                        # dealer must hit on 16 or less
                        # deal another card to the dealer, check for aces, calculate score
                        dealer_card3 = deck.get_card()
                        print(f'Dealer hits, new card: {dealer_card3}')
                        dealer_aces = check_ace(dealer_card3.face, dealer_aces)
                        dealer_score += dealer_card3.val

                        if dealer_score > 21 and dealer_aces > 0:
                            # adjust score for aces
                            dealer_score -= 10
                            dealer_aces -= 1

                        elif dealer_score > 21:
                            # check for dealer bust
                            print("You win! Dealer busted. Yay!")
                            print()

                            # ask user if they want to play again
                            play_again = play_again_function()
                            break
                    else:   
                        print("Dealer Score: ", dealer_score)
                        print()

                        # check for winner, deliver results
                        if dealer_score > score:
                            print("Dealer wins. Their score is higher than yours.")
                        elif dealer_score == score:
                            print("It's a push. You and the dealer have the same score.")
                        else:
                            print("You win! Your score is higher than the dealer's.")
                        print()

                        # ask user if they want to play again
                        play_again = play_again_function()

            else: 
                print('please enter y or n')     


        