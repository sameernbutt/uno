import socket
import threading

def receive_messages(client_socket, gui):
    unrec = True
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith("deal:"):
                cards = message.split(":")[1].split(", ")
                gui.update_hand(cards)
            elif message.startswith("update:"):
                parts = message.split(":")
                current_card = parts[1]
                player1_cards = parts[2]
                player2_cards = parts[3]
                gui.update_current_card(current_card)
                gui.update_opponent_cards(player1_cards, player2_cards)
            elif message.startswith("new_card:"):
                new_card = message.split(":")[1]
                gui.add_card_to_hand(new_card)
            elif message.startswith("win:"):
                winner_id = message[4:]
                gui.show_winner(winner_id)
        except:
            print("Connection closed")
            break

def start_client(server_ip, gui):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, 5555))

    threading.Thread(target=receive_messages, args=(client, gui)).start()

    return client