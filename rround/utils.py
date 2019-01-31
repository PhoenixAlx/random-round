import random

def prob_gen(prob):
    num = 0
    while num < prob:
        yield num
        num = random.random()




def get_num_rounds(prob):
    return len([i for i in prob_gen(prob)])

