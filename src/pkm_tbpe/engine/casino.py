import random
from .graphics import Graphics
from .bag import Bag

class Casino:
    @classmethod
    def start_blackjack(cls, user):
        print("\nWelcome to the Blackjack table!")

        while True:
            pokedollars = user.bag.pokedollars
            print(f"Current Pokedollars: ${pokedollars}")

            wager_input = input("Enter your wager (or 'B' to back): ").upper()
            if wager_input == 'B':
                break

            try:
                wager = int(wager_input)
            except ValueError:
                print("Invalid wager.")
                continue

            if wager > pokedollars:
                print("You don't have enough money!")
                continue
            if wager <= 0:
                print("Wager must be positive.")
                continue

            user.bag.remove_pokedollars(wager)

            deck = [2,3,4,5,6,7,8,9,10,10,10,10,11] * 4
            random.shuffle(deck)

            player_hand = [deck.pop(), deck.pop()]
            dealer_hand = [deck.pop(), deck.pop()]

            player_turn = True
            while player_turn and sum(player_hand) < 21:
                print(f"\nYour hand: {player_hand} (Total: {sum(player_hand)})")
                print(f"Dealer showing: {dealer_hand[0]}")

                action = input("[H]it or [S]tand? ").upper()
                if action == 'H':
                    player_hand.append(deck.pop())
                elif action == 'S':
                    player_turn = False

            player_total = sum(player_hand)
            print(f"\nYour final hand: {player_hand} (Total: {player_total})")

            if player_total > 21:
                print("Bust! You lost your wager.")
            else:
                print(f"Dealer's hand: {dealer_hand}")
                while sum(dealer_hand) < 17:
                    dealer_hand.append(deck.pop())
                    print(f"Dealer draws: {dealer_hand[-1]} (Total: {sum(dealer_hand)})")

                dealer_total = sum(dealer_hand)
                if dealer_total > 21 or player_total > dealer_total:
                    print(f"You win! You got ${wager * 2}")
                    user.bag.add_pokedollars(wager * 2)
                elif player_total == dealer_total:
                    print("Push! You get your wager back.")
                    user.bag.add_pokedollars(wager)
                else:
                    print("Dealer wins! You lost your wager.")

            if input("\nPlay again? (Y/N): ").upper() != 'Y':
                break
