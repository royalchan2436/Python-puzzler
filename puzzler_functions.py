'''Phrase Puzzler: functions'''

import random


# Phrase Puzzler constants

DATA_FILE = 'puzzles_small.txt'

HIDDEN = '^'

VOWEL_PRICE = 1
CONSONANT_BONUS = 2

# Game types
HUMAN = '1'
HUMAN_HUMAN = '2'
HUMAN_COMPUTER = '3'

# Computer difficulty levels
EASY = 'E'
HARD = 'H'

# Players' names
PLAYER_ONE = 'Player One'
PLAYER_TWO = 'Player Two'

# Consonant and vowel sets
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
VOWELS = 'aeiou'

# Menu options
CONSONANT = 'C'
VOWEL = 'V'
SOLVE = 'S'
QUIT = 'Q'

# The order in which a computer player, hard difficulty, will guess consonants.
PRIORITY_CONSONANTS = 'tnrslhdcmpfgybwvkqxjz'


# Define your functions here.

def is_win(puzzle, view):
    '''(str, str) -> bool

    Return True iff puzzle is the same as view.


    >>> is_win('banana', 'banana')
    True
    >>> is_win('apple', 'banana')
    False
    '''
    # put the function body here
    return puzzle == view

def game_over(puzzle,view,current_selection):
    '''(str,str,str) -> bool

    Return True iff the puzzle is the same as the view or the selection is true
    
    >>>game_over('banana','apple','Q')
    True
    >>>game_over('banana','apple','C')
    False
    '''
    return puzzle == view or current_selection == 'Q'
    
def get_view(puzzle):
    '''(str) -> str

    Return the hidden replace the puzzle

    >>>get_view('banana')
    ^^^^^^
    >>>get_view('let's go')
    ^^^'^ ^^

    '''
    display = ''
    for ch in puzzle :
        if ch in CONSONANTS or ch in VOWELS :
            display =  display + HIDDEN
        else :
            display = display + ch
    return display
        

def update_view(puzzle,view,guess_letter):
    '''(str,str,str) -> str

    Return the view of the puzzle with each occurrence of the letter
    in the puzzle revealed

    >>>update_view('apple','^pp^^','a')
    'app^^'
    >>>update_view()

    '''
    display = ''
    dis = ''
    for ch in view :
        if ch == HIDDEN :
            display = display + guess_letter
        else :
            display = display + ch
    temp = display
    for i in range(len(view)):
         if puzzle[i] == temp[i] :
             dis = dis + puzzle[i]
         else :
             dis = dis + HIDDEN
    return dis

def make_guessed(unguess_consonant,unguess_vowel,letter):
    '''(str,str,str) -> tuple of (str,str)

    Return the first two parameters with the letter removed from whichever 
    string,if any, contains it

    >>>make_guessed('hks','aeiou','a')
    ('hks','eiou')
    >>>make_guessed('hks','aeiou','h')
    ('ks','aeiou')
    '''
    display = ''
    dis = ''
    for ch in unguess_consonant :
        if ch == letter :
            display = display + ''
        else :
            display = display + ch
    temp = display
    for ab in unguess_vowel :
        if ab == letter :
            dis = dis + ''
        else :
            dis = dis + ab
    return(temp,dis)

    

def calculate_score(current_score,occurrences_letter,kind_of_letter):
    '''(int,int,str) -> int

    Return the new score by adding one point per occurrence of the letter
    to the original score if the letter is a consonant, or by deducting
    the VOWEL_PRICE from the score if the letter is a vowel
    
    >>>calculate_score(4,3,'CONSONANT')
    7
    >>>calculate_score(4,3,'VOWEL')
    3
    '''
    if kind_of_letter == CONSONANT:
        return current_score + occurrences_letter
    elif kind_of_letter == VOWEL :
        return current_score - VOWEL_PRICE
    else :
        return False
    

def finalize_score(puzzle,view,unguessed_consonants,current_score):
    '''(str,str,str,int) -> int

    Return the final score, which is calculated by adding
    CONSONANT_BONUS points to the score for each unguessed consonant from
    the puzzle that is HIDDEN in the view

    >>>finalize_score('apple','a^^l^','ghjkpq',1)
    5
    
    '''
    count = 0
    for ch in puzzle :
        if ch in unguessed_consonants :
            count = count + 1
    return 1 + CONSONANT_BONUS * count       

def update_score(player_one_score,player_two_score,current_player_score,current_player):

    '''(int,int,int,int,str) -> tuple of (int,int)

    Return player one and player two's updated scores, replacing the
    score of the current player with the new score
    
    >>>update_score(1,3,2,PLAYER_ONE)
    (2,3)
    >>>update_score(1,3,2,PLAYER_TWO)
    (1,2)
    '''
    if current_player == PLAYER_ONE :
        player_one_score = current_player_score
    elif current_player == PLAYER_TWO :
        player_two_score = current_player_score
    else :
        return False
    return (player_one_score,player_two_score)

def next_player(current_player,number_occurrances_in_puzzle):
    '''(str,int) -> str

    Return the next player

    >>>next_player(PLAYER_ONE,2)
    PLAYER_ONE
    >>>next_player(PLAYER_TWO,0)
    PLAYER_ONE
    '''
    if number_occurrances_in_puzzle > 0 :
        return current_player
    elif number_occurrances_in_puzzle == 0:
        if current_player == PLAYER_ONE:
           return PLAYER_TWO
        elif current_player == PLAYER_TWO :
            return PLAYER_ONE
            
def guess_letter(unguessed_consonant,difficult_level):
    '''(str,str) -> str

    Return the consonant to be guessed next by the computer player

    >>>guess_letter('tsk',HARD)
    't'
    >>>guess_letter('tsk',EASY)
    'y'
    '''
    if difficult_level == EASY :
        return random.choice(unguessed_consonant)
    elif difficult_level == HARD :
        for abc in PRIORITY_CONSONANTS  :
            if abc in unguessed_consonant :
                return abc
            
    

def half_revealed(view):
    '''(str) -> bool

    Return True iff at least half of the alphabetic characters in the
    view are revealed

    >>>half_revealed('^^ple')
    True
    >>>half_revealed('^^^^e')
    False
    '''
    count = 0
    for ch in view :
        if ch == HIDDEN :
            count = count + 1
    if count >= 0.5 * len(view) :
        return True
    else :
        return False
   
def is_match(puzzle,view):
    '''(str,str) -> bool

    Return True iff the view could be a view of the given puzzle

    >>>is_match('apple','^^ple')
    True
    >>>is_match('apple','^^^^k')
    False

    '''
    dis = ''
    if puzzle == view :
            return True
    elif view == HIDDEN*len(view) :
            return True
    elif len(puzzle) == len(view) :
        for i in range(len(view)) :
            if  view[i] == HIDDEN :
                dis = dis + puzzle[i]
            elif puzzle[i] == view[i]:
                dis = dis + view[i]
        if puzzle == dis:
            return True
        else :
            return False
    else :
        return False
            
    
