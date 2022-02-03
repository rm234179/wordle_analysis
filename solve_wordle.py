import json
import string
from typing import Tuple, Dict, List, Set, Optional

def get_words_with_letters(words: Set[str], 
                           required_letters: List[Tuple[chr, Optional[int]]], 
                           exclude_letters: List[Tuple[chr, Optional[int]]]) -> Tuple[Set[str], Set[str]]:
    allowed_words = set()
    not_allowed_words = set()
    for word in words:
        has_excluded = False
        for letter, location in exclude_letters:
            if location is None:
                if letter in word:
                    has_excluded = True
                    break
            else:
                if letter == word[location]:
                    has_excluded = True
                    break
        has_required = True
        for letter, location in required_letters:
            if location is None:
                if letter not in word:
                    has_required = False
                    break
            else:
                if letter != word[location]:
                    has_required = False
                    break
        if has_required and not has_excluded:
            allowed_words.add(word)
        else:
            not_allowed_words.add(word)
    return allowed_words, not_allowed_words

def get_words_by_letter(words):
    words_by_letter = {}
    for word in words:
        for letter in word:
            if letter not in words_by_letter:
                words_by_letter[letter] = set()
            words_by_letter[letter].add(word)
    return words_by_letter

def get_most_unique_score(words: Set[str]) -> List[Tuple[int, str]]:
    scores_and_words = []
    words_by_letter = get_words_by_letter(words)
    for word in words:
        score = 0
        for letter in set(word):
            score += len(words_by_letter[letter])
        scores_and_words.append((score, word))
    best = sorted(scores_and_words, reverse=True)
    return best

def simulate_guess(guess, word):
    response = '1'
    for i in range(5):
        if guess[i] == word[i]:
            response += 'y'
        elif guess[i] in word:
            response += 'm'
        else:
            response += 'n'
    return response

def single_loop(words: Set[str], 
                required_letters: Set[Tuple[chr, Optional[int]]], 
                exclude_letters: Set[Tuple[chr, Optional[int]]],
                guesses_to_show=3, guess_to_simulate=None):
    allowed_words, not_allowed_words = get_words_with_letters(words, 
                           required_letters, 
                           exclude_letters)

    guesses = get_most_unique_score(allowed_words)
    if guesses_to_show > 0:
        print(f"\nNumber of Words Remaining: {len(allowed_words)}")
        for i in range(min(guesses_to_show, len(guesses))):
            print(f"{i + 1}. {guesses[i][1]} with score of {guesses[i][0]}")
    if simulate_guess is None:
        response = input("Enter your pick and the results: ")
    else:
        response = simulate_guess(guesses[0][1], guess_to_simulate)
    pick_value = int(response[0]) - 1
    if pick_value == -1:
        print("Exiting")
        return (None, None, allowed_words)
    word = guesses[pick_value][1]
    new_required_letters = required_letters.copy()
    new_exclude_letters = exclude_letters.copy()
    for i in range(5):
        letter_response = response[i + 1]
        letter = word[i]
        if letter_response == 'n':
            new_exclude_letters.add((letter, None))
        elif letter_response == 'y':
            new_required_letters.add((letter, i))
        elif letter_response == 'm':
            new_required_letters.add((letter, None))
            new_exclude_letters.add((letter, i))
        else:
            raise ValueError()
    return new_required_letters, new_exclude_letters, allowed_words, word        
    
        
def run_all(words):
    required_letters = set()
    exclude_letters = set()
    allowed_words = words.copy()
    while required_letters is not None:
        # print(("required", required_letters))
        # print(("excluded", exclude_letters))
        required_letters, exclude_letters, allowed_words, guess = single_loop(allowed_words, 
                                                                       required_letters, 
                                                                       exclude_letters)

def find_steps_required_to_solve(word_to_find, words, guesses_to_show=0):
    counter = 0
    required_letters = set()
    exclude_letters = set()
    allowed_words = words.copy()
    while required_letters is not None:
        required_letters, exclude_letters, allowed_words, guess = single_loop(allowed_words, 
                                                                       required_letters, 
                                                                       exclude_letters, 
                                                                       guesses_to_show=guesses_to_show,
                                                                       guess_to_simulate=word_to_find)
        counter += 1
        if guess == word_to_find:
            break
    return counter

def load_words(file_name):
    with open(file_name, 'rt') as f:
        raw = json.load(f)
    all_words = list(sorted(raw['Ta'] + raw['La']))
    return all_words

if __name__ == '__main__':
    all_words = load_words('wordle_words.json')
    print(f"Total number of words: {len(all_words)}")
    run_all(all_words)
    
    