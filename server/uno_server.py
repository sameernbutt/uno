import socket
import threading
import random
import atexit

# Define the card colors and values
COLORS = ['Red', 'Green', 'Blue', 'Yellow']
VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', 'Draw Two']
names = []

# Change to change the number of cards per player
cardsPerPlayer = 7

# Make deck of cards
def create_deck():
    deck = []
    for color in COLORS:
        for value in VALUES:
            deck.append(f"{color} {value}")
            if value != '0':
                deck.append(f"{color} {value}")
    for i in range(4):
        deck.append("Wild")
        deck.append("Draw Four")
    return deck

# Server code
def handle_client(client_socket, player_id, players, game_state):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Player {player_id}: {data}")
            if(data.startswith("name")):
                pass
            if data.startswith("play:"):
                # Handle playing a card
                card = data.split(":")[1]
                if is_valid_move(card, game_state['current_card']):
                    game_state['current_card'] = card
                    game_state['player_cards'][player_id] -= 1
                    if game_state['player_cards'][player_id] == 0:
                        broadcast_win(player_id, players)
                        break
                else: # invalid move so send the card back
                    new_card = card
                    client_socket.send(f"new_card:{new_card}".encode('utf-8'))
            elif data == "pickup":
                # Handle picking up a card
                if game_state['deck']:
                    new_card = game_state['deck'].pop()
                    game_state['player_cards'][player_id] += 1
                    client_socket.send(f"new_card:{new_card}".encode('utf-8'))
            # Broadcast updated game state to all players
            elif data.startswith("disconnect"):
                print(f"Player {player_id} has disconnected.")
                client_socket.close()
                players.pop(client_socket, None)
                break  # Exit loop to stop receiving data
            broadcast_game_state(players, game_state)
        except Exception as e:
            print(f"Error: {e}")
            client_socket.close()
            break
    client_socket.close()
    

def is_valid_move(card, current_card):
    if current_card is None:
        return True  # First card played is always valid
    if card.startswith("Wild") or card.startswith("Draw Four"):
        return True  # Wild and Draw Four cards are always valid
    if current_card.startswith("Wild") or current_card.startswith("Draw Four"):
        return True  # If the current card is Wild or Draw Four, any card is valid
    try:
        if(card.endswith("Draw Two")): # draw 2 splits unexpectedly so added this if statement to accomodate
            card_color = card.split()[0]
            card_value = "Draw Two"
        else:
            card_color, card_value = card.split()
        if(current_card.endswith("Draw Two")): # same reason as the above if statement but for the current card
            current_color = current_card.split()[0]
            current_value = "Draw Two"
        else:
            current_color, current_value = current_card.split()
        return card_color == current_color or card_value == current_value
    except ValueError:
        return False  # If the card format is invalid, it's not a valid move

def broadcast_game_state(players, game_state):
    for p in players:
        p.send(f"update:{game_state['current_card']}:{game_state['player_cards'][1]}:{game_state['player_cards'][2]}".encode('utf-8'))

def broadcast_win(winner_id, players):
    winner = names[winner_id-1]
    for p in players:
        print("Broadcasting win to " + str(p))
        p.send(f"win:{winner}".encode('utf-8'))

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(2)
    print("Server started, waiting for connections...")

    players = []
    player_id = 1
    deck = create_deck()
    random.shuffle(deck)
    game_state = {'current_card': None, 'player_cards': {1: cardsPerPlayer, 2: cardsPerPlayer}, 'deck': deck[cardsPerPlayer*2:]}

    atexit.register(cleanup, server, players)

    while len(players) < 2:
        client, addr = server.accept()
        
        print(f"Player {player_id} connected from {addr}")
        data = client.recv(1024).decode('utf-8')
        if(data.startswith("name")):
            names.append(data[5:])
        players.append(client)
        threading.Thread(target=handle_client, args=(client, player_id, players, game_state)).start()
        player_id += 1

    # Start the game
    for i, player in enumerate(players):
        player.send(f"deal:{', '.join(deck[i*cardsPerPlayer:(i+1)*cardsPerPlayer])}".encode('utf-8'))
def cleanup(server, players):
    """Cleanup function to close all sockets."""
    print("Cleaning up server resources...")
    for player in players:
        player.close()  # Close all client sockets
    server.close()  # Close the server socket
    print("Server shutdown complete.")

if __name__ == "__main__":
    start_server()