import pygame
import nordle

pygame.init()


# --- [1] UI SETUP AND CONSTANTS: Edit these to change the look of the game ---

# Screen dimensions
SCREEN_WIDTH = 650
SCREEN_HEIGHT = 700

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (120, 124, 126)
DARK_GREY = (60, 60, 60) # For empty grid cells
GREEN = (255, 15, 155) #change to pink
YELLOW = (201, 180, 88)
DEFAULT_BG = (18, 18, 19)

# Initialize fonts
font_path = "./HopeGold.ttf"
LETTER_FONT = pygame.font.Font(font_path, 55)
KEYBOARD_FONT = pygame.font.Font(font_path, 40)
TITLE_FONT = pygame.font.Font(font_path, 55)

# Grid settings
CELL_SIZE = 50
CELL_PADDING = 8
GRID_START_X = (SCREEN_WIDTH - (5 * (CELL_SIZE + CELL_PADDING) - CELL_PADDING)) // 2
GRID_START_Y = 100

# Keyboard settings
KEY_WIDTH = 40
KEY_HEIGHT = 45
KEY_PADDING = 8
KEYBOARD_ROWS = [
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM"
]
KEYBOARD_START_Y = GRID_START_Y + 6 * (CELL_SIZE + CELL_PADDING) + 50

# --- [2] UI CLASS: Manages UI state and input ---

class WordleUI:
    def __init__(self):
        # --- UI State Variables ---
        # These variables control what is shown on the screen.
        # Your backend will provide the values to update them.
        
        self.guesses = [[""] * 5 for _ in range(6)]
        self.tile_colors = [[DARK_GREY] * 5 for _ in range(6)]
        self.keyboard_colors = {letter: GREY for row in KEYBOARD_ROWS for letter in row}
        
        self.current_attempt = 0
        self.current_char_index = 0
        self.message = ""
        self.is_game_over = False
        self.original_candidates = open("word_lists/wordle-candidates.txt").read().split('\n')
        self.candidates = self.original_candidates

        self.keyboard_rects = self._create_keyboard_rects()

    def _create_keyboard_rects(self):
        """Pre-calculates the Rect objects for each keyboard key for easy drawing and clicking."""
        rects = {}
        y = KEYBOARD_START_Y
        for i, row_str in enumerate(KEYBOARD_ROWS):
            row_width = len(row_str) * (KEY_WIDTH + KEY_PADDING) - KEY_PADDING
            x_start = (SCREEN_WIDTH - row_width) // 2
            for j, letter in enumerate(row_str):
                x = x_start + j * (KEY_WIDTH + KEY_PADDING)
                rects[letter] = pygame.Rect(x, y, KEY_WIDTH, KEY_HEIGHT)
            y += KEY_HEIGHT + KEY_PADDING
        return rects

    def handle_input(self, event):
        """Processes a single key press or mouse click. Calls your logic when needed."""
        if self.is_game_over:
            # Optional: You could add a hook here to listen for an "Enter" key
            # press to reset the game.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.reset_game()
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.current_char_index == 5:
                    self.submit_guess() # This is where your logic gets called
            elif event.key == pygame.K_BACKSPACE:
                self.delete_char()
            elif event.unicode.isalpha() and self.current_char_index < 5:
                self.add_char(event.unicode.upper())
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for letter, rect in self.keyboard_rects.items():
                if rect.collidepoint(event.pos):
                    self.add_char(letter)
                    break

    def add_char(self, char):
        """UI ONLY: Adds a character to the current guess grid."""
        if self.current_char_index < 5:
            self.guesses[self.current_attempt][self.current_char_index] = char
            self.current_char_index += 1

    def delete_char(self):
        """UI ONLY: Deletes the last character from the current guess grid."""
        if self.current_char_index > 0:
            self.current_char_index -= 1
            self.guesses[self.current_attempt][self.current_char_index] = ""

    # --------------------------------------------------------------------------
    ### HOOK #1: SUBMIT GUESS - PLUG YOUR BACKEND LOGIC IN HERE ###
    # --------------------------------------------------------------------------
    def submit_guess(self):
        """
        This is the main bridge to your backend.
        It's called when the user hits Enter.
        """
        current_guess_str = "".join(self.guesses[self.current_attempt]).lower()
        print(f"UI: Submitting guess '{current_guess_str}' to backend.")

        results = nordle.getPattern(current_guess_str, self.candidates)
        if results == -1:
            return #do not allow invalid guesses

        self.candidates = results[1]
        results = results[0]
        
        for i in range(0, len(results)):
            if results[i] == 'g':
                results[i] = GREEN
            elif results[i] == 'b':
                results[i] = DARK_GREY
            elif results[i] == 'y':
                results[i] = YELLOW

        current_guess_str = current_guess_str.upper() #for keyboard_colors to work
        is_game_over_lose = self.current_attempt == 5 and results.count(GREEN) < 5 
        is_game_over_win = results.count(GREEN) == 5 
        #BUG with keyboard colors: if two of the same letter in guess, gives color of second letter and not of first
        formatted_results = {
            "tile_colors": [GREY if x == DARK_GREY else x for x in results ],
            "keyboard_colors": {current_guess_str[0]: results[0], current_guess_str[1]: results[1], current_guess_str[2]: results[2], current_guess_str[3]: results[3], current_guess_str[4]: results[4]},
            "message": nordle.getMessage(is_game_over_win, is_game_over_lose),
            "game_over": is_game_over_win or is_game_over_lose
        }
        
        # 2. UPDATE THE UI WITH THE RESULTS FROM YOUR BACKEND
        #    Use the helper function below to update the UI state.
        self.update_ui_from_backend(
            tile_colors=formatted_results["tile_colors"],
            keyboard_updates=formatted_results["keyboard_colors"],
            message=formatted_results["message"],
            is_game_over=formatted_results["game_over"]
        )

    def update_ui_from_backend(self, tile_colors, keyboard_updates, message, is_game_over):
        """Helper function to update all UI elements based on backend results."""
        self.tile_colors[self.current_attempt] = tile_colors
        
        # Update keyboard colors based on the new information
        for letter, color in keyboard_updates.items():
            self.keyboard_colors[letter] = color
            
        self.message = message
        self.is_game_over = is_game_over

        # Move to the next line for the next guess
        if not self.is_game_over:
            self.current_attempt += 1
            self.current_char_index = 0
            
    # --------------------------------------------------------------------------
    ### HOOK #2: RESET GAME - PLUG YOUR BACKEND RESET LOGIC IN HERE ###
    # --------------------------------------------------------------------------
    def reset_game(self):
        """Resets the UI to its initial state for a new game."""
        print("UI: Resetting for a new game.")

        self.candidates = self.original_candidates

        #reset all ui
        self.guesses = [[""] * 5 for _ in range(6)]
        self.tile_colors = [[DARK_GREY] * 5 for _ in range(6)]
        self.keyboard_colors = {letter: GREY for row in KEYBOARD_ROWS for letter in row}
        
        self.current_attempt = 0
        self.current_char_index = 0
        self.message = ""
        self.is_game_over = False

# --- [3] DRAWING FUNCTIONS: These render the UI state to the screen ---

def draw_grid(screen, ui):
    for row in range(6):
        for col in range(5):
            x = GRID_START_X + col * (CELL_SIZE + CELL_PADDING)
            y = GRID_START_Y + row * (CELL_SIZE + CELL_PADDING)
            
            cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            color = ui.tile_colors[row][col]

            pygame.draw.rect(screen, color, cell_rect, border_radius=3)
            
            # Draw border for cells that are being typed in or are empty
            if color == DARK_GREY:
                 pygame.draw.rect(screen, GREY, cell_rect, 2, border_radius=3)

            # Draw the letter inside the cell
            letter = ui.guesses[row][col]
            if letter:
                text_surface = LETTER_FONT.render(letter, True, WHITE)
                text_rect = text_surface.get_rect(center=(cell_rect.center[0]+2, cell_rect.center[1]-5))
                screen.blit(text_surface, text_rect)

def draw_keyboard(screen, ui):
    for letter, rect in ui.keyboard_rects.items():
        color = ui.keyboard_colors[letter]
        pygame.draw.rect(screen, color, rect, border_radius=5)

        text_surface = KEYBOARD_FONT.render(letter, True, WHITE)
        text_rect = text_surface.get_rect(center=(rect.center[0]+2, rect.center[1]-5))
        screen.blit(text_surface, text_rect)

def draw_header_and_messages(screen, ui):
    # Title
    title_surface = TITLE_FONT.render("NORDLE", True, WHITE)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(title_surface, title_rect)

    img = pygame.image.load('heart.png')
    screen.blit(img,(SCREEN_WIDTH // 3 , 38))
    screen.blit(img,(SCREEN_WIDTH // 1.635 , 38))
    
    # Game message
    if ui.message:
        msg_surface = KEYBOARD_FONT.render(ui.message, True, WHITE)
        msg_rect = msg_surface.get_rect(center=(SCREEN_WIDTH // 2, GRID_START_Y + 365))
        screen.blit(msg_surface, msg_rect)




