import tkinter as tk
from tkinter import messagebox, font
from PIL import Image, ImageTk, ImageDraw, ImageFont  # image handling
from uno_client import start_client
import os

class UnoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Uno Game")
        self.root.geometry("600x500") 
        self.root.configure(bg="#2E86C1")  # blue background

        # font for game
        self.custom_font = font.Font(family="Helvetica", size=12, weight="bold")

        # Server IP Input
        self.server_ip = tk.StringVar()
        self.server_frame = tk.Frame(root, bg="#2E86C1")
        self.server_frame.pack(pady=10)

        tk.Label(self.server_frame, text="Server IP:", bg="#2E86C1", fg="white", font=self.custom_font).pack(side=tk.LEFT)
        tk.Entry(self.server_frame, textvariable=self.server_ip, font=self.custom_font).pack(side=tk.LEFT, padx=5)
        tk.Button(self.server_frame, text="Connect", command=self.connect_to_server, bg="#28B463", fg="white", font=self.custom_font).pack(side=tk.LEFT)

        # display whatever the current card (or last played card) is
        self.current_card = tk.Label(root, text="Current Card: None", bg="#2E86C1", fg="white", font=self.custom_font)
        self.current_card.pack(pady=10)

        # show how many cards the opponent has (7 to start off)
        self.opponent_cards = tk.Label(root, text="Opponent Cards: 7", bg="#2E86C1", fg="white", font=self.custom_font)
        self.opponent_cards.pack(pady=10)

        # Pick Up Card Button
        tk.Button(root, text="Draw Card", command=self.pickup_card, bg="#FFFFFF", fg="black", font=self.custom_font).pack(pady=10)
        
        # Hand Frame (where player's cards are displayed)
        self.hand_frame = tk.Frame(root, bg="#2E86C1")
        self.hand_frame.pack(pady=20)
        


        # Load card images
        self.card_images = self.load_card_images()

    def load_card_images(self):
        # Load card images from the cards folder
        card_images = {}
        card_folder = "cards"  # Folder containing images (not my images)

        # Ensure the folder exists
        if not os.path.exists(card_folder):
            print(f"Error: Folder '{card_folder}' not found. Please create it and add Uno card images.")
            return card_images

        # Load images for each card
        for color in ["Red", "Green", "Blue", "Yellow"]:
            for value in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "Draw Two"]:
                image_path = os.path.join(card_folder, f"{color}_{value}.png")
                if os.path.exists(image_path):
                    card_images[f"{color} {value}"] = self.create_card_image(image_path)
                else:
                    print(f"Warning: Image not found for {color} {value} at {image_path}")

            # Load Wild and Draw Four cards
            wild_path = os.path.join(card_folder, "Wild.png")
            draw_four_path = os.path.join(card_folder, "Draw Four.png")
            if os.path.exists(wild_path):
                card_images["Wild"] = self.create_card_image(wild_path)
            if os.path.exists(draw_four_path):
                card_images["Draw Four"] = self.create_card_image(draw_four_path)

        return card_images

    def create_card_image(self, image_path):
        # Load and resize the image from the given path
        from PIL import Image
        try:
            image = Image.open(image_path)
            image = image.resize((100, 150), Image.Resampling.LANCZOS)  # Resize image to fit
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None

    def connect_to_server(self):
        server_ip = self.server_ip.get()
        if not server_ip:
            messagebox.showerror("Error", "Please enter a server IP")
            return
        self.client = start_client(server_ip, self)
        messagebox.showinfo("Connected", "Successfully connected to the server")

    def update_hand(self, cards):
        self.hand = cards
        self.update_hand_display()

    def update_current_card(self, card):
        # Update the current card display with color and styling
        color = card.split()[0]
        fore = "white" if color in ["Red", "Blue", "Wild", "Draw"] else "black"
        back = self.get_color_code(color)
        self.current_card.config(text=f"Current Card: {card}", fg=fore, bg=back, font=self.custom_font)

    def update_opponent_cards(self, player1_cards, player2_cards):
        self.opponent_cards.config(text=f"Player 1 Cards: {player1_cards}, Player 2 Cards: {player2_cards}", font=self.custom_font)

    def update_hand_display(self):
    # Clear the current hand display
        for widget in self.hand_frame.winfo_children():
            widget.destroy()

        # Determine the number of rows needed
        num_cards = len(self.hand)
        cards_per_row = 7  # Maximum number of cards per row
        num_rows = (num_cards + cards_per_row - 1) // cards_per_row  # Calculate the number of rows

        # Create a grid layout for the cards
        for row in range(num_rows):
            row_frame = tk.Frame(self.hand_frame)
            row_frame.pack(side=tk.TOP, pady=5)  # Pack each row frame vertically

            # Calculate the range of cards for the current row
            start_index = row * cards_per_row
            end_index = min((row + 1) * cards_per_row, num_cards)

            # Add cards to the current row
            for i in range(start_index, end_index):
                card = self.hand[i]
                color = card.split()[0]
                button = tk.Button(
                    row_frame,
                    text=card,
                    command=lambda c=card: self.play_card(c),
                    bg=self.get_color_code(color),
                    fg="white" if color in ["Red", "Blue", "Wild", "Draw"] else "black",
                    font=self.custom_font,
                    padx=10,
                    pady=10,
                )
                if card in self.card_images:
                    button.config(image=self.card_images[card], compound=tk.TOP)  # Add image to button
                button.pack(side=tk.LEFT, padx=5, pady=5)  # Pack buttons horizontally in the row

    def play_card(self, card):
        self.client.send(f"play:{card}".encode('utf-8'))
        self.hand.remove(card)
        self.update_hand_display()

    def pickup_card(self):
        self.client.send("pickup".encode('utf-8'))
    
    # pick up 2 cards
    def pick_2_cards(self):
        for i in range(0,2):
            self.client.send("pickup".encode('utf-8'))
    
    # draw 4
    def pick_4_cards(self):
        for i in range(0,4):
            self.client.send("pickup".encode('utf-8'))


    def add_card_to_hand(self, card):
        self.hand.append(card)
        self.update_hand_display()

    def show_winner(self, winner_id):
        messagebox.showinfo("Game Over", f"Player {winner_id} has won the game!")

    def get_color_code(self, color):
        # Map Uno colors to button background colors
        color_map = {
            "Red": "#E74C3C",  # Red
            "Green": "#28B463",  # Green
            "Blue": "#3498DB",  # Blue
            "Yellow": "#F1C40F",  # Yellow
            "Wild": "#000000",  # Wild
            "Draw": "#000000",  # Draw Four
        }
        return color_map.get(color, "#FFFFFF")  # Default to white if color is not found

if __name__ == "__main__":
    root = tk.Tk()
    gui = UnoGUI(root)
    root.mainloop()
