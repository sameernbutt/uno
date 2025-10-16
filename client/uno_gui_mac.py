
import pygame
import pygame_gui
import os
import sys
from pygame.locals import *
from uno_client import start_client

def resource_path(relative_path):
    """Get the absolute path to a resource."""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class UnoGUI:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("UNO Game")
        
        # Initial window size
        self.screen_width, self.screen_height = 1000, 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        
        # UI Manager
        self.manager = pygame_gui.UIManager((self.screen_width, self.screen_height), 'theme.json')
        
        # Colors
        self.BLUE = (46, 134, 193)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        
        # Game state
        self.hand = []
        self.current_card = "None"
        self.opponent_cards = "7"
        self.player_name = ""
        self.server_ip = ""
        self.connected = False
        self.card_rects = []  # To track card positions for clicking
        
        # UI Elements
        self.create_ui_elements()
        
        # Load card images
        self.card_images = self.load_card_images()
        
        # Font
        self.font = pygame.font.SysFont("Helvetica", 20)
        self.title_font = pygame.font.SysFont("Helvetica", 24, bold=True)
        
        # Clock
        self.clock = pygame.time.Clock()
    
    def create_ui_elements(self):
        # Calculate center positions
        center_x = self.screen_width // 2
        
        # Name input
        self.name_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(center_x - 250, 20, 100, 30),
            text="Name:",
            manager=self.manager,
            object_id=pygame_gui.core.ObjectID(class_id="@labels", object_id="#name_label")
        )
        self.name_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(center_x - 140, 20, 200, 30),
            manager=self.manager
        )
        
        # Server IP input
        self.server_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(center_x - 250, 60, 100, 30),
            text="Server IP:",
            manager=self.manager,
            object_id=pygame_gui.core.ObjectID(class_id="@labels", object_id="#server_label")
        )
        self.server_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(center_x - 140, 60, 200, 30),
            manager=self.manager
        )
        
        # Connect button
        self.connect_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(center_x + 70, 60, 100, 30),
            text="Connect",
            manager=self.manager
        )
        
        # Current card display (centered, moved up)
        self.current_card_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(center_x - 100, 100, 200, 30),
            text="Current Card: None",
            manager=self.manager,
            object_id=pygame_gui.core.ObjectID(class_id="@labels", object_id="#current_card_label")
        )
        
        # Opponent cards display (moved further down to avoid card overlap)
        self.opponent_cards_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(center_x - 150, 280, 300, 30),
            text="Opponent Cards: 7",
            manager=self.manager,
            object_id=pygame_gui.core.ObjectID(class_id="@labels", object_id="#opponent_label")
        )
        
        # Draw card button (moved further down to avoid card overlap)
        self.draw_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(center_x - 75, 320, 150, 40),
            text="Draw Card",
            manager=self.manager
        )
    
    def load_card_images(self):
        card_images = {}
        card_folder = resource_path("cards")
        
        if not os.path.exists(card_folder):
            print(f"Error: Folder '{card_folder}' not found.")
            return card_images
        
        # Load all card images
        for color in ["Red", "Green", "Blue", "Yellow"]:
            for value in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "Draw Two"]:
                image_path = os.path.join(card_folder, f"{color}_{value}.png")
                try:
                    if os.path.exists(image_path):
                        image = pygame.image.load(image_path).convert_alpha()
                        image = pygame.transform.scale(image, (80, 120))
                        card_images[f"{color} {value}"] = image
                except Exception as e:
                    print(f"Error loading {image_path}: {e}")
        
        # Load special cards
        special_cards = ["Wild", "Draw Four"]
        for card in special_cards:
            filename = card
            image_path = os.path.join(card_folder, f"{card}.png")
            try:
                if os.path.exists(image_path):
                    image = pygame.image.load(image_path).convert_alpha()
                    image = pygame.transform.scale(image, (80, 120))
                    card_images[card] = image
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        
        return card_images
    
    def connect_to_server(self):
        self.server_ip = self.server_input.get_text()
        self.player_name = self.name_input.get_text()
        
        # if not self.server_ip:
        #     self.show_message("Error", "Please enter a server IP")
        #     return

        # assuming the aws server doesn't reset, just use this ip. If it does, make sure to update or just omit this and go back to the old way
        if not self.server_ip:
            self.server_ip = "3.131.38.246"
        
        if not self.player_name:
            self.show_message("Error", "Please enter your name")
            return
        
        try:
            self.client = start_client(self.server_ip, self)
            self.client.send(f"name:{self.player_name}".encode('utf-8'))
            self.connected = True
            self.show_message("Connected", f"Connected as {self.player_name}")
        except Exception as e:
            self.show_message("Error", f"Could not connect: {str(e)}")
    
    def update_hand(self, cards):
        self.hand = cards
        self.card_rects = []  # Reset card positions
    
    def play_sound(self, sound_file):
        sound_path = resource_path(sound_file)  # Use resource_path to locate the sound file
        pygame.mixer.init()
        sound = pygame.mixer.Sound(sound_path)
        sound.play()

    def update_current_card(self, card):
        self.current_card = card
        self.current_card_label.set_text(f"Current Card: {card}")
        if(card.startswith("Draw Four")):
            self.play_sound("sounds/Dramatic VineInstagram Boom - Sound Effect (HD) [TubeRipper.com].mp3")
    
    def update_opponent_cards(self, player1_cards, player2_cards):
        self.opponent_cards_label.set_text(f"Player 1: {player1_cards}, Player 2: {player2_cards}")
    
    def add_card_to_hand(self, card):
        self.hand.append(card)
    
    def show_winner(self, winner_id):
        self.show_message("Game Over", f"{winner_id} won!")
        self.play_sound("sounds/SpongeBob Production Music You're Nice.mp3")
    
    def show_message(self, title, message):
        pygame_gui.windows.UIMessageWindow(
            rect=pygame.Rect(self.screen_width//2 - 200, self.screen_height//2 - 100, 400, 200),
            html_message=message,
            window_title=title,
            manager=self.manager
        )
    
    def draw_game(self):
        self.screen.fill(self.BLUE)
        self.manager.draw_ui(self.screen)
        
        # Draw current card
        if hasattr(self, 'current_card') and self.current_card != "None":
            if self.current_card in self.card_images:
                card_img = self.card_images[self.current_card]
                card_rect = card_img.get_rect(center=(self.screen_width//2, 200))
                self.screen.blit(card_img, card_rect)
            else:
                # Fallback if image not found
                card_rect = pygame.Rect(0, 0, 80, 120)
                card_rect.center = (self.screen_width//2, 200)
                pygame.draw.rect(self.screen, self.WHITE, card_rect)
                card_text = self.font.render(self.current_card, True, self.BLACK)
                text_rect = card_text.get_rect(center=card_rect.center)
                self.screen.blit(card_text, text_rect)
        
        # Draw player's hand with 7 cards per row
        self.card_rects = []  # Reset before drawing
        if hasattr(self, 'hand'):
            cards_per_row = 7
            card_width, card_height = 80, 120
            padding = 10
            start_y = self.screen_height - card_height - 20
            
            for i, card in enumerate(self.hand):
                row = i // cards_per_row
                col = i % cards_per_row
                
                # Center the cards horizontally
                total_row_width = cards_per_row * (card_width + padding) - padding
                x = (self.screen_width - total_row_width) // 2 + col * (card_width + padding)
                y = start_y - row * (card_height + padding)
                
                card_rect = pygame.Rect(x, y, card_width, card_height)
                self.card_rects.append((card_rect, card))  # Store position and card
                
                if card in self.card_images:
                    # Draw card image if available
                    self.screen.blit(self.card_images[card], card_rect)
                else:
                    # Fallback if image not found
                    pygame.draw.rect(self.screen, self.WHITE, card_rect)
                    card_text = self.font.render(card, True, self.BLACK)
                    text_rect = card_text.get_rect(center=card_rect.center)
                    self.screen.blit(card_text, text_rect)
        
        pygame.display.flip()
    
    def handle_card_click(self, pos):
        for rect, card in self.card_rects:
            if rect.collidepoint(pos):
                if self.connected:
                    self.client.send(f"play:{card}".encode('utf-8'))
                    if(not card.startswith("Draw Four")):
                        self.play_sound("sounds/12732__leady__briefcase-click2.wav") # play sound when user plays a card
                    self.hand.remove(card)
                    return True
        return False
    
    def handle_resize(self, event):
        self.screen_width, self.screen_height = event.size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        self.manager.set_window_resolution((self.screen_width, self.screen_height))
        
        # Re-center all UI elements
        center_x = self.screen_width // 2
        
        self.name_label.set_position((center_x - 250, 20))
        self.name_input.set_position((center_x - 140, 20))
        self.server_label.set_position((center_x - 250, 60))
        self.server_input.set_position((center_x - 140, 60))
        self.connect_button.set_position((center_x + 70, 60))
        self.current_card_label.set_position((center_x - 100, 100))
        self.opponent_cards_label.set_position((center_x - 150, 280))
        self.draw_button.set_position((center_x - 75, 320))
    
    def run(self):
        running = True
        
        while running:
            time_delta = self.clock.tick(60)/1000.0
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.handle_card_click(event.pos)
                
                if event.type == pygame.VIDEORESIZE:
                    self.handle_resize(event)
                
                self.manager.process_events(event)
                
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.connect_button:
                            self.connect_to_server()
                        elif event.ui_element == self.draw_button:
                            if self.connected:
                                self.client.send("pickup".encode('utf-8'))
                                self.play_sound("sounds/683101__florianreichelt__quick-woosh.mp3") 
                            
            
            self.manager.update(time_delta)
            self.draw_game()
        
        pygame.quit()

if __name__ == "__main__":
    # Create a theme.json file for white text
    with open('theme.json', 'w') as f:
        f.write('''
        {
            "@labels": {
                "normal_text_color": "#FFFFFF",
                "text_horiz_alignment": "center"
            },
            "@buttons": {
                "normal_text_color": "#FFFFFF",
                "hovered_text_color": "#FFFFFF",
                "pressed_text_color": "#FFFFFF",
                "disabled_text_color": "#CCCCCC"
            },
            "@text_entry_lines": {
                "normal_text_color": "#000000",
                "focused_text_color": "#000000",
                "disabled_text_color": "#666666"
            },
            "#name_label": {
                "normal_text_color": "#FFFFFF"
            },
            "#server_label": {
                "normal_text_color": "#FFFFFF"
            },
            "#current_card_label": {
                "normal_text_color": "#FFFFFF"
            },
            "#opponent_label": {
                "normal_text_color": "#FFFFFF"
            }
        }
        ''')
    
    game = UnoGUI()
    game.run()