import time
import solve_wordle
from multiprocessing import Pool


first = [(1, 1),
(2, 178),
(3, 2060),
(4, 4429),
(5, 3170),
(6, 1589),
(7, 753),
(8, 399),
(9, 201),
(10, 100),
(11, 51),
(12, 24),
(13, 10),
(14, 3),
(15, 3),
(16, 1)]

# (14, ['bares', 'cills', 'rarks'])
# (15, ['bills', 'karks', 'rares'])
# (16, ['lills'])

def find_parallel(all_words, words_to_find):
    words_by_count = {}
    guesses_to_show = 0
    debug = False
    data = [(word, all_words, guesses_to_show, debug) for word in words_to_find]
    with Pool(14) as p:
        results = p.map(solve_wordle.find_steps_required_to_solve, data)
        for res in results:
            counter, word = res
            if counter not in words_by_count:
                words_by_count[counter] = []
            words_by_count[counter].append(word)

    print()
    for counter in sorted(words_by_count.keys()):
        print((counter, len(words_by_count[counter])))
        if counter > 13:
            print((counter, words_by_count[counter]))


if __name__ == '__main__':
    t0 = time.time()
    all_words = solve_wordle.load_words('wordle_words.json')
    find_parallel(all_words, all_words)
    # counter, word = solve_wordle.find_steps_required_to_solve(('karks', all_words, 0, False))
    # print(f"It took {counter} guesses to get {word}")
    print(f"Elapsed time {time.time() - t0: 0.2f} seconds")