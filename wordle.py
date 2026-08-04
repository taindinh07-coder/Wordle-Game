
# Imports
import random
from english_words import get_english_words_set
import pygame
import sys



# Screen Setup
pygame.init()

# Setup
web2_words = get_english_words_set(['web2'], lower=True)
word_list = [word for word in web2_words if len(word) == 5]
password = random.choice(word_list)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(title='Wordle')
# Set up Tiles and Grid
TILE_SIZE = 60
TILE_GAP = 8

GRID_X = (SCREEN_WIDTH - (5 * TILE_SIZE + 4 * TILE_GAP))//2 
GRID_Y = 80
# Text Font
FONT_SIZE = 40
font = pygame.font.Font(None, FONT_SIZE)
# Create color variables
white = (255,255,255)
gray = (211,211,211)
green = (144,238,144)
yellow = (255,255,197)

# Game State
current_row = 0
current_guess = ''
guesses = []
feedback = []
game_over = False

# Main Loop
clock = pygame.time.Clock()
running = True
while running:

    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_BACKSPACE:
                current_guess = current_guess[:-1]
        # submit answer logic
            elif event.key == pygame.K_RETURN and len(current_guess) == 5:
            # Compare guess to word
                result = []
                for i in range(5):
                    if current_guess[i] == password[i]:
                        result.append(green)
                    elif current_guess[i] in password:
                        result.append(yellow)
                    else:
                        result.append(gray)
                # Store guess and feedback
                guesses.append(current_guess)
                feedback.append(result)    
            # Check for win
                if current_guess == password:
                    game_over = True
                # Move to next row
                current_row += 1
                current_guess = ''
                # Check for loss
                if current_row == 6 and not game_over:
                    game_over = True
            elif len(current_guess) < 5 and event.unicode.isalpha():
                current_guess += event.unicode.lower()
            # Restart function
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                password = random.choice(word_list)
                current_row = 0
                current_guess = ''
                guesses = []
                feedback = []
                game_over = False

# Draw Empty Grid
    screen.fill(white)

    for row in range(6):
        for col in range(5):
            x = GRID_X + col * (TILE_SIZE + TILE_GAP)
            y = GRID_Y + row * (TILE_SIZE + TILE_GAP)
            pygame.draw.rect(screen, gray, (x, y, TILE_SIZE, TILE_SIZE))

            # Submitted row with colors
            if row < len(guesses):
                pygame.draw.rect(screen, feedback[row][col], (x, y, TILE_SIZE, TILE_SIZE))
                letter = font.render(guesses[row][col].upper(), True, (0,0,0))
                screen.blit(letter, (x + 15, y + 10))

            # Draw current row typing
            elif row == current_row and col < len(current_guess):
                letter = font.render(current_guess[col].upper(), True, (0,0,0))
                screen.blit(letter, (x + 15, y + 10))

    # Win/Loss
    if game_over:
        if password in guesses:
            message = font.render('You win!', True, (0,128,0))
        else:
            message = font.render(f'The word was {password.upper()}', True, (200,0,0))
        screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width()//2 , GRID_Y -60))

        # Restart hint
        hint = font.render('Press R to play again', True, (100,100,100))
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width()//2, SCREEN_HEIGHT-60))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
