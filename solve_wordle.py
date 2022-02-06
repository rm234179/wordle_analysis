import json
import random
import string
import time
from typing import Tuple, Dict, List, Set, Optional, Callable
from multiprocessing import Pool

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

def get_words_by_letter(words: Set[str]) -> Dict[chr, Set[str]]:
    words_by_letter = {}
    for letter in string.ascii_lowercase:
        words_by_letter[letter] = set()
    for word in words:
        for letter in word:
            words_by_letter[letter].add(word)
    return words_by_letter

def get_most_unique_score_look_at_letter_score(allowed_words: Set[str], all_words: Set[str],
                          required_letters: Set[Tuple[chr, Optional[int]]],
                          exclude_letters: Set[Tuple[chr, Optional[int]]],
                          ) -> List[Tuple[int, str]]:
    scores_and_words = []
    words_by_letter = get_words_by_letter(allowed_words)
    word_count_by_letter = {letter: len(words_by_letter[letter]) for letter in words_by_letter}
    for word in allowed_words:
        score = 0
        for letter in set(word):
            score += word_count_by_letter[letter]
        scores_and_words.append((score, word))
    best = sorted(scores_and_words, reverse=True)
    return best

def get_most_unique_score_look_at_letter_score_all_words(allowed_words: Set[str], all_words: Set[str],
                          required_letters: Set[Tuple[chr, Optional[int]]],
                          exclude_letters: Set[Tuple[chr, Optional[int]]],
                          ) -> List[Tuple[int, str]]:
    scores_and_words = []
    words_by_letter = get_words_by_letter(allowed_words)
    word_count_by_letter = {letter: len(words_by_letter[letter]) for letter in words_by_letter}
    for word in all_words:
        score = 0
        if word in allowed_words:
            score += 0.1
        for letter in set(word):
            score += word_count_by_letter[letter]
        scores_and_words.append((score, word))
    best = sorted(scores_and_words, reverse=True)
    return best

def get_most_unique_score_look_at_allowed_words(allowed_words: Set[str], all_words: Set[str],
                          required_letters: Set[Tuple[chr, Optional[int]]],
                          exclude_letters: Set[Tuple[chr, Optional[int]]],
                          ) -> List[Tuple[int, str]]:
    scores_and_words = []
    words_by_letter = get_words_by_letter(allowed_words)
    # This section looks for and removes letters that are common among all words
    num_allowed_words = len(allowed_words)
    for letter in words_by_letter:
        if len(words_by_letter[letter]) == num_allowed_words:
            words_by_letter[letter] = set()
    for word in allowed_words:
        score = 0
        tmp = set()
        for letter in set(word):
            tmp = tmp.union(words_by_letter[letter])
        score += len(tmp)
        scores_and_words.append((score, word))
    best = sorted(scores_and_words, reverse=True)
    return best

def get_most_unique_score_look_at_all_words(allowed_words: Set[str], all_words: Set[str],
                          required_letters: Set[Tuple[chr, Optional[int]]],
                          exclude_letters: Set[Tuple[chr, Optional[int]]],
                          ) -> List[Tuple[int, str]]:
    # TODO add ability to give extra partial points for
    #  looking for positions of required letters
    scores_and_words = []
    words_by_letter = get_words_by_letter(allowed_words)
    num_allowed_words = len(allowed_words)
    for letter in words_by_letter:
        if len(words_by_letter[letter]) == num_allowed_words:
            words_by_letter[letter] = set()
    for word in all_words:
        score = 0
        if word in allowed_words:
            score += 0.1
        tmp = set()
        for letter in set(word):
            tmp = tmp.union(words_by_letter[letter])
        score += len(tmp)
        scores_and_words.append((score, word))
    best = sorted(scores_and_words, reverse=True)
    return best



def simulate_guess(guess: str, word: str) -> str:
    response = '1'
    for i in range(5):
        if guess[i] == word[i]:
            response += 'y'
        elif guess[i] in word:
            response += 'm'
        else:
            response += 'n'
    return response

def single_loop(all_words: Set[str], 
                required_letters: Set[Tuple[chr, Optional[int]]], 
                exclude_letters: Set[Tuple[chr, Optional[int]]],
                scoring_algorithm: Callable[[Set[str], Set[str], Set[Tuple[chr, Optional[int]]], Set[Tuple[chr, Optional[int]]]], List[Tuple[int, str]]],
                guesses_to_show: int=3, guess_to_simulate: Optional[str]=None):
    allowed_words, not_allowed_words = get_words_with_letters(all_words, 
                           required_letters, 
                           exclude_letters)
    guesses = scoring_algorithm(allowed_words, all_words, required_letters, exclude_letters)
    if guesses_to_show > 0:
        print(f"\nNumber of Words Remaining: {len(allowed_words)}")
        for i in range(min(guesses_to_show, len(guesses))):
            print(f"{i + 1}. {guesses[i][1]} with score of {guesses[i][0]}")
    if guess_to_simulate is None:
        response = input("Enter your pick and the results: ")
    else:
        response = simulate_guess(guesses[0][1], guess_to_simulate)
        # print(f"Simulated response = {response}")
    pick_value = int(response[0]) - 1
    if pick_value == -1:
        print("Exiting")
        return (None, None, allowed_words, None)
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
    
        
def run_all(words: Set[str],
            scoring_algorithm: Callable[[Set[str], Set[str], Set[Tuple[chr, Optional[int]]], Set[Tuple[chr, Optional[int]]]], List[Tuple[int, str]]],):
    required_letters = set()
    exclude_letters = set()
    all_words = words.copy()
    while required_letters is not None:
        # print(("required", required_letters))
        # print(("excluded", exclude_letters))
        required_letters, exclude_letters, allowed_words, guess = single_loop(all_words, 
                                                                       required_letters, 
                                                                       exclude_letters,
                                                                       scoring_algorithm,
                                                                       guesses_to_show=5,
                                                                       guess_to_simulate=None)

def find_steps_required_to_solve(args: Tuple[
                                        str, Set[str],
                                        Callable[[Set[str], Set[str], Set[Tuple[chr, Optional[int]]], Set[Tuple[chr, Optional[int]]]], List[Tuple[int, str]]],
                                        int, bool
                                       ]) -> Tuple[int, str]:
    (word_to_find, words, scoring_algorithm, guesses_to_show, debug) = args
    counter = 0
    required_letters = set()
    exclude_letters = set()
    all_words = words.copy()
    while required_letters is not None:
        required_letters, exclude_letters, allowed_words, guess = single_loop(all_words, 
                                                                       required_letters, 
                                                                       exclude_letters,
                                                                       scoring_algorithm,
                                                                       guesses_to_show=guesses_to_show,
                                                                       guess_to_simulate=word_to_find)
        if debug:
            print(f'guess = {guess}')
        counter += 1
        if guess == word_to_find:
            break
    if debug:
        print((word_to_find, counter))
    return counter, word_to_find

def load_words(file_name: str) -> List[str]:
    with open(file_name, 'rt') as f:
        raw = json.load(f)
    all_words = list(sorted(raw['Ta'] + raw['La']))
    return all_words

def get_random_words(all_words: Set[str], number: int, seed: int=42) -> List[str]:
    random.seed(seed)
    sample = random.sample(all_words, number)
    return sample

def find_serial(all_words: Set[str], words_to_find: Set[str],
                scoring_algorithm: Callable[
                    [Set[str], Set[str], Set[Tuple[chr, Optional[int]]], Set[Tuple[chr, Optional[int]]]],
                    List[Tuple[int, str]]]) -> Tuple[float, Dict[int, int], Dict[int, Set[str]]]:
    t0 = time.time()
    words_by_count = {}
    guesses_to_show = 0
    debug = False
    data = [(word, all_words, scoring_algorithm, guesses_to_show, debug) for word in words_to_find]

    results = map(find_steps_required_to_solve, data)
    for res in results:
        counter, word = res
        if counter not in words_by_count:
            words_by_count[counter] = []
        words_by_count[counter].append(word)

    number_words_by_count = {}
    for counter in sorted(words_by_count.keys()):
        number_words_by_count[counter] = len(words_by_count[counter])

    t1 = time.time()
    dt = t1 - t0
    return dt, number_words_by_count, words_by_count

def find_parallel(all_words: Set[str], words_to_find: Set[str],
                scoring_algorithm: Callable[
                    [Set[str], Set[str], Set[Tuple[chr, Optional[int]]], Set[Tuple[chr, Optional[int]]]],
                    List[Tuple[int, str]]]) -> Tuple[float, Dict[int, int], Dict[int, Set[str]]]:
    t0 = time.time()
    words_by_count = {}
    guesses_to_show = 0
    debug = False
    data = [(word, all_words, scoring_algorithm, guesses_to_show, debug) for word in words_to_find]
    with Pool(14) as p:
        results = p.map(find_steps_required_to_solve, data)
        for res in results:
            counter, word = res
            if counter not in words_by_count:
                words_by_count[counter] = []
            words_by_count[counter].append(word)

    number_words_by_count = {}
    for counter in sorted(words_by_count.keys()):
        number_words_by_count[counter] = len(words_by_count[counter])

    t1 = time.time()
    dt = t1 - t0
    return dt, number_words_by_count, words_by_count

if __name__ == '__main__':
    all_words = load_words('wordle_words.json')
    print(f"Total number of words: {len(all_words)}")
    run_all(all_words, get_most_unique_score_look_at_all_words)
    
    