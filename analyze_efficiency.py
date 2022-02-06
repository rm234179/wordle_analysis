import time
import solve_wordle


# first = [(1, 1),
#          (2, 178),
#          (3, 2060),
#          (4, 4429),
#          (5, 3170),
#          (6, 1589),
#          (7, 753),
#          (8, 399),
#          (9, 201),
#          (10, 100),
#          (11, 51),
#          (12, 24),
#          (13, 10),
#          (14, 3),
#          (15, 3),
#          (16, 1)]

# (14, ['bares', 'cills', 'rarks'])
# (15, ['bills', 'karks', 'rares'])
# (16, ['lills'])



if __name__ == '__main__':
    t0 = time.time()
    all_words = solve_wordle.load_words('wordle_words.json')
    words_to_find = solve_wordle.get_random_words(all_words, 1000)
    # scoring_algorithm = solve_wordle.get_most_unique_score_look_at_letter_score
    # scoring_algorithm = solve_wordle.get_most_unique_score_look_at_allowed_words
    # scoring_algorithm = solve_wordle.get_most_unique_score_look_at_all_words
    scoring_algorithm = solve_wordle.get_most_unique_score_look_at_letter_score_all_words
    # dt, number_words_by_count, words_by_count = solve_wordle.find_serial(all_words, words_to_find, scoring_algorithm)
    dt, number_words_by_count, words_by_count = solve_wordle.find_parallel(all_words, words_to_find, scoring_algorithm)
    print(dt)
    print(number_words_by_count)
    print(words_by_count)


    # solve_wordle.find_steps_required_to_solve(('aloft', all_words, solve_wordle.get_most_unique_score_look_at_all_words, 5, True))
    print(f"Elapsed time {time.time() - t0: 0.2f} seconds")