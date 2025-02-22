import pygame
import tkinter as tk
import os
import sys
import pyttsx3
import random
import json
from tkinter import messagebox
from datetime import datetime

# Initialize Pygame and pyttsx3
pygame.init()
pygame.font.init()
pygame.mixer.init()
engine = pyttsx3.init()

# Initial setting for music
music_on = True  # Assuming music is on by default
sound_volume = 1

HOVER_BORDER_COLOR = (255, 215, 0)  # Gold color for hover border
BORDER_COLOR = (0, 0, 0)            # Black color for general borders

# Font
FONT1 = pygame.font.Font(None, 62)
FONT2 = pygame.font.Font(None, 36)

# Screen settings
screen_width = 900
screen_height = 600
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
TOP_MARGIN = 50

# Dark theme colors
DARK_TEXT_COLOR = (255, 255, 255)
DARK_BUTTON_COLOR = (139, 69, 19)
DARK_BUTTON_BORDER_COLOR = (34, 139, 34)
DARK_BUTTON_HOVER_COLOR = (184, 134, 11)
DARK_BG_COLOR = (47, 79, 79)

BG_COLOR = (255, 255, 255)
FOUND_COLOR = (0, 255, 0)  # Green color
HINT_COLOR = (245, 222, 179)  
TEXT_COLOR = (0, 0, 0)
BUTTON_BORDER_COLOR = (100, 100, 100)  # New border color for buttons
TEXT_BORDER_COLOR = (255, 255, 255)  # White border for text
BUTTON_COLOR = (70, 130, 180)
SHADOW_COLOR = (200, 200, 200)
SHADOW_OFFSET = 3
GRID_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (200, 200, 200)
HOVER_BORDER_COLOR = (0, 0, 0)
BORDER_COLOR = (0, 0, 0)
COMPLETED_COLOR = (100, 255, 100)  # Light green for completed levels
HIGHLIGHT_COLOR = (255, 255, 100)  # Light yellow for current level
LOCKED_COLOR = (255, 100, 100)  # Light red for locked levels
GOLDEN_COLOR = (255, 215, 0)
FONT_SIZE = 36
FONT = pygame.font.Font(None, FONT_SIZE)

# Initialize the list of colors
WORD_COLORS = [
    (0, 255, 0),   # Green
    (0, 0, 255),   # Blue
    (255, 0, 0),   # Red
    (255, 165, 0), # Orange
    (128, 0, 128), # Purple
    (0, 255, 255), # Cyan
    (255, 192, 203), # Pink
    (165, 42, 42), # Brown
    (255, 255, 0), # Yellow
    (0, 128, 128), # Teal
    (255, 105, 180), # Hot Pink
    (75, 0, 130),  # Indigo
    (255, 20, 147), # Deep Pink
    (218, 112, 214), # Orchid
    (138, 43, 226), # Blue Violet
    (255, 69, 0),  # Red Orange
    (46, 139, 87), # Sea Green
    (186, 85, 211),# Medium Orchid
    (128, 128, 0), # Olive
    (210, 105, 30) # Chocolate
]

# Initialize a list to store the colors assigned to each found word
found_word_colors = []
# Initialize the list to store the cells of the found words
found_words_cells = []

# Load sound effects
click_sound = pygame.mixer.Sound('click.wav')  # Ensure you have this sound in the same directory
correct_sound = pygame.mixer.Sound('correct.mp3')  # Ensure you have this sound in the same directory
background_music = pygame.mixer.Sound("background_music.mp3")

# Load assets
INTRO_IMAGE = pygame.image.load('background3.png')
INTRO_IMAGE = pygame.transform.scale(INTRO_IMAGE, (screen_width, screen_height))
level_background = pygame.image.load('level_background.jpg')
level_background = pygame.transform.scale(level_background, (screen_width, screen_height))

# Game variables
EASY_TIME_LIMIT = 300  # seconds (5 minutes)
MEDIUM_TIME_LIMIT = 180  # seconds (3 minutes)
HARD_TIME_LIMIT = 120  # seconds (2 minutes)    

# Game variables
EASY_HINTS = 5
MEDIUM_HINTS = 3
HARD_HINTS = 1
hints_remaining = 0

words_found = 0
hints_used = 0
mistakes_made = 0
level_completed = False
time_remaining = 0
levels_completed_flawlessly = 0
all_words_found = False
levels_completed_speedily = 0
levels_completed_without_hints = 0
levels_completed_consecutively = 0
consecutive_days_played = 0
levels_completed = 0
night_gaming_hours = 0

# Cooldown variables
HINT_COOLDOWN_DURATION = 10  # seconds (adjust as needed)
hint_cooldown_remaining = 0

level = 1
selected_word = ""
selected_cells = []
found_words_lls = []
mouse_down = False
game_state = "MENU"  # States: MENU, GAME, INSTRUCTIONS, LEVELS
previous_state = "MENU"
score = 0
completed_levels = []
max_level = 1
multiplier = 1
penalty = 10
display_new_grid = False
is_selecting = False
is_scrolling  = True

# Initialize video playback variables
video = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video.mp4')
is_playing = True
video_speed = 1.0

# Function to draw button
def draw_button(button_rect, text):
    font_small = pygame.font.SysFont("Arial", 30)
    TEXT_COLOR = (0, 0, 0)
    BUTTON_COLOR = (166, 121, 52)
    BUTTON_HOVER_COLOR = (134, 200, 168)
    BUTTON_BORDER_COLOR = (100, 100, 100)
    bg_color = BUTTON_COLOR
    hover_color = BUTTON_HOVER_COLOR
    text_color = (255,255,255)
    border_color = (255,255,255)

    if button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, hover_color, button_rect, border_radius=10)
    else:
        pygame.draw.rect(screen, bg_color, button_rect, border_radius=10)
    pygame.draw.rect(screen, border_color, button_rect, width=3, border_radius=10)
    render_centered_text_wob(text, font_small, text_color, button_rect.centerx, button_rect.centery)
#without border
def render_text_wob(text, x, y, font, color):
    global dark_mode
    text_surface = font.render(text, True, (255,255,255))
    screen.blit(text_surface, (x, y))
#without border
def render_centered_text_wob(text, font, color, center_x, center_y):
    global dark_mode
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    screen.blit(text_surface, text_rect)

# def play_video(video_path=video):
#     global is_playing, video_speed

#     # Load video using ffpyplayer
#     player = MediaPlayer(video_path)
#     clock = pygame.time.Clock()

#     # Define buttons
#     backward_button = pygame.Rect(screen_width // 2 - 280, screen_height - 70, 100, 50)
#     play_pause_button = pygame.Rect(screen_width // 2 - 160, screen_height - 70, 100, 50)
#     forward_button = pygame.Rect(screen_width // 2 - 40, screen_height - 70, 100, 50)
#     speed_button = pygame.Rect(screen_width // 2 + 80, screen_height - 70, 100, 50)
#     back_button = pygame.Rect(screen_width // 2 + 200, screen_height - 70, 100, 50)

#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if play_pause_button.collidepoint(event.pos):
#                     is_playing = not is_playing
#                 elif forward_button.collidepoint(event.pos):
#                     player.seek(10)  # Seek forward 10 seconds
#                 elif backward_button.collidepoint(event.pos):
#                     player.seek(-10)  # Seek backward 10 seconds
#                 elif speed_button.collidepoint(event.pos):
#                     video_speed = 2.0 if video_speed == 1.0 else 1.0
                    
#                 elif back_button.collidepoint(event.pos):
#                     player.close_player()
#                     return  # Go back to the instruction screen

#         if is_playing:
#             frame, val = player.get_frame()
#             if val == 'eof':
#                 player.seek(0)  # Restart video on end
#             if frame is not None:
#                 img, t = frame
#                 # Convert frame to Pygame surface
#                 frame_surface = pygame.image.frombuffer(img.to_bytearray()[0], img.get_size(), "RGB")
                
#                 # Scale the video to fit the screen (600x500 in this case)
#                 frame_surface = pygame.transform.scale(frame_surface, (600, 450))
                
#                 screen.fill((0,0,0))
#                 screen.blit(level_background, (0, 0))
#                 screen.blit(frame_surface, (133, 50))  # Center the video on screen

#         # Draw buttons
#         buttons = [
#             (backward_button, '<<'),
#             (play_pause_button, 'Pause' if is_playing else 'Play'),
#             (forward_button, '>>'),
#             (speed_button, 'Speed' if video_speed == 1.0 else 'Normal'),
#             (back_button, 'Back')
#         ]

#         for button_rect, text in buttons:
#             draw_button(button_rect, text)

#         pygame.display.flip()
#         clock.tick(30*video_speed)

def show_intro():
    screen.blit(INTRO_IMAGE, (0, 0))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                waiting = False

easy_words = [
    "MAKE", "GATE", "NOTE", "VIEW", "EXIT", "ZONE", "HAND", "JOIN", "VARY",
    "LINE", "BOSS", "GOOD", "SEND", "LOAD", "VOTE", "BIRD", "HEAD", "TAKE", "FACT",
    "FALL", "RISE", "JURY", "TIME", "CITY", "TINY", "TREE", "ECHO", "HIGH", "LOST",
    "JUMP", "WEEK", "TEST", "BACK", "WELL", "GAME", "CORE", "PATH", "PAGE", "SELF",
    "BLUE", "GIVE", "WIND", "KING", "TASK", "FOUR", "ROAD", "LEFT", "WALL", "MEAL",
    "SHOT", "SONG", "SAVE", "DATA", "PASS", "PLAN", "HELP", "BANK", "DATE", "MOVE",
    "LIVE", "MILD", "MUST", "FORD", "AREA", "ARMY", "BABY", "BALL", "BAND",
    "BASE", "BILL", "BODY", "BOOK", "CALL", "CARD", "CARE", "CASE", "CLUB", "COST",
    "DEAL", "DESK", "DOOR", "DUTY", "EAST", "EDGE", "FACE", "FARM", "FEAR", "FILE",
    "FILM", "FIRE", "FOOD", "FUND", "SIDE"
]

medium_words = [
    "TRAVEL", "SCHOOL", "YELLOW", "ORANGE", "PURPLE", "VIOLET", "BANANA", "COFFEE", 
    "FRIEND", "SUNSET", "HIKING", "BEACH",  "DOCTOR", "FARMER", "LAWYER", "DRIVER", 
    "ARTIST", "AUTHOR", "SINGER", "STRONG", "RUNNER", "BAKING", "CARING", "KINDLY", 
    "JOYFUL", "PARENT", "CHILD", "BRIGHT",  "PILLOW", "CARPET", "WINDOW", "BUTTON", 
    "MIRROR", "BOTTLE", "ERASER", "CAMERA", "REMOTE", "TOYS", "GAMES", "LADDER", 
    "HANDLE", "TROPHY", "STATUE", "PLANET", "FOREST", "JUNGLE", "VALLEY", "ISLAND", 
    "BEACON", "TEMPLE", "CASTLE", "BUTTER", "CHEESE", "YOGURT", "CEREAL", "COOKIE", 
    "PEPPER", "SALMON", "SHRIMP", "PICKLE", "GARLIC", "ALMOND", "HAZELNUT", "WALNUT", 
    "CASHEW", "PISTACHIO", "PEANUT", "RAISIN"
]

hard_words = [
    "WALLET", "FINGER", "BRAINY", "BRANCH", "SHOULD", "SEASON", "MARBLE", "COTTON", 
    "RUBBER", "LETTER", "POLICE", "OFFICE", "GARDEN", "DESERT", "PLANET", "AUTHOR", 
    "SUNSET", "FRIEND", "PEPPER", "ERASER", "REMOTE", "TOYS", "BUTTON", "MIRROR", 
    "PLANET", "HANDLE", "TROPHY", "STATUE", "ISLAND", "JUNGLE", "BEACON", "TEMPLE", 
    "LADDER", "PILLOW", "CARPET", "WINDOW", "BUTTON", "BOTTLE", "CAMERA", "REMOTE", 
    "FOREST", "JUNGLE", "VALLEY", "ISLAND", "BEACON", "TEMPLE", "CASTLE", "BUTTER", 
    "CHEESE", "YOGURT", "COOKIE", "SALMON", "SHRIMP", "PICKLE", "TOMATO", "CASHEW", 
    "PEANUT", "RAISIN", "GRAPES", "WALLET", "FINGER", "BRAINY", "BRANCH", "SHOULD", 
    "SEASON", "MARBLE", "RUBBER", "LETTER", "FOREST", "ORANGE", "POLICE", "OFFICE", 
    "FRIEND", "DESERT", "HANDLE", "DRIVER", "DOCTOR", "ARTIST", "SINGER", "WRITER", 
    "LOVING", "PARENT", "BRIGHT", "PILLOW", "CARPET", "WINDOW", "BUTTON", "CAMERA", 
    "REMOTE", "PILLOW", "YOGURT", "ALMOND", "SHOULD", "GARDEN", "LOVING", "BUTTER", 
    "STATUE", "TEMPLE", "BRIDGE", "FOREST", "TRAVEL", "COFFEE", "WRITER", "HANDLE", 
    "BRIGHT", "CEREAL", "COTTON", "GRAPES", "BLACK", "DESERT", "ELEPHANT", "KANGAROO", 
    "DOLPHIN", "CHOCOLATE", "STRAWBERRY", "PINEAPPLE", "WATERMELON", "CELEBRATE", 
    "BIRTHDAY", "GRADUATION", "HONEYMOON", "ANNIVERSARY", "CHRISTMAS", "THANKSGIVING", 
    "HAPPINESS", "CREATIVITY", "ADVENTURE", "IMAGINATION", "INSPIRATION", "MOTIVATION", 
    "OPPORTUNITY", "INTEGRITY", "LEADERSHIP", "FRIENDSHIP", "KINDNESS", "GENEROSITY", 
    "HONESTY", "POLITENESS", "ENTHUSIASM", "DEDICATION", "COMMITMENT", "RESPONSIBILITY", 
    "COMMUNICATION", "UNDERSTANDING", "COMMUNITY", "NEIGHBORHOOD", "ENVIRONMENT", 
    "SUSTAINABILITY", "CONSERVATION", "RECYCLING", "RECOGNITION", "ACHIEVEMENT", 
    "DEVELOPMENT", "IMPROVEMENT", "GROWTH", "ADVANCEMENT", "INNOVATION", "INVENTION", 
    "BREAKTHROUGH", "DISCOVERY", "EXPLORATION", "INVESTIGATION", "DATABASE", "INFORMATION", 
    "TECHNOLOGY", "SOFTWARE", "HARDWARE", "NETWORK", "INTERFACE", "AUTOMATION", "ENGINEERING", 
    "MANUFACTURING", "CONSTRUCTION", "ARCHITECTURE", "DESIGNING", "LOGISTICS", "DISTRIBUTION", 
    "SUPPLY", "DEMAND", "PROCUREMENT", "INVENTORY", "WAREHOUSE", "COMMERCE", "BUSINESS", 
    "MARKETING", "ADVERTISING", "PROMOTION", "BRANDING", "SALES", "ECONOMY", "FINANCE", 
    "ACCOUNTING", "BUDGETING", "AUDITING", "TAXATION", "INSURANCE", "REALESTATE", "PROPERTY", 
    "URBAN", "PLANNING", "ZONING", "GOVERNMENT", "POLITICS", "DIPLOMACY", "NEGOTIATION", 
    "LEGISLATION", "JURISDICTION", "MANAGEMENT", "SUPERVISION", "COORDINATION", "IMPLEMENTATION", 
    "MAINTENANCE", "OPTIMIZATION", "EFFICIENCY", "EDUCATION", "LEARNING", "TEACHING", "TRAINING", 
    "INSTRUCTION", "CURRICULUM", "SYLLABUS", "RESEARCH", "SCHOLARSHIP", "FELLOWSHIP", "INTERNSHIP", 
    "APPRENTICESHIP", "PROFESSIONAL", "EXPERIENCE", "KNOWLEDGE", "SKILLS", "ABILITIES", 
    "COMPETENCIES", "CAPABILITIES", "EXCELLENCE", "PERFECTION", "DISTINCTION", "SUPERIORITY", 
    "BRILLIANCE", "GENIUS", "TALENT", "CAPABILITY", "POTENTIAL", "CAPACITY", "STRENGTH", 
    "ENDURANCE", "STAMINA", "RESILIENCE", "SUSTAINABILITY", "ECOFRIENDLY", "ENVIRONMENTAL", 
    "BIODIVERSITY", "PRESERVATION", "ENERGY", "SOLAR", "WIND", "HYDRO", "GEOTHERMAL", "BIOMASS", 
    "BIOENERGY", "BIOFUEL", "BIODEGRADABLE", "RENEWABLE", "NONRENEWABLE", "FOSSILFUEL", "CARBON", 
    "FOOTPRINT", "EMISSIONS", "POLAR", "CLIMATE", "CHANGE", "GLOBAL", "WARMING", "WEATHER", 
    "METEOROLOGY", "ATMOSPHERE", "STRATOSPHERE", "TROPOSPHERE", "OZONE", "LAYER", "GREENHOUSE", 
    "GASES", "CARBON", "DIOXIDE", "METHANE", "NITROUSOXIDE", "CHLOROFLUOROCARBONS", "HYDROFLUOROCARBONS", 
    "PERFLUOROCARBONS", "SULFURHEXAFLUORIDE", "DEFORESTATION", "REFORESTATION", "AFFORESTATION", 
    "DESERTIFICATION", "URBANIZATION", "INDUSTRIALIZATION", "AGRICULTURE", "CULTIVATION", "HORTICULTURE", 
    "FLORICULTURE", "AGRIBUSINESS", "FOOD", "SECURITY", "NUTRITION", "DIET", "HEALTH", "WELLNESS", 
    "FITNESS", "EXERCISE", "SPORTS", "ATHLETICS", "TRAINING", "COACHING", "MENTORING", "LEADERSHIP", 
    "MANAGEMENT", "ADMINISTRATION", "ORGANIZATION", "PLANNING", "STRATEGY", "TACTICS", "OPERATIONS", 
    "LOGISTICS", "COORDINATION", "COLLABORATION", "PARTNERSHIP", "TEAMWORK", "SYNERGY", "DYNAMICS", 
    "INNOVATION", "CREATIVITY", "ENTREPRENEURSHIP", "STARTUP", "BUSINESS", "ENTERPRISE", "VENTURE", 
    "CAPITAL", "INVESTMENT", "FINANCE", "ECONOMICS", "MARKETING", "ADVERTISING", "BRANDING", "PROMOTION", 
    "PUBLIC", "RELATIONS", "COMMUNICATIONS", "JOURNALISM", "BROADCASTING", "MEDIA", "PUBLISHING", 
    "PRINT", "ONLINE", "DIGITAL", "SOCIAL", "NETWORKING", "PLATFORM", "WEBSITE", "APPLICATION"
]

# Global list to track used words
used_words = []
high_score = 0
difficulty = "medium"
GRID_SIZE = 10

def generate_random_grid_and_words(GRID_SIZE,used_words, difficulty):
    # Merge word lists based on difficulty
    if difficulty == "easy":
        MAX_WORDS = 10
        available_words = [word for word in easy_words if word not in used_words]
    elif difficulty == "medium":
        MAX_WORDS = 15
        available_words = [word for word in (easy_words + medium_words) if word not in used_words]
    else:  # hard
        MAX_WORDS = 20
        available_words = [word for word in (easy_words + medium_words + hard_words) if word not in used_words]

    # Ensure unique word selection based on MAX_WORDS
    words = []
    remaining_words = MAX_WORDS

    if difficulty in ["medium", "hard"]:
        for word_list in [easy_words, medium_words, hard_words]:
            if remaining_words > 0:
                new_words = [word for word in word_list if word not in used_words and word not in words]
                words.extend(random.sample(new_words, min(len(new_words), remaining_words)))
                remaining_words = MAX_WORDS - len(words)
    else:  # easy
        words = random.sample(available_words, min(len(available_words), MAX_WORDS))
    
    used_words.extend(words)

    # Initialize empty grid
    grid = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # Place words in grid
    for word in words:
        placed = False
        while not placed:
            directions = ['horizontal', 'vertical']
            if difficulty == "hard":
                directions.append('diagonal')
            direction = random.choice(directions)

            if direction == 'horizontal':
                row = random.randint(0, GRID_SIZE - 1)
                col = random.randint(0, GRID_SIZE - len(word))
                if all(grid[row][col + i] in ('', letter) for i, letter in enumerate(word)):
                    for i, letter in enumerate(word):
                        grid[row][col + i] = letter
                    placed = True
            elif direction == 'vertical':
                row = random.randint(0, GRID_SIZE - len(word))
                col = random.randint(0, GRID_SIZE - 1)
                if all(grid[row + i][col] in ('', letter) for i, letter in enumerate(word)):
                    for i, letter in enumerate(word):
                        grid[row + i][col] = letter
                    placed = True
            elif direction == 'diagonal':
                row = random.randint(0, GRID_SIZE - len(word))
                col = random.randint(0, GRID_SIZE - len(word))
                if all(grid[row + i][col + i] in ('', letter) for i, letter in enumerate(word)):
                    for i, letter in enumerate(word):
                        grid[row + i][col + i] = letter
                    placed = True

    # Fill empty cells with random letters
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == '':
                grid[row][col] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    return words, grid

# Initialize screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Word Puzzle Game")

# Initialize game grid and words
words, word_grid = generate_random_grid_and_words(GRID_SIZE,used_words, difficulty)
cell_size = (SCREEN_HEIGHT - TOP_MARGIN) // len(word_grid)

# Load the background image
BG_IMAGE = pygame.image.load('background2.jpg')
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (screen_width, screen_height))
bg_width, bg_height = BG_IMAGE.get_size()

BUTTON_BORDER_COLOR = (100, 100, 100)  # New border color for buttons
TEXT_BORDER_COLOR = (255, 255, 255)  # White border for text

def draw_text_with_border(surface, text, font, color, border_color, pos):
    # Draw the border
    border_surface = font.render(text, True, border_color)
    border_rect = border_surface.get_rect(center=pos)
    offsets = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
    for offset in offsets:
        surface.blit(border_surface, (border_rect.x + offset[0], border_rect.y + offset[1]))
    # Draw the main text
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)
    surface.blit(text_surface, text_rect)

CELL_SIZE = 50

def get_cells_in_line(start, end):
    """Returns a list of cells between start and end if they form a valid line."""
    start_row, start_col = start
    end_row, end_col = end

    cells_in_line = []
   # Check if the cells are in a straight line (horizontal, vertical, diagonal)
    if start_row == end_row:  # Horizontal
        step = 1 if start_col < end_col else -1
        for col in range(start_col, end_col + step, step):
            cells_in_line.append((start_row, col))
    elif start_col == end_col:  # Vertical
        step = 1 if start_row < end_row else -1
        for row in range(start_row, end_row + step, step):
            cells_in_line.append((row, start_col))
    elif abs(start_row - end_row) == abs(start_col - end_col):  # Diagonal
        row_step = 1 if start_row < end_row else -1
        col_step = 1 if start_col < end_col else -1
        for i in range(abs(start_row - end_row) + 1):
            cells_in_line.append((start_row + i * row_step, start_col + i * col_step))

    return cells_in_line

def draw_grid():
    TEXT_COLOR = (0, 0, 0)
    HINT_COLOR = (245, 222, 179)  
    BUTTON_BORDER_COLOR = (100, 100, 100)  # New border color for buttons
    TEXT_BORDER_COLOR = (255, 255, 255)  # White border for text
    HIGHLIGHT_COLOR = (255, 255, 100)  # Light yellow for current level
    FONT = pygame.font.Font(None, 30)
    screen.blit(level_background, (0, 0))

    for row in range(len(word_grid)):
        for col in range(len(word_grid[0])):
            cell_value = word_grid[row][col]
            cell_rect = pygame.Rect(col * CELL_SIZE, TOP_MARGIN + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            found = False
            for i, cells in enumerate(found_words_cells):
                if (row, col) in cells:
                    color = found_word_colors[i]
                    pygame.draw.rect(screen, color, cell_rect, border_radius=10)
                    found = True
                    break
            if not found:
                if (row, col) in selected_cells:
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, cell_rect, border_radius=10)
                elif (row, col) in highlighted_hint_word_cells:
                    pygame.draw.rect(screen, HINT_COLOR, cell_rect, border_radius=10)
                else:
                    pygame.draw.rect(screen, (200, 200, 200), cell_rect, border_radius=10)  #(200, 200, 200)  light grey
            
            text_pos = (col * CELL_SIZE + CELL_SIZE // 2, TOP_MARGIN + row * CELL_SIZE + CELL_SIZE // 2)
            draw_text_with_border(screen, cell_value, FONT, TEXT_COLOR, TEXT_BORDER_COLOR, text_pos)

    if selected_cells:
        start_cell = selected_cells[0]
        end_cell = selected_cells[-1]
        start_pos = (start_cell[1] * CELL_SIZE + CELL_SIZE // 2, TOP_MARGIN + start_cell[0] * CELL_SIZE + CELL_SIZE // 2)
        end_pos = (end_cell[1] * CELL_SIZE + CELL_SIZE // 2, TOP_MARGIN + end_cell[0] * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.line(screen, (0, 255, 0), start_pos, end_pos, 5)  # Draw the strip line

    # Display the words
    x_offset = SCREEN_WIDTH + 20
    y_offset = TOP_MARGIN + 30
    for word in words:
        draw_text_with_border(screen, word, FONT, TEXT_COLOR, TEXT_BORDER_COLOR, (x_offset, y_offset))
        y_offset += FONT_SIZE + 10
        if y_offset > SCREEN_HEIGHT - 170:
            y_offset = TOP_MARGIN + 30
            x_offset += 150  # Adjust offset for next column

    # Display the level
    level_text = FONT.render(f"Level: {level}", True, TEXT_COLOR)
    screen.blit(level_text, (20, 10))
    # Display the hints remaining
    hints_text = FONT.render(f"Hints: {hints_remaining}", True, TEXT_COLOR)
    screen.blit(hints_text, (125, 10))
    # Display the mistakes made
    mistakes_text = FONT.render(f"Mistakes: {mistakes_made}", True, TEXT_COLOR)
    screen.blit(mistakes_text, (230, 10))
    # Display the hint cooldown remaining
    hint_cooldown_text = FONT.render(f"Hint cooldown: {hint_cooldown_remaining}", True, TEXT_COLOR)
    screen.blit(hint_cooldown_text, (370, 10))

    # Create buttons using create_button function
    back_button = create_button(screen_width - 290, SCREEN_HEIGHT - 80, 150, 50, "Back", FONT, TEXT_COLOR, (166, 121, 52), (134, 200, 168), BUTTON_BORDER_COLOR, border_radius=50)
    save_button = create_button(screen_width - 200, SCREEN_HEIGHT - 140, 150, 50, "Save", FONT, TEXT_COLOR, (166, 121, 52), (134, 200, 168), BUTTON_BORDER_COLOR, border_radius=50)
    hint_button = create_button(screen_width - 380, SCREEN_HEIGHT - 140, 150, 50, "Hint", FONT, TEXT_COLOR, (166, 121, 52), (134, 200, 168), BUTTON_BORDER_COLOR, border_radius=50)

    # Render buttons using render_button function
    render_button(screen, back_button)
    render_button(screen, save_button)
    render_button(screen, hint_button)

    return back_button["rect"], save_button["rect"], hint_button["rect"]

highlighted_hint_word_cells = []

def provide_hint():
    global hints_remaining, hints_used, found_words_cells, hint_cooldown_remaining, highlighted_hint_word_cells
    
    if hints_remaining > 0 and hint_cooldown_remaining == 0:
        hints_remaining -= 1
        hints_used += 1
        check_achievements()
        hint_cooldown_remaining = HINT_COOLDOWN_DURATION  # Start cooldown
        unselected_words = [word for word in words if word not in found_words_cells]
        if unselected_words:
            hint_word = random.choice(unselected_words)
            for i, row in enumerate(word_grid):
                for j, cell in enumerate(row):
                    if cell == hint_word[0]:
                        # Check horizontally
                        if j + len(hint_word) <= len(row) and word_grid[i][j:j+len(hint_word)] == list(hint_word):
                            highlighted_hint_word_cells = [(i, j+k) for k in range(len(hint_word))]
                            return
                        # Check vertically
                        if i + len(hint_word) <= len(word_grid) and [word_grid[i+k][j] for k in range(len(hint_word))] == list(hint_word):
                            highlighted_hint_word_cells = [(i+k, j) for k in range(len(hint_word))]
                            return
                        # Check diagonally
                        if j + len(hint_word) <= len(row) and i + len(hint_word) <= len(word_grid) and [word_grid[i+k][j+k] for k in range(len(hint_word))] == list(hint_word):
                            highlighted_hint_word_cells = [(i+k, j+k) for k in range(len(hint_word))]
                            return
        speak(f"Hint used. {hints_remaining} hints remaining.")
    elif hint_cooldown_remaining > 0:
        speak(f"Hint on cooldown. {hint_cooldown_remaining} seconds remaining.")
    else:
        speak("No hints remaining.")

def speak(text):
    if sound_volume > 0:
        engine.say(text)
        engine.runAndWait()

def handle_click(pos):
    global selected_word, selected_cells, is_selecting, found_words_cells, score

    col = pos[0] // CELL_SIZE
    row = (pos[1] - TOP_MARGIN) // CELL_SIZE

    if 0 <= row < len(word_grid) and 0 <= col < len(word_grid[0]):
        if not is_selecting:
            # Start selecting a new word
            selected_word = word_grid[row][col]
            selected_cells = [(row, col)]
            is_selecting = True
        else:
            # Continue selecting the word
            if (row, col) not in selected_cells:
                selected_word += word_grid[row][col]
                selected_cells.append((row, col))
                click_sound.play()
                speak(selected_word)
    else:
        # Reset the selection if the click is outside the grid
        selected_word = ""
        selected_cells = []
        is_selecting = False

def check_word():
    global selected_word, selected_cells, found_words_cells, words, score, multiplier, words_found, mistakes_made
    if selected_word in words:
        speak(f"Correct! You found the word {selected_word}")
        words_found += 1
        check_achievements()
        correct_sound.play()
        found_words_cells.append(list(selected_cells))
        found_word_colors.append(WORD_COLORS[(words_found - 1) % len(WORD_COLORS)])
        words.remove(selected_word)
        score += 30 * multiplier  # Use multiplier for scoring
        multiplier += 1  # Increase multiplier for consecutive correct answers
        if not words:
            speak("Level Complete!")
            check_achievements()
            advance_level()
        else:
            display_new_grid = True 
    else:
        mistakes_made += 1
        check_achievements()
        speak("Keep trying")

    score -= penalty  # Penalty for incorrect guesses
    multiplier = 1  # Reset multiplier on incorrect guess
    if score < 0:
        score = 0
    selected_word = ""
    selected_cells = []
    
# Load Background Music
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.set_volume(0.2)

def advance_level():
    global level, words, word_grid, selected_word, selected_cells, found_words_cells, \
        cell_size, game_state, score, completed_levels, max_level, time_remaining, hints_remaining
    
    completed_levels.append(level)
    
    if level == max_level:
        max_level += 1
    
    level += 1
    
    # Select the appropriate word list based on difficulty
    if difficulty == "easy":        
        MAX_WORDS = 10
        word_list_for_level = easy_words
    elif difficulty == "medium":        
        MAX_WORDS = 15
        word_list_for_level = easy_words + medium_words
    else:  # hard        
        MAX_WORDS = 20
        word_list_for_level = easy_words + medium_words + hard_words
    
    if level > len(word_list_for_level) // GRID_SIZE:  # Check if more levels are available
        speak("Congratulations! You've completed all levels!")
        level = 1
        score = 0
        game_state = "MENU"
    else:
        words, word_grid = generate_random_grid_and_words(GRID_SIZE, used_words, difficulty)
        cell_size = (SCREEN_HEIGHT - TOP_MARGIN) // len(word_grid)
        selected_word = ""
        selected_cells = []
        found_words_cells = []
        
        # Initialize the timer and hints based on the difficulty level
        if difficulty == "easy":
            MAX_WORDS = 10
            time_remaining = EASY_TIME_LIMIT
            hints_remaining = EASY_HINTS
        elif difficulty == "medium":
            MAX_WORDS = 15
            time_remaining = MEDIUM_TIME_LIMIT
            hints_remaining = MEDIUM_HINTS
        else:
            MAX_WORDS = 20
            time_remaining = HARD_TIME_LIMIT
            hints_remaining = HARD_HINTS
        
        save_progress()
        speak(f"Congratulations! Now you are moving to level {level}.")
        save_scoreboard()
        display_new_grid = True

def save_progress():
    global level, score, used_words
    data = {
        "level": level,
        "score": score,
        "used_words": used_words
    }
    
def update_timer():
    global time_remaining, game_state
    time_remaining -= 1
    if time_remaining <= 0:
        speak("Time's up!")
        show_replay_dialog()

def show_replay_dialog():
    global game_state
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    result = messagebox.askyesno("Time's Up", "Time's up! Do you want to replay the level?")
    if result:
        replay_level()
    else:
        game_state = "MENU"
        speak("Going back to the menu.")
    root.destroy()

def replay_level():
    global words, word_grid, selected_word, selected_cells, found_words_cells, cell_size, time_remaining, hints_remaining
    words, word_grid = generate_random_grid_and_words(GRID_SIZE, used_words, difficulty)
    cell_size = (SCREEN_HEIGHT - TOP_MARGIN) // len(word_grid)
    selected_word = ""
    selected_cells = []
    found_words_cells = []
    # Initialize the timer based on the difficulty level
    if difficulty == "easy":
        MAX_WORDS = 10
        time_remaining = EASY_TIME_LIMIT
        hints_remaining = EASY_HINTS
    elif difficulty == "medium":
        MAX_WORDS = 15
        time_remaining = MEDIUM_TIME_LIMIT
        hints_remaining = MEDIUM_HINTS
    else:
        MAX_WORDS = 20
        time_remaining = HARD_TIME_LIMIT
        hints_remaining = HARD_HINTS
    speak(f"Replaying level {level}.")
    display_new_grid = True

def create_button(x, y, width, height, text, font, text_color, button_color, hover_color, border_color, border_radius=50):
    button_rect = pygame.Rect(x, y, width, height)
    button_data = {
        "rect": button_rect,
        "text": text,
        "font": font,
        "text_color": text_color,
        "button_color": button_color,
        "hover_color": hover_color,
        "border_color": border_color,
        "border_radius": border_radius
    }
    return button_data

def render_button(screen, button_data):
    button_rect = button_data["rect"]
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, button_data["hover_color"], button_rect, border_radius=button_data["border_radius"])
    else:
        pygame.draw.rect(screen, button_data["button_color"], button_rect, border_radius=button_data["border_radius"])
    pygame.draw.rect(screen, button_data["border_color"], button_rect, 3, border_radius=button_data["border_radius"])
    text_surface = button_data["font"].render(button_data["text"], True, button_data["text_color"])
    screen.blit(text_surface, (
        button_rect.x + (button_rect.width - text_surface.get_width()) // 2,
        button_rect.y + (button_rect.height - text_surface.get_height()) // 2
    ))

def draw_menu():
    TEXT_COLOR = (0, 0, 0)
    BUTTON_COLOR = (70, 130, 180)
    BUTTON_HOVER_COLOR = (200, 200, 200)
    FONT1 = pygame.font.Font(None, 72)
    FONT2 = pygame.font.Font(None, 36)
    screen.blit(BG_IMAGE, (0, 0))  # Draw the background image

    # Draw the title with a white border
    title_text = "Word Search Game"
    title_pos = (screen_width // 2, 50)
    draw_text_with_border(screen, title_text, FONT1, TEXT_COLOR, (255, 255, 255), title_pos)

    # Create buttons
    buttons = [
        create_button(screen_width // 2 - 100, 100, 200, 50, "Play Game", FONT2, TEXT_COLOR, BUTTON_COLOR, BUTTON_HOVER_COLOR, (255, 255, 255), border_radius=50),
        create_button(screen_width // 2 - 100, 170, 200, 50, "Score Board", FONT2, TEXT_COLOR, BUTTON_COLOR, BUTTON_HOVER_COLOR, (255, 255, 255), border_radius=50),
        create_button(screen_width // 2 - 100, 240, 200, 50, "Instructions", FONT2, TEXT_COLOR, BUTTON_COLOR, BUTTON_HOVER_COLOR, (255, 255, 255), border_radius=50),
        create_button(screen_width // 2 - 100, 310, 200, 50, "Levels", FONT2, TEXT_COLOR, BUTTON_COLOR, BUTTON_HOVER_COLOR, (255, 255, 255), border_radius=50),
        create_button(screen_width // 2 - 100, 380, 200, 50, "Achievements", FONT2, TEXT_COLOR, BUTTON_COLOR, BUTTON_HOVER_COLOR, (255, 255, 255), border_radius=50),
        create_button(screen_width // 2 - 100, 450, 200, 50, "Setting", FONT2, TEXT_COLOR, BUTTON_COLOR, BUTTON_HOVER_COLOR, (255, 255, 255), border_radius=50),
        create_button(screen_width // 2 - 100, 520, 200, 50, "Exit", FONT2, TEXT_COLOR, BUTTON_COLOR, BUTTON_HOVER_COLOR, (255, 255, 255), border_radius=50)
    ]

    # Render buttons
    for button in buttons:
        render_button(screen, button)

    return buttons

# Function to save the scoreboard
def save_scoreboard():
    global level, score
    try:
        with open("scoreboard.json", "r") as file:
            scoreboard = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        scoreboard = []

    new_entry = {
        "date": str(datetime.now()),
        "level": level,
        "score": score
    }
    
    # Insert the new entry at the beginning of the list
    scoreboard.insert(0, new_entry)

    with open("scoreboard.json", "w") as file:
        json.dump(scoreboard, file, indent=4)

def load_scoreboard():
    try:
        with open("scoreboard.json", "r") as file:
            scoreboard = json.load(file)
    except (FileNotFoundError, json
    
    .JSONDecodeError):
        scoreboard = []
    return scoreboard

def draw_scoreboard():
    TEXT_COLOR = (0, 0, 0)
    HEADER_COLOR = (255, 223, 186)
    ENTRY_COLOR = (255, 245, 238)
    BUTTON_COLOR = (166, 121, 52)
    BUTTON_HOVER_COLOR = (134, 200, 168)
    BUTTON_BORDER_COLOR = (100, 100, 100)
    BOX_COLOR = (240, 240, 240)
    BOX_BORDER_COLOR = (0, 0, 0)
    FONT1 = pygame.font.Font(None, 72)
    FONT2 = pygame.font.Font(None, 36)  # Font for the scoreboard entries

    # Draw the background image on the main screen
    screen.blit(level_background, (0, 0))

    # Back button settings
    back_button = create_button(10, 15, 80, 40, "Back", FONT2, TEXT_COLOR, BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_BORDER_COLOR, border_radius=50)

    # Draw title with a white border
    title_text = "Scoreboard"
    title_pos = (screen_width // 2, 40)
    draw_text_with_border(screen, title_text, FONT1, TEXT_COLOR, (255, 255, 255), title_pos)

    # Load the scoreboard and sort it in descending order by score
    scoreboard = load_scoreboard()
    scoreboard.sort(key=lambda x: x['score'], reverse=True)

    if not scoreboard:
        # No scores found, display message
        no_scores_text = "No previous scores found"
        no_scores_surface = FONT2.render(no_scores_text, True, TEXT_COLOR)
        no_scores_width = no_scores_surface.get_width()
        no_scores_height = no_scores_surface.get_height()

        # Define the box for the no scores message
        box_width = no_scores_width + 20
        box_height = no_scores_height + 20
        box_x = screen_width // 2 - box_width // 2
        box_y = 160

        pygame.draw.rect(screen, BOX_COLOR, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, BOX_BORDER_COLOR, (box_x, box_y, box_width, box_height), 2)

        # Display the no scores message in the box
        no_scores_pos = (box_x + 10, box_y + 10)
        screen.blit(no_scores_surface, no_scores_pos)
    else:
        # Scores found, display headers and scores
        headers = ["S.No", "Score"]
        header_x_positions = [370, 530]  # X positions for the headers
        y_offset = 100

        # Render headers with background rectangle
        for i, header in enumerate(headers):
            header_surface = FONT2.render(header, True, TEXT_COLOR)
            header_rect = header_surface.get_rect(center=(header_x_positions[i], y_offset))
            pygame.draw.rect(screen, HEADER_COLOR, (header_rect.x - 10, header_rect.y - 5, header_rect.width + 20, header_rect.height + 10))
            screen.blit(header_surface, header_rect)
        
        y_offset += 60  # Move down for the entries

        high_score = 0
        low_score = scoreboard[-1]['score']

        # Render scoreboard entries with background rectangle
        for idx, entry in enumerate(scoreboard, start=1):
            sno_surface = FONT2.render(str(idx), True, TEXT_COLOR)
            score_surface = FONT2.render(str(entry['score']), True, TEXT_COLOR)

            sno_rect = sno_surface.get_rect(center=(header_x_positions[0], y_offset))
            score_rect = score_surface.get_rect(center=(header_x_positions[1], y_offset))

            pygame.draw.rect(screen, ENTRY_COLOR, (sno_rect.x - 10, sno_rect.y - 5, sno_rect.width + 20, sno_rect.height + 10))
            pygame.draw.rect(screen, ENTRY_COLOR, (score_rect.x - 10, score_rect.y - 5, score_rect.width + 20, score_rect.height + 10))

            screen.blit(sno_surface, sno_rect)
            screen.blit(score_surface, score_rect)

            y_offset += 50

            # Update high score
            if entry['score'] > high_score:
                high_score = entry['score']

        # Display high score and low score in a box
        y_offset += 25
        box_width = 250
        box_height = 100
        box_x = screen_width // 2 - 430
        box_y = y_offset + 35

        pygame.draw.rect(screen, BOX_COLOR, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, BOX_BORDER_COLOR, (box_x, box_y, box_width, box_height), 2)

        high_score_text = f"High Score: {high_score}"
        low_score_text = f"Low Score: {low_score}"

        high_score_surface = FONT2.render(high_score_text, True, TEXT_COLOR)
        low_score_surface = FONT2.render(low_score_text, True, TEXT_COLOR)

        high_score_pos = (screen_width // 2 - 400, box_y + 10)
        low_score_pos = (screen_width // 2 - 400, box_y + 50)

        screen.blit(high_score_surface, high_score_pos)
        screen.blit(low_score_surface, low_score_pos)

    render_button(screen, back_button)
    return back_button["rect"]

def draw_instructions():
    TEXT_COLOR = (0, 0, 0)
    BUTTON_COLOR = (166, 121, 52)
    BUTTON_HOVER_COLOR = (134, 200, 168)
    BUTTON_BORDER_COLOR = (100, 100, 100)

    screen.blit(level_background, (0, 0))

    instructions = [
        "Welcome to the Word Search Game!",
        "1. Find and select words from the grid.",
        "2. Click on letters to form words.",
        "3. Complete all words to advance to the next level.",
        "4. Each correct word gives you points.",
        "5. Use hints to find words when stuck.",
        "6. You can save your progress anytime.",
        "7. Use the back button to return to the menu.",
        "Good luck and have fun!"
    ]

    y_offset = 80
    line_height = 40

    # Draw the title
    title_surface = FONT1.render("Instructions", True, TEXT_COLOR)
    screen.blit(title_surface, (screen_width // 2 - title_surface.get_width() // 2, 15))

    # Draw the instructions
    y = y_offset
    for line in instructions:
        text_surface = FONT2.render(line, True, TEXT_COLOR)
        screen.blit(text_surface, (50, y))
        y += line_height

    play_button = create_button(200, SCREEN_HEIGHT - 80, 150, 50, "Play video", FONT2, TEXT_COLOR, BUTTON_COLOR, BUTTON_HOVER_COLOR, (255, 255, 255), border_radius=50)
    render_button(screen, play_button)
    # Back button settings
    back_button = create_button(600, SCREEN_HEIGHT - 80, 150, 50, "Back", FONT, TEXT_COLOR, (166, 121, 52), (134, 200, 168), (255,255,255), border_radius=50)
    render_button(screen, back_button)
    return play_button,back_button

def get_word_list_for_difficulty(difficulty):
    if difficulty == "easy":
        return easy_words, 10, 70, 20
    elif difficulty == "medium":
        return easy_words + medium_words, 15, 60, 15
    else:  # hard
        return easy_words + medium_words + hard_words, 20, 60, 15

def calculate_layout_params(screen_width, screen_height, button_size, spacing):
    cols = (screen_width - 2 * spacing) // (button_size + spacing)
    rows = (screen_height - 150) // (button_size + spacing)
    x_offset = (screen_width - (cols * (button_size + spacing) - spacing)) // 2
    y_offset = 100
    return cols, rows, x_offset, y_offset

def render_level_button(screen, button_rect, lvl, completed_levels, max_level, colors):
    if lvl in completed_levels:
        pygame.draw.rect(screen, colors["completed"], button_rect, border_radius=15)
    elif lvl == max_level:
        pygame.draw.rect(screen, colors["highlight"], button_rect, border_radius=15)
    else:
        pygame.draw.rect(screen, colors["locked"], button_rect, border_radius=15)
    pygame.draw.rect(screen, colors["border"], button_rect, 3, border_radius=15)
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, colors["hover"], button_rect, border_radius=15)
        pygame.draw.rect(screen, colors["hover_border"], button_rect, 3, border_radius=15)

def draw_levels():
    TEXT_COLOR = (0, 0, 0)
    BUTTON_COLOR = (166, 121, 52)
    BUTTON_HOVER_COLOR = (134, 200, 168)
    BUTTON_BORDER_COLOR = (100, 100, 100)
    HOVER_BORDER_COLOR = (0, 0, 0)
    COMPLETED_COLOR = (100, 255, 100)
    HIGHLIGHT_COLOR = (255, 255, 100)
    LOCKED_COLOR = (255, 100, 100)
    GOLDEN_COLOR = (255, 215, 0)

    # Draw the background image on the main screen
    screen.blit(level_background, (0, 0))

    # Back button settings
    back_button_data = create_button(10, 15, 100, 50, "Back", FONT2, TEXT_COLOR, BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_BORDER_COLOR, border_radius=50)

    # Select the appropriate word list based on difficulty
    word_list_for_level, MAX_WORDS, button_size, spacing = get_word_list_for_difficulty(difficulty)

    # Calculate the number of levels
    num_levels = len(word_list_for_level) // GRID_SIZE

    # Calculate the number of columns and rows based on the screen size
    cols, rows, x_offset, y_offset = calculate_layout_params(screen_width, screen_height, button_size, spacing)

    # Draw the title
    levels_title = FONT1.render("Select Level", True, TEXT_COLOR)
    screen.blit(levels_title, (screen_width // 2 - levels_title.get_width() // 2, 20))

    level_buttons = []
    colors = {
        "completed": COMPLETED_COLOR,
        "highlight": HIGHLIGHT_COLOR,
        "locked": LOCKED_COLOR,
        "border": GOLDEN_COLOR,
        "hover": BUTTON_HOVER_COLOR,
        "hover_border": HOVER_BORDER_COLOR,
        "text": TEXT_COLOR
    }

    for lvl in range(1, num_levels + 1):
        col = (lvl - 1) % cols
        row = (lvl - 1) // cols
        x = x_offset + col * (button_size + spacing)
        y = y_offset + row * (button_size + spacing)
        button_rect = pygame.Rect(x, y, button_size, button_size)

        # Draw buttons with different colors based on level status
        render_level_button(screen, button_rect, lvl, completed_levels, max_level, colors)

        # Render level number
        level_text = FONT2.render(str(lvl), True, TEXT_COLOR)
        screen.blit(level_text, (button_rect.x + button_size // 2 - level_text.get_width() // 2, button_rect.y + button_size // 2 - level_text.get_height() // 2))

        level_buttons.append((button_rect, lvl))

    # Render the back button
    render_button(screen, back_button_data)

    return level_buttons, back_button_data["rect"]

def handle_menu_click(mouse_pos):
    global game_state, previous_state
    start_button = pygame.Rect(100, 200, 300, 50)
    score_button = pygame.Rect(100, 300, 300, 50)
    instructions_button = pygame.Rect(100, 400, 300, 50)
    levels_button = pygame.Rect(100, 500, 300, 50)
    achievements_button = pygame.Rect(100, 600, 300, 50)
    setting_button = pygame.Rect(100, 700, 300, 50)

    if start_button.collidepoint(mouse_pos):
        game_state = "GAME"
        previous_state = "MENU"
        speak("Starting the game")
    elif score_button.collidepoint(mouse_pos):
        game_state = "SCOREBOARD"
        previous_state = "MENU"
        draw_scoreboard()
    elif instructions_button.collidepoint(mouse_pos):
        game_state = "INSTRUCTIONS"
        previous_state = "MENU"
        draw_instructions()
    elif levels_button.collidepoint(mouse_pos):
        game_state = "LEVELS"
        previous_state = "MENU"
        draw_levels()
    elif achievements_button.collidepoint(mouse_pos):
        game_state = "ACHIEVEMENTS"
        previous_state = "MENU"
        draw_achievements()
    elif setting_button.collidepoint(mouse_pos):
        game_state = "SETTINGS"
        previous_state = "MENU"
        draw_settings()

def load_achievements():
    global achievements
    default_achievements = {
        "First Word": {"description": "Find your first word.", "unlocked": False},
        "Word Hunter": {"description": "Find 10 words.", "unlocked": False},
        "Hint Master": {"description": "Use 5 hints.", "unlocked": False},
        "Flawless Victory": {"description": "Complete a level without mistakes.", "unlocked": False},
        "Speed Runner": {"description": "Complete a level within half the time limit.", "unlocked": False},
        "Perfectionist": {"description": "Complete 5 levels without making a mistake.", "unlocked": False},
        "Explorer": {"description": "Find all words in a level.", "unlocked": False},
        "Night Owl": {"description": "Play the game between midnight and 6 AM.", "unlocked": False},
        "Early Bird": {"description": "Play the game between 6 AM and noon.", "unlocked": False},
        "Speed Demon": {"description": "Complete 3 levels in a row within half the time limit.", "unlocked": False},
        "Novice": {"description": "Find 50 words.", "unlocked": False},
        "Intermediate": {"description": "Find 100 words.", "unlocked": False},
        "Expert": {"description": "Find 200 words.", "unlocked": False},
        "Word Master": {"description": "Find 500 words.", "unlocked": False},
        "Ultimate Hunter": {"description": "Find 1000 words.", "unlocked": False},
        "No Help Needed": {"description": "Complete 5 levels without using any hints.", "unlocked": False},
        "Hint Novice": {"description": "Use your first hint.", "unlocked": False},
        "Mistake Avoider": {"description": "Complete a level with fewer than 3 mistakes.", "unlocked": False},
        "Unstoppable": {"description": "Complete 10 levels in a row without failing.", "unlocked": False},
        "Strategist": {"description": "Complete a level with more than 5 minutes remaining.", "unlocked": False},
        "Comeback King": {"description": "Win a level with less than 1 minute remaining.", "unlocked": False},
        "Consistent Player": {"description": "Play the game for 7 consecutive days.", "unlocked": False},
        "Marathon Player": {"description": "Play the game for 30 consecutive days.", "unlocked": False},
        "Puzzle Enthusiast": {"description": "Complete 20 levels.", "unlocked": False},
        "Puzzle Expert": {"description": "Complete 50 levels.", "unlocked": False},
        "Puzzle Master": {"description": "Complete 100 levels.", "unlocked": False},
        "Speed Challenger": {"description": "Complete 5 levels within the time limit.", "unlocked": False}
    }

    try:
        with open("achievements.json", "r") as file:
            data = json.load(file)
            # Ensure the loaded data has the correct structure
            if "achievements" in data:
                achievements = data["achievements"]
            else:
                achievements = default_achievements
    except (FileNotFoundError, json.JSONDecodeError):
        achievements = default_achievements


def save_achievements():
    try:
        # Check if the file is writable or the directory is accessible
        if not os.access(".", os.W_OK):
            print("Error: Current directory is not writable.")
            return
        
        # Open the file and wite the data
        with open("achievements.json", "w") as file:
            json.dump(achievements, file, indent=4)
        print("Achievements saved successfully.")
    
    except OSError as e:
        print(f"Failed to save achievements due to an OS error: {e}")
    
    except json.JSONDecodeError as e:
        print(f"Failed to save achievements due to JSON error: {e}")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def check_achievements():
    global achievements, time_limit
    updated = False
    if difficulty == "easy":
        time_limit = EASY_TIME_LIMIT
    elif difficulty == "medium":
        time_limit = MEDIUM_TIME_LIMIT
    elif difficulty == "hard":
        time_limit = HARD_TIME_LIMIT
    else:
        time_limit = 0
    if not achievements["First Word"]["unlocked"] and words_found >= 1:
        print("Unlocking 'First Word' achievement")
        achievements["First Word"]["unlocked"] = True
        updated = True
    if not achievements["Word Hunter"]["unlocked"] and words_found >= 10:
        achievements["Word Hunter"]["unlocked"] = True
        updated = True
    if not achievements["Hint Master"]["unlocked"] and hints_used >= 5:
        achievements["Hint Master"]["unlocked"] = True
        updated = True
    if not achievements["Flawless Victory"]["unlocked"] and mistakes_made == 0 and level_completed:
        achievements["Flawless Victory"]["unlocked"] = True
        updated = True
    if not achievements["Perfectionist"]["unlocked"] and levels_completed_flawlessly >= 5:
        achievements["Perfectionist"]["unlocked"] = True
        updated = True
    if not achievements["Explorer"]["unlocked"] and all_words_found:
        achievements["Explorer"]["unlocked"] = True
        updated = True
    if not achievements["Speed Demon"]["unlocked"] and levels_completed_speedily >= 3:
        achievements["Speed Demon"]["unlocked"] = True
        updated = True
    if not achievements["Novice"]["unlocked"] and words_found >= 50:
        achievements["Novice"]["unlocked"] = True
        updated = True
    if not achievements["Intermediate"]["unlocked"] and words_found >= 100:
        achievements["Intermediate"]["unlocked"] = True
        updated = True
    if not achievements["Expert"]["unlocked"] and words_found >= 200:
        achievements["Expert"]["unlocked"] = True
        updated = True
    if not achievements["Word Master"]["unlocked"] and words_found >= 500:
        achievements["Word Master"]["unlocked"] = True
        updated = True
    if not achievements["Ultimate Hunter"]["unlocked"] and words_found >= 1000:
        achievements["Ultimate Hunter"]["unlocked"] = True
        updated = True
    if not achievements["No Help Needed"]["unlocked"] and levels_completed_without_hints >= 5:
        achievements["No Help Needed"]["unlocked"] = True
        updated = True
    if not achievements["Hint Novice"]["unlocked"] and hints_used >= 1:
        achievements["Hint Novice"]["unlocked"] = True
        updated = True
    if not achievements["Mistake Avoider"]["unlocked"] and mistakes_made < 3 and level_completed:
        achievements["Mistake Avoider"]["unlocked"] = True
        updated = True
    if not achievements["Unstoppable"]["unlocked"] and levels_completed_consecutively >= 10:
        achievements["Unstoppable"]["unlocked"] = True
        updated = True
    if not achievements["Strategist"]["unlocked"] and time_remaining > 300:
        achievements["Strategist"]["unlocked"] = True
        updated = True
    if not achievements["Comeback King"]["unlocked"] and time_remaining < 60 and level_completed:
        achievements["Comeback King"]["unlocked"] = True
        updated = True
    if not achievements["Puzzle Enthusiast"]["unlocked"] and levels_completed >= 20:
        achievements["Puzzle Enthusiast"]["unlocked"] = True
        updated = True
    if not achievements["Puzzle Expert"]["unlocked"] and levels_completed >= 50:
        achievements["Puzzle Expert"]["unlocked"] = True
        updated = True
    if not achievements["Puzzle Master"]["unlocked"] and levels_completed >= 100:
        achievements["Puzzle Master"]["unlocked"] = True
        updated = True
    if not achievements["Speed Challenger"]["unlocked"] and levels_completed_speedily >= 5:
        achievements["Speed Challenger"]["unlocked"] = True
        updated = True

    if updated:
        save_achievements()

def draw_achievements():
    global achievements, scroll_offset  # Ensure achievements is global
    TEXT_COLOR = (0, 0, 0)
    BUTTON_COLOR = (166, 121, 52)
    BUTTON_HOVER_COLOR = (134, 200, 168)
    BUTTON_BORDER_COLOR = (100, 100, 100)
    FONT1 = pygame.font.Font(None, 48)
    FONT2 = pygame.font.Font(None, 36)
    FONT3 = pygame.font.Font(None, 30)

    # Back button settings
    back_button_data = create_button(10, 15, 80, 35, "Back", FONT2, TEXT_COLOR, BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_BORDER_COLOR, border_radius=50)

    # Draw the background image on the main screen
    screen.blit(level_background, (0, 0))
    # Draw the title with a white border
    title_text = "Achievements"
    title_pos = (screen_width // 2, 30)
    draw_text_with_border(screen, title_text, FONT1, TEXT_COLOR, (255, 255, 255), title_pos)

    # Define the top margin height
    top_margin_height = 70

    # Define initial y offset and calculate the scrollable area height
    initial_y_offset = 5
    line_height = 40
    achievements_height = initial_y_offset + len(achievements) * line_height

    # Create a surface for the achievements
    scroll_surface = pygame.Surface((screen_width, achievements_height), pygame.SRCALPHA)

    # Draw the achievements on the scrollable surface
    y = initial_y_offset
    for i, (achievement_key, achievement_value) in enumerate(achievements.items(), start=1):
        achievement_label = FONT3.render(f"{i}. {achievement_key}: {achievement_value['description']} - {'Unlocked' if achievement_value['unlocked'] else 'Locked'}", True, TEXT_COLOR)
        scroll_surface.blit(achievement_label, (40, y))
        y += FONT3.get_height() + 10

    # Adjust scroll_offset to ensure the last achievement is close to the bottom
    if achievements_height > screen_height - top_margin_height:
        # Calculate the scroll offset needed to bring the last achievement close to the bottom
        max_scroll_offset = achievements_height - (screen_height - top_margin_height)
        scroll_offset = max(0, min(scroll_offset, max_scroll_offset))
    else:
        scroll_offset = 0  # No need to scroll if achievements fit within the visible area

    # Clip the area below the top margin
    screen.set_clip(pygame.Rect(0, top_margin_height, screen_width, screen_height - top_margin_height))

    # Blit the scrollable surface to the screen at the current scroll position
    screen.blit(scroll_surface, (0, top_margin_height - scroll_offset))

    # Reset the clipping area
    screen.set_clip(None)

    # Draw the scrollbar
    scrollbar_width = 20
    scrollbar_rect = pygame.Rect(screen_width - scrollbar_width, top_margin_height, scrollbar_width, screen_height - top_margin_height)
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, scrollbar_rect)
    scrollbar_handle_height = max(20, (screen_height - top_margin_height) * ((screen_height - top_margin_height) / achievements_height))  # Minimum height for handle
    scrollbar_handle_rect = pygame.Rect(screen_width - scrollbar_width, top_margin_height + (scroll_offset * ((screen_height - top_margin_height) / achievements_height)), scrollbar_width, scrollbar_handle_height)
    pygame.draw.rect(screen, BUTTON_COLOR, scrollbar_handle_rect)

    # Render the back button
    render_button(screen, back_button_data)
    return back_button_data['rect'], achievements_height
        
def save_game():
    global level, words, word_grid, score, completed_levels, max_level, time_remaining,\
        achievements, high_score
    game_data = {
        "level": level,
        "completed_levels": completed_levels,
        "words": words,
        "word_grid": word_grid,
        "found_words_cells": found_words_cells,
        "time_remaining": time_remaining,
        "max_level": max_level,
        "achievements": achievements,
        "high_score": high_score
    }
    with open("savegame.json", "w") as file:
        json.dump(game_data, file)
    speak("Game saved successfully.")

def load_game():
    global level, words, word_grid, score, completed_levels, max_level, time_remaining,\
        achievements, high_score, selected_word, selected_cells, found_words_cells
    try:
        with open("savegame.json", "r") as file:
            game_data = json.load(file)
            level = game_data.get("level", 1)
            score = game_data.get("score", 0)
            completed_levels = game_data.get("completed_levels", [])
            words = game_data.get("words", [])
            word_grid = game_data.get("word_grid", [])
            found_words_cells = game_data.get("found_words_cells", [])
            time_remaining = game_data.get("time_remaining", 0)
            max_level = game_data.get("max_level", 1)
            achievements = game_data.get("achievements", [])
            high_score = game_data.get("high_score", 0)
            selected_word = ""
            selected_cells = []
            found_words_cells = []
    except FileNotFoundError:
        print("No saved game found.")
    except json.JSONDecodeError:
        print("No saved game data found.")

# Icons (placeholders)
volume_icon = pygame.Surface((40, 40))
volume_icon.fill((255, 255, 255))
music_icon = pygame.Surface((40, 40))
music_icon.fill((255, 255, 255))
difficulty_icon = pygame.Surface((40, 40))
difficulty_icon.fill((255, 255, 255))
theme_icon = pygame.Surface((40, 40))
theme_icon.fill((255, 255, 255))

def draw_rounded_rect(surface, color, rect, radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_shadowed_text(surface, text, font, color, pos, shadow_color, offset=SHADOW_OFFSET):
    shadow_surface = font.render(text, True, shadow_color)
    shadow_rect = shadow_surface.get_rect(center=(pos[0] + offset, pos[1] + offset))
    surface.blit(shadow_surface, shadow_rect)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)
    surface.blit(text_surface, text_rect)
    
theme_light = True

def draw_settings():
    # Use global variables
    global TEXT_COLOR, BUTTON_COLOR, BUTTON_BORDER_COLOR, BUTTON_HOVER_COLOR, BG_COLOR
    
    # Draw the background image on the main screen
    screen.blit(level_background, (0, 0))

    # Settings title
    title_surface = FONT1.render("Settings", True, TEXT_COLOR)
    screen.blit(title_surface, (screen_width // 2 - title_surface.get_width() // 2, 30))

    # Sound Volume Control
    volume_label = FONT.render("Sound Volume", True, TEXT_COLOR)
    volume_rect = volume_label.get_rect(center=(screen_width // 2 - 150, 150))
    screen.blit(volume_label, volume_rect)
    
    # Minus Button
    minus_button = pygame.Rect(screen_width // 2 + 25, 135, 40, 40)
    if minus_button.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, minus_button, border_radius=10)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, minus_button, border_radius=10)
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, minus_button, width=4, border_radius=10)
    minus_text = FONT.render("-", True, TEXT_COLOR)
    minus_text_rect = minus_text.get_rect(center=minus_button.center)
    screen.blit(minus_text, minus_text_rect)

    # Volume Value Display
    volume_value = FONT.render(f"{int(sound_volume * 100)}%", True, TEXT_COLOR) 
    volume_value_rect = volume_value.get_rect(center=(screen_width // 2 + 100, 155))
    screen.blit(volume_value, volume_value_rect)

    # Plus Button
    plus_button = pygame.Rect(screen_width // 2 + 140, 135, 40, 40)
    if plus_button.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, plus_button, border_radius=10)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, plus_button, border_radius=10)
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, plus_button, width=2, border_radius=10)
    plus_text = FONT.render("+", True, TEXT_COLOR)
    plus_text_rect = plus_text.get_rect(center=plus_button.center)
    screen.blit(plus_text, plus_text_rect)

    # Music Toggle
    music_label = FONT.render("Background Music", True, TEXT_COLOR)
    music_rect = music_label.get_rect(center=(screen_width // 2 - 150, 250))
    screen.blit(music_label, music_rect)
    music_button = pygame.Rect(screen_width // 2 + 50, 235, 100, 40)
    if music_button.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, music_button, border_radius=10)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, music_button, border_radius=10)
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, music_button, width=2, border_radius=10)
    music_value = FONT.render("On" if music_on else "Off", True, TEXT_COLOR)
    music_value_rect = music_value.get_rect(center=music_button.center)
    screen.blit(music_value, music_value_rect)

    # Difficulty Selection
    difficulty_label = FONT.render("Difficulty", True, TEXT_COLOR)
    difficulty_rect = difficulty_label.get_rect(center=(screen_width // 2 - 150, 350))
    screen.blit(difficulty_label, difficulty_rect)
    difficulty_button = pygame.Rect(screen_width // 2 + 50, 335, 100, 40)
    if difficulty_button.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, difficulty_button, border_radius=10)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, difficulty_button, border_radius=10)
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, difficulty_button, width=2, border_radius=10)
    
    # Correctly display the difficulty value
    if difficulty == "easy":
        MAX_WORDS = 10
        difficulty_value = FONT.render("Easy", True, TEXT_COLOR)
    elif difficulty == "medium":
        MAX_WORDS = 15
        difficulty_value = FONT.render("Medium", True, TEXT_COLOR)
    else:
        MAX_WORDS = 20
        difficulty_value = FONT.render("Hard", True, TEXT_COLOR)
    
    difficulty_value_rect = difficulty_value.get_rect(center=difficulty_button.center)
    screen.blit(difficulty_value, difficulty_value_rect)

    # Theme Change
    theme_label = FONT.render("Change Theme", True, TEXT_COLOR)
    theme_rect = theme_label.get_rect(center=(screen_width // 2 - 150, 450))
    screen.blit(theme_label, theme_rect)
    theme_button = pygame.Rect(screen_width // 2 + 50, 435, 100, 40)
    if theme_button.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, theme_button, border_radius=10)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, theme_button, border_radius=10)
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, theme_button, width=2, border_radius=10)
    theme_value = FONT.render("Light" if theme_light else "Dark", True, TEXT_COLOR)
    theme_value_rect = theme_value.get_rect(center=theme_button.center)
    screen.blit(theme_value, theme_value_rect)

    # Back Button
    back_button = pygame.Rect(50, 30, 100, 40)
    if back_button.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, back_button, border_radius=20)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, back_button, border_radius=20)
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, back_button, width=2, border_radius=20)
    back_text =  FONT.render("Back", True, TEXT_COLOR)
    screen.blit(back_text, (
        back_button.x + (back_button.width - back_text.get_width()) // 2,
        back_button.y + (back_button.height - back_text.get_height()) // 2
    ))

    pygame.display.flip()   
    return back_button, minus_button, plus_button, music_button, difficulty_button, theme_button

music_button_rect =  pygame.Rect(100, 100,200,50)

# Example button drawing function
def draw_music_button():
    if music_on:
        music_text = FONT.render("Music: On", True, TEXT_COLOR)
    else:
        music_text = FONT.render("Music: Off", True, TEXT_COLOR)
    screen.blit(music_text, (100, 100))

# Example button rectangles (you should replace these with your actual button positions and sizes)
volume_button = pygame.Rect(100, 100, 50, 50)
music_button = pygame.Rect(200, 100, 50, 50)
difficulty_button = pygame.Rect(300, 100, 50, 50)
theme_button = pygame.Rect(400, 100, 50, 50)

clock = pygame.time.Clock()
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 1000)  # 1 second timer for updating time

# Constants for scrolling
SCROLL_SPEED = 10
scroll_offset = 0
max_scroll_offset = 0

def main():
    global game_state, previous_state, mouse_down, selected_word, \
        selected_cells, found_words_cells, score, level, completed_levels, \
        max_level, time_remaining, sound_volume, music_on, time_limit, \
        BG_COLOR, GRID_COLOR, TEXT_COLOR, FONT_SIZE, FONT, difficulty, hint_button,\
        hint_cooldown_remaining, hints_remaining, theme_light, word_list_for_level, achievements,\
        scroll_surface_height, scroll_offset, SCROLL_SPEED, max_scroll_offset, cell_size, words, mistakes_made, hints_used,play_button
    
    mistakes_made = 0
    hints_used = 0
    # Initialize the game state and settings
    load_game()
    load_achievements()
    # Define a variable for smooth scrolling increment
    scroll_increment = 0
    pygame.mixer.music.play(-1)  # Play music indefinitely (-1 means loop)
    # Initialize Pygame and the main loop
    back_button, save_button, scroll_surface_height = None, None, None
    clock = pygame.time.Clock()
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)
    screen.fill(BG_COLOR)
    running = True
    display_new_grid = False

    show_intro()

    while running:
        if game_state == "MENU":
            buttons = draw_menu()
        elif game_state == "SCOREBOARD":
            back_button = draw_scoreboard()
        elif game_state == "INSTRUCTIONS":
            play_button, back_button = draw_instructions()
        elif game_state == "LEVELS":
            level_buttons, back_button = draw_levels()
        elif game_state == "ACHIEVEMENTS":
            back_button, scroll_surface_height = draw_achievements()
            max_scroll_offset = max(0, scroll_surface_height - screen_height - 50)
        elif game_state == "SETTINGS":
            back_button, minus_button, plus_button, music_button, difficulty_button, theme_button = draw_settings()
        elif game_state == "GAME":
            back_button, save_button, hint_button = draw_grid()
            if display_new_grid:
                pygame.display.flip()
                display_new_grid = False
            timer_surface = FONT.render(f"Time: {time_remaining}", True, TEXT_COLOR)
            screen.blit(timer_surface, (SCREEN_WIDTH - 25, TOP_MARGIN - 40))
            score_surface = FONT.render(f"Score: {score}", True, TEXT_COLOR)
            screen.blit(score_surface, (SCREEN_WIDTH + 150, TOP_MARGIN - 40))

        pygame.display.flip()

        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "MENU":
                    for button in buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            if button["text"] == "Play Game":
                                previous_state = "MENU"
                                game_state = "GAME"
                                selected_word = ""
                                selected_cells = []
                                found_words_cells = []
                                score = 0
                                speak("Game started")
                                display_new_grid = True

                                # Initialize the timer based on the difficulty level
                                if difficulty == "easy":
                                    MAX_WORDS = 10
                                    time_remaining = EASY_TIME_LIMIT
                                    hints_remaining = EASY_HINTS
                                elif difficulty == "medium":
                                    MAX_WORDS = 15
                                    time_remaining = MEDIUM_TIME_LIMIT
                                    hints_remaining = MEDIUM_HINTS
                                else:
                                    MAX_WORDS = 20
                                    time_remaining = HARD_TIME_LIMIT
                                    hints_remaining = HARD_HINTS
                            elif button["text"] == "Score Board":
                                game_state = "SCOREBOARD"
                                speak("Scoreboard")                                
                            elif button["text"] == "Instructions":
                                game_state = "INSTRUCTIONS"
                                speak("Here are the instructions.")
                            elif button["text"] == "Levels":
                                game_state = "LEVELS"
                                speak("Select a level.")
                            elif button["text"] == "Achievements":
                                game_state = "ACHIEVEMENTS"
                                speak("Achievements.")
                            elif button["text"] == "Setting":
                                game_state = "SETTINGS"
                                speak("Settings.")
                            elif button["text"] == "Exit":
                                # Handle Exit button click
                                running = False    
                elif game_state == "SCOREBOARD":
                    if back_button.collidepoint(mouse_pos):
                        game_state = "MENU"
                        speak("Going back to the menu")
                elif game_state == "INSTRUCTIONS":
                    if play_button["rect"].collidepoint(mouse_pos):
                        speak("Playing video")
                        #play_video(video)
                    if back_button["rect"].collidepoint(mouse_pos):
                        game_state = "MENU"
                        speak("Going back to the menu")
                elif game_state == "LEVELS":
                    if back_button.collidepoint(event.pos):
                        game_state = "MENU"
                        speak("Going back to the menu")
                    else:
                        for button_rect, lvl in level_buttons:
                            if button_rect.collidepoint(event.pos):
                                if lvl > max_level:
                                    print("Cannot start this level because it is locked.")
                                    speak("This level is locked.")
                                else:
                                    previous_state = "LEVELS"
                                    level = lvl
                                    game_state = "GAME"
                                    words, word_grid = generate_random_grid_and_words(GRID_SIZE, used_words, difficulty)
                                    cell_size = (SCREEN_HEIGHT - TOP_MARGIN) // len(word_grid)
                                    selected_word = ""
                                    selected_cells = []
                                    found_words_cells = []

                                    # Initialize the timer based on the difficulty level
                                    if difficulty == "easy":
                                        MAX_WORDS = 10
                                        word_list_for_level = easy_words
                                        time_remaining = EASY_TIME_LIMIT
                                    elif difficulty == "medium":
                                        MAX_WORDS = 15
                                        word_list_for_level = medium_words
                                        time_remaining = MEDIUM_TIME_LIMIT
                                    else:
                                        MAX_WORDS = 20
                                        word_list_for_level = hard_words
                                        time_remaining = HARD_TIME_LIMIT

                                    score = 0
                                    display_new_grid = True
                                    speak(f"Level {level} started.")
                elif game_state == "ACHIEVEMENTS":
                    if back_button.collidepoint(mouse_pos):
                        game_state = "MENU"
                        speak("Going back to the menu")
                elif game_state == "SETTINGS":
                    if back_button.collidepoint(mouse_pos):
                        game_state = "MENU"
                        speak("Going back to the menu")
                    elif minus_button.collidepoint(mouse_pos):
                        if sound_volume > 0:
                            sound_volume -= 0.1
                            speak("Volume down")
                    elif plus_button.collidepoint(mouse_pos):
                        if sound_volume < 1:
                            sound_volume += 0.1
                            speak("Volume up")
                    elif music_button.collidepoint(mouse_pos):
                        music_on = not music_on
                        if music_on:
                            pygame.mixer.music.play(-1)
                        else:
                            pygame.mixer.music.stop()
                        speak("Music toggled")
                    elif difficulty_button.collidepoint(mouse_pos):
                        if difficulty == "easy":
                            difficulty = "medium"
                            speak("Difficulty set to medium")
                        elif difficulty == "medium":
                            difficulty = "hard"
                            speak("Difficulty set to hard")
                        else:
                            difficulty = "easy"
                            speak("Difficulty set to easy")
                    elif theme_button.collidepoint(mouse_pos):
                        if theme_light:
                            theme_light = False
                            BG_COLOR = (0, 0, 0)
                            GRID_COLOR = (255, 255, 255)
                            TEXT_COLOR = (255, 255, 255)
                            speak("Theme set to dark")
                        else:
                            theme_light = True
                            BG_COLOR = (255, 255, 255)
                            GRID_COLOR = (0, 0, 0)
                            TEXT_COLOR = (0, 0, 0)
                            speak("Theme set to light")
                elif game_state == "GAME":
                    back_button, save_button, hint_button = draw_grid()
                    mouse_down = True
                    selected_word = ""
                    selected_cells = []
                    if back_button.collidepoint(event.pos):
                        game_state = previous_state
                        if game_state == "MENU":
                            speak("Going back to the menu")
                        else:
                            speak("Going back to the level selection")
                    elif save_button.collidepoint(event.pos):
                        save_game()
                        speak("Game saved")
                    elif hint_button.collidepoint(event.pos):
                        if hint_cooldown_remaining == 0 and hints_remaining > 0:
                            provide_hint()
                            hint_cooldown_remaining = HINT_COOLDOWN_DURATION
                            hints_remaining -= 1
                            speak(f"Hint given. {hints_remaining} hints remaining.")
                        else:
                            speak("No hints available or cooldown active.")
                    else:
                        handle_click(event.pos)
                elif game_state == "LEVELS":
                    if back_button.collidepoint(event.pos):
                        game_state = "MENU"
                        speak("Going back to the menu")
                    else:
                        for button_rect, lvl in level_buttons:
                            if button_rect.collidepoint(event.pos):
                                if lvl > max_level:
                                    print("Cannot start this level because it is locked.")
                                    speak("This level is locked.")
                                else:
                                    previous_state = "LEVELS"
                                    level = lvl
                                    game_state = "GAME"
                                    words, word_grid = generate_random_grid_and_words(GRID_SIZE, used_words, difficulty)
                                    cell_size = (SCREEN_HEIGHT - TOP_MARGIN) // len(word_grid)
                                    selected_word = ""
                                    selected_cells = []
                                    found_words_cells = []

                                    # Initialize the timer based on the difficulty level
                                    if difficulty == "easy":
                                        MAX_WORDS = 10
                                        word_list_for_level = easy_words
                                        time_remaining = EASY_TIME_LIMIT
                                    elif difficulty == "medium":
                                        MAX_WORDS = 15
                                        word_list_for_level = medium_words
                                        time_remaining = MEDIUM_TIME_LIMIT
                                    else:
                                        MAX_WORDS = 20
                                        word_list_for_level = hard_words
                                        time_remaining = HARD_TIME_LIMIT

                                    score = 0
                                    display_new_grid = True
                                    speak(f"Level {level} started.")
            elif event.type == pygame.MOUSEBUTTONUP and game_state == "GAME":
                mouse_down = False
                check_word()
            elif event.type == pygame.MOUSEMOTION and game_state == "GAME" and mouse_down:
                handle_click(event.pos)
            elif event.type == pygame.KEYDOWN and game_state == "GAME":
                if event.key == pygame.K_RETURN:
                    check_word()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif game_state == "GAME" and event.key == pygame.K_SPACE:
                    provide_hint()
                elif game_state == "ACHIEVEMENTS":
                    if event.key == pygame.K_DOWN:
                        scroll_increment = SCROLL_SPEED
                    elif event.key == pygame.K_UP:
                        scroll_increment = -SCROLL_SPEED
            elif event.type == pygame.KEYUP:
                if game_state == "ACHIEVEMENTS":
                    if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                        scroll_increment = 0
            elif event.type == timer_event and game_state == "GAME":
                if game_state == "GAME":
                    time_remaining -= 1
                    if time_remaining <= 0:
                        time_remaining = 0
                        speak("Time's up!")
                        show_replay_dialog()
                    
        if game_state == "ACHIEVEMENTS":
            # Apply smooth scrolling
            scroll_offset = max(0, min(max_scroll_offset, scroll_offset + scroll_increment))
        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()  # Stop music when game ends
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()