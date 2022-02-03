import logging
import solve_wordle

all_words = solve_wordle.load_words('wordle_words.json')
print(solve_wordle.find_steps_required_to_solve('apple', all_words))