import pygame
import random as r
import json
import sys
import math as m
from enum import Enum


# data handling
def tree_path(n: int) -> str:
    return "trees/" + str(n) + "_word_search_tree.json"

def get_tree(n: int) -> []:
    with open(tree_path(n), 'r') as json_file:
        data = json.load(json_file)
    return data

def list_path(n: int) -> str:
    return "lists/all_" + str(n) + "_words.txt"

def add_to_history(n: int):
    if n < 1 or n > 11:
        return

    with open("stats.json", "r") as json_file:
        history_file = json.load(json_file)
    
    if n == 11:
        history_file["x"] += 1
    else:
        history_file[str(n)] += 1
    
    with open("stats.json", "w") as json_file:
        json.dump(history_file, json_file, indent=4)


# variables
all_guesses = []
all_letter_colors = []
word_combo = []
chosen_word = ""
current_guess = ""

all_letters = "abcdefghijklmnopqrstuvwxyz"
game_note = ""

# style options
spacing = 18
grid_size = 20

# version
version = "1.0.0"


# word controls
def get_word(length: int) -> str:
    word_list = open(list_path(length)).readlines()
    choice = word_list[r.randint(0, len(word_list) - 1)].replace('\n', '')
    return choice

def pick_word_combo(length: int, low: int) -> []:
    choice = r.randint(low, length - low)
    return [choice, length - choice]

def pick_word(combo: []) -> str:
    return get_word(combo[0]) + get_word(combo[1])

# notes
def note(text: str):
    global game_note
    game_note = text
    print(game_note)

# game drawing options
def draw_game_screen(screen):
    # get current guess
    possibilities = all_possibilities(current_guess)

    # print lines
    for i in range(10):
        # add possibilities to screen if applicable
        if len(possibilities) >= 19 - 2 * i:
            draw_text_row(str(possibilities[19 - 2 * i - 1]), screen, i, 1)
        
        if len(possibilities) >= 20 - 2 * i:
            draw_text_row(str(possibilities[20 - 2 * i - 1]), screen, i, 2)
        
        # skip to next if no guess
        if not len(all_guesses) > i:
            continue
        
        # else print guess
        colors = get_guess_colors(all_guesses[i])
        draw_text_row(all_guesses[i], screen, i, 0, colors)

    # draw remaining letters
    draw_text_row(all_letters, screen, 11, 0, all_letter_colors)

    # current guess
    draw_text_row(current_guess, screen, 12, 0)

    # draw text pointer
    pygame.draw.rect(screen, BLACK, (grid_size * len(current_guess) , grid_size * 13, grid_size, 5))

    # draw note
    draw_text_row(game_note, screen, 13.25, 0)

def get_guess_colors(guess: str) -> []:
    global chosen_word
    
    # initialize colors for "# "
    colors = [WHITE] * 12

    if int(guess[0]) == word_combo[0]:
        colors[0] = GREEN
    elif int(guess[0]) == word_combo[1]:
        colors[0] = YELLOW

    # gets remaining letters from list not green
    remaining_letters = []

    # find greens
    for i in range(10):
        # get letter
        letter = guess[i + 2]
        
        # if word matches
        if letter == chosen_word[i]:
            colors[i + 2] = GREEN
            continue

        # else add to remaining letters
        remaining_letters.append(chosen_word[i])
    
    # find yellows
    for i in range(10):
        # skip if guess letter is not white
        if colors[i + 2] != WHITE:
            continue
        
        # skip if no remaining letters
        if len(remaining_letters) < 1:
            continue

        # else get letter
        letter = guess[i + 2]
        
        # skip if not in remaining letters
        if not letter in remaining_letters:
            continue

        # see if letter is remaining
        for l in range(len(remaining_letters)):
            # see if letter matches somewhere in chosen word
            if letter == remaining_letters[l]:
                colors[i + 2] = YELLOW
                remaining_letters.pop(l)
                break
    
    # all others are already greyed out
    return colors

def all_possibilities(current_guess: str) -> [str]:
    # get input line
    input_line = current_guess.strip()
    inputs = input_line.split(" ")

    # check if first is 1 character long
    try:
        current_length = int(inputs[0])
    except:
        return ["NO NUMBER"]
    
    if not len(inputs[0]) == 1:
        return ["NUMBER TOO LONG"]

    # check there's more than a number
    if len(inputs) == 1:
        current_guess = ""
    # if more than 2 inputs use 2nd guess
    elif len(inputs) > 2:
        current_guess = inputs[2].strip().lower()
        current_length = 10 - current_length
    else:
        current_guess = inputs[1].strip().lower()

    return get_valid_guesses(current_guess, current_length)

def get_valid_guesses(guess: str, length: int) -> [str]:
    if length < 2:
        return ["LENGTH TOO SHORT"]
    
    if length > 8:
        return ["LENGTH TOO LONG"]
    
    if len(guess) > length:
        return ["GUESS TOO LONG"]

    # get data from tree
    branch = get_tree(length)

    for i in range(len(guess)):
        # branch 0 always says # of guesses remaining on the branch
        branch_sub = branch[1]

        # if branch_sub is a list break
        if isinstance(branch_sub, list):
            break

        # check if key exists in dict
        key = guess[:i + 1]
        if not key in branch_sub:
            return ["NO WORDS EXIST"]
        
        branch = branch_sub[key]
    
    # return count (branch[0]) if branch[1] is dictionary
    if isinstance(branch[1], dict):
        string = "%s WORDS" % str(branch[0])
        return [string]
    
    # else return valid guesses from list
    branch_sub = branch[1]
    results = []
    for word in branch_sub:
        # see if word is guess
        if guess == word:
            return [guess.upper() + ": VALID GUESS"]

        # otherwise word start matches with guess
        if word[:len(guess)] == guess:
            results.append(word)
    
    if len(results) > 0:
        return results
    
    return ["INVALID WORD"]

def validate_word(word: str) -> bool:
    length = len(word)

    # make sure length is ok
    if length > 8 or length < 2:
        return False
    
    # check if inside tree
    branch = get_tree(length)

    for i in range(length):
        # branch[0] is number of valid guesses in branch[1]
        sub_branch = branch[1]

        # break if list
        if isinstance(sub_branch, list):
            break

        key = word[:i + 1]

        # if there is no key the word doesn't exist
        if not key in sub_branch:
            return False

        # else branch is sub_branch
        branch = sub_branch[key]
    
    sub_branch = branch[1]
    
    # True if in branch
    if word in sub_branch:
        return True

    # else False
    return False

# menu drawing
def draw_menu(screen):
    global menu_selection

    # Title
    draw_text_row(" " * spacing, screen, 1, 0, [GREEN] * spacing)
    draw_text_row("Combordle", screen, 1, 1, [GREEN] * 9)

    # colors
    row_colors = [WHITE] * 4
    row_colors[menu_selection] = GREEN

    # lengths
    draw_len = [4, 7, 6, 4]

    # PLAY
    draw_text_row(" " * spacing, screen, 4, 0, [row_colors[0]] * spacing)
    draw_text_row("PLAY", screen, 4, 1, [row_colors[0]] * draw_len[0])

    # HISTORY
    draw_text_row(" " * spacing, screen, 6, 0, [row_colors[1]] * spacing)
    draw_text_row("HISTORY", screen, 6, 1, [row_colors[1]] * draw_len[1])

    # HOW TO
    draw_text_row(" " * spacing, screen, 8, 0, [row_colors[2]] * spacing)
    draw_text_row("HOW TO", screen, 8, 1, [row_colors[2]] * draw_len[2])

    # QUIT
    draw_text_row(" " * spacing, screen, 10, 0, [row_colors[3]] * spacing)
    draw_text_row("QUIT", screen, 10, 1, [row_colors[3]] * draw_len[3])

    # CURSOR
    # bottom
    pygame.draw.rect(screen, BLACK, (spacing * grid_size - 5, (5 + 2 * menu_selection) * grid_size, grid_size * draw_len[menu_selection] + 10, 5))
    # top
    pygame.draw.rect(screen, BLACK, (spacing * grid_size - 5, (4 + 2 * menu_selection) * grid_size - 5, grid_size * draw_len[menu_selection] + 10, 5))
    # left
    pygame.draw.rect(screen, BLACK, (spacing * grid_size - 5, (4 + 2 * menu_selection) * grid_size - 5, 5, grid_size + 10))
    # right
    pygame.draw.rect(screen, BLACK, ((spacing + draw_len[menu_selection]) * grid_size, (4 + 2 * menu_selection) * grid_size - 5, 5, grid_size + 10))

    # version
    draw_text_row("v" + version, screen, 13, 1)


# draw how to
def draw_how_to(screen):
    draw_text_row("How to play combordle:", screen, 0, 0, [GREEN] * 22)
    draw_text_row("You must guess a secret word that is a combination", screen, 2, 0)
    draw_text_row("   of 2 words, and is 10 letters long in total.", screen, 3, 0)
    draw_text_row("To make a guess, type a number, then each word. The", screen, 4, 0)
    draw_text_row("   number is the length of the first word.", screen, 5, 0)
    draw_text_row("Example: 6 throws lone", screen, 6, 0)
    draw_text_row("Different colors mean different things:", screen, 8, 0)
    draw_text_row("Green: Right letter, right spot", screen, 9, 0, [GREEN] * 31)
    draw_text_row("Yellow: Right letter, wrong spot", screen, 10, 0, [YELLOW] * 32)
    draw_text_row("White: Letter is not used", screen, 11, 0)
    draw_text_row("Press any key to go back to menu >", screen, 13, 0)

# draw history
def draw_history(screen):
    # title
    draw_text_row("Stats history", screen, 0, 0)
    draw_text_row("press any key to exit", screen, 0, 1)

    # text
    draw_text_row("Guesses", screen, 2, 0)
    draw_text_row("Total", screen, 2, 2)

    # get history
    with open("stats.json", "r") as json_file:
        history = json.load(json_file)
    
    # lengths
    h_lengths = []
    max_length = 0

    for key in history:
        h_lengths.append(history[key])
        if history[key] > max_length:
            max_length = history[key]

    # draw bars
    for i in range(11):
        l = str(i + 1)
        if l == "11":
            l = "X"
        
        if len(l) < 2:
            l = l + " "

        # draw # guesses
        draw_text_row(l, screen, i + 3, 0)
        
        # draw total guesses
        draw_text_row(str(h_lengths[i]), screen, i + 3, 2)

        # draw bars
        if h_lengths[i] > 0:
            x = grid_size * 3
            y = grid_size * (i + 3)
            w = (spacing * 2 - 4) * grid_size * h_lengths[i] / max_length
            pygame.draw.rect(screen, BLACK, (x, y, w, grid_size))

# guess processing
def attempt_guess_push():
    global all_letter_colors

    # try number
    try:
        length = int(current_guess[0])
    except:
        note("> %s is not a number" % current_guess[0])
        return
    
    # no space after number
    if current_guess[1] != " ":
        note(" | remove '%s' character" % current_guess[1])
        return

    # invalid number
    if int(current_guess[0]) < 2:
        note("> %s must be 2 or more" % current_guess[0])
        return
    if int(current_guess[0]) > 8:
        note("> %s must be 8 or less" % current_guess[0])
    
    # guess too long / short
    # 10 letters + 2 spaces + 1 number
    if len(current_guess) != 13:
        n = int(current_guess[0])
        note(str(n) + " " + "X" * n + " " + "X" * (10 - n) + " < Correct Format")
        return
    
    splits = current_guess.split(" ")

    # too many splits
    if not len(splits) == 3:
        note("> %s != 3 splits" % len(splits))
        return
    
    # number too long
    if len(splits[0]) != 1:
        note("> len(%s) != 1" % splits[0])
        return
    
    if len(splits[1]) != int(splits[0]):
        note("> len(%s) != %s" % (splits[1], splits[0]))
        return
    
    # validate words
    if not validate_word(splits[1]):
        note("> %s not valid word" % splits[1])
        return
    
    if not validate_word(splits[2]):
        note("> %s not valid word" % splits[2])
        return

    # combined word
    combord = splits[1] + splits[2]

    # word length wrong
    if len(combord) != 10:
        note("> len(%s) != 10" % combord)
        return 

    # push word
    string = splits[0] + " " + combord
    all_guesses.append(string)

    # remaining letter colors
    colors = get_guess_colors(string)
    
    # white -> black
    for i in range(10):
        if colors[i + 2] == WHITE:
            colors[i + 2] = BLACK

    # assign colors to alphabet list
    for i in range(2, len(string), 1):
        # turn letter to number 0-26
        n = ord(string[i].lower()) - ord('a')
        
        # skip if all_colors already green
        if all_letter_colors[n] == GREEN:
            continue
        
        # only replace all_colors YELLOW with GREEN
        if all_letter_colors[n] == YELLOW:
            if colors[i] == GREEN:
                all_letter_colors[n] = GREEN
            
            continue

        # otherwise replace all_letter_colors
        all_letter_colors[n] = colors[i]

    # win condition
    if combord == chosen_word and int(splits[0]) == word_combo[0]:
        return "WIN"
    
    return True

# pygame setup
pygame.init()
pygame.display.set_caption("Combordle " + version)
font = pygame.font.Font("RubikMonoOne-Regular.ttf", grid_size)

# colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 80)
GREEN = (80, 255, 80)
BLACK = (0, 0, 0)

# set screen
WIDTH = grid_size * spacing * 3
HEIGHT = grid_size * 14 + 5
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# logic bools
running = True

class SMode(Enum):
    MENU = 0
    GAME = 1
    PAUSED = 2
    HISTORY = 3
    HOW_TO = 4
    QUIT = 5

screen_mode = SMode.MENU
menu_selection = 0

# drawing methods
def draw_letter_box(text: str, screen, color, position: tuple):
    pygame.draw.rect(screen, color, (position[0], position[1], grid_size, grid_size))
    text_thing = font.render(text[0].upper(), True, BLACK)
    # +1 / -2 centers letter in box
    screen.blit(text_thing, (position[0] + 1, position[1] - 2))

def draw_text_row(text: str, screen, row: float, column: float, colors = []):
    base_x = column * spacing * grid_size
    
    y = row * grid_size
    
    i = 0
    for letter in text:
        x = base_x + i * grid_size

        # get color
        try:
            color = colors[i]
        except:
            color = WHITE

        draw_letter_box(letter, screen, color, (x, y))

        # increment
        i += 1

# set up
def refresh_game():
    global all_guesses
    global all_letter_colors
    global word_combo
    global chosen_word
    global current_guess
    global game_complete
    
    # guess data
    all_guesses = []
    all_letter_colors = [WHITE] * 26

    # pick the word
    word_combo = pick_word_combo(10, 2)
    chosen_word = pick_word(word_combo)

    current_guess = ""

    # setup notes
    note("Guess a word")
    # note(chosen_word)

    # game not complete
    game_complete = False


# logic loops
# checks if time to quit
def check_quit(events) -> bool:
    for event in events:
        if event.type == pygame.QUIT:
            return True
    
    return False

# main game
def game_loop(events, screen) -> bool:
    global current_guess
    global all_guesses
    
    done = False

    # event logic
    for event in events:
        if event.type == pygame.KEYDOWN:
            # push guess on ENTER
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                result = attempt_guess_push()
                if result == "WIN":
                    current_guess = ""
                    note("WIN: " + chosen_word.upper())
                    add_to_history(len(all_guesses))
                    done = True
                elif result == True:
                    current_guess = ""
                    note("Guess a word")
                    
                    # lose if hit max guesses and didn't win
                    if len(all_guesses) >= 10:
                        note("You Lose | Correct word: %s %s" %(word_combo[0], chosen_word))
                        add_to_history(11)
                        done = True
            
            # add space
            if event.key == pygame.K_SPACE:
                current_guess += " "

            # add characters
            if event.unicode.isalnum():
                current_guess += event.unicode.lower()
            
            # backspace to delete
            if event.key == pygame.K_BACKSPACE:
                current_guess = current_guess[:-1]
            
            # restrict guess length
            if len(current_guess) > spacing * 3 - 1:
                    current_guess = current_guess[:-1]

    # clear screen
    screen.fill(WHITE)

    # draw screen
    draw_game_screen(screen)

    # return result
    return done

# wait for key press to continue
def pause_for_keypress(events) -> bool:
    for event in events:
        if event.type == pygame.KEYDOWN:
            return True
    
    return False

# main menu
def menu_loop(events, screen):
    global menu_selection

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if menu_selection == 0:
                    return SMode.GAME
                elif menu_selection == 1:
                    return SMode.HISTORY
                elif menu_selection == 2:
                    return SMode.HOW_TO
                elif menu_selection == 3:
                    return SMode.QUIT
            elif event.key == pygame.K_DOWN:
                menu_selection += 1
            elif event.key == pygame.K_UP:
                menu_selection -= 1
            
            if menu_selection > 3:
                menu_selection -= 4
            
            if menu_selection < 0:
                menu_selection += 4

    # clear
    screen.fill(WHITE)

    # draw
    draw_menu(screen)

    return SMode.MENU

# history
def history_loop(events, screen):
    for event in events:
        if event.type == pygame.KEYDOWN:
            return SMode.MENU

    # clear
    screen.fill(WHITE)

    # draw
    draw_history(screen)

    return SMode.HISTORY

# how to
def how_to(events, screen):
    for event in events:
        if event.type == pygame.KEYDOWN:
            return SMode.MENU

    # clear
    screen.fill(WHITE)

    # draw
    draw_how_to(screen)

    return SMode.HOW_TO


# set up game
refresh_game()

# start main loop
while running:
    # get events
    events = pygame.event.get()

    # see if quitting
    running = not check_quit(events)
    
    # handle events
    # main menu
    if screen_mode == SMode.MENU:
        screen_mode = menu_loop(events, screen)

    # game
    elif screen_mode == SMode.GAME:
        if game_loop(events, screen):
            screen_mode = SMode.PAUSED
            draw_text_row("Press any key to continue>", screen, 12, 0, [GREEN] * 30)

    # game waits for backspace to go to main menu
    elif screen_mode == SMode.PAUSED:
        if pause_for_keypress(events):
            screen_mode = SMode.MENU
            menu_selection = 0
            refresh_game()
    
    # game history
    elif screen_mode == SMode.HISTORY:
        screen_mode = history_loop(events, screen)
    
    # how to play
    elif screen_mode == SMode.HOW_TO:
        screen_mode = how_to(events, screen)
    
    # quit
    elif screen_mode == SMode.QUIT:
        running = False

    # update pygame
    pygame.display.update()

pygame.quit()