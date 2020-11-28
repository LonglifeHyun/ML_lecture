#-------------------------------------------------------------------------------
# Name:        201724557_장수현.py
# Purpose:     머신러닝 과제1 ( N-Queen with Genetic Algorithm )
#
# Author:      Jang SooHyun
#
# Created:     12-04-2020
# Copyright:   Jang SooHyun
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import random
import matplotlib.pyplot as plt
import numpy as np

N = 5
NUM_CHROMOSOME = 100
NUM_SELECTION = 10
NUM_AFTER_CROSS = (NUM_SELECTION*2)

BAD_WEIGHT = 3
GOOD_WEIGHT = 5
NUM_PAIR_NEIGHBOR = N*(N-1)//2
MAX_SCORE = (NUM_PAIR_NEIGHBOR*GOOD_WEIGHT)

# 전역 선언 #
generation = 0
cross_begin, cross_end = 0, 0
chromosome=[[0 for i in range(N)] for j in range(NUM_CHROMOSOME)]
score_fe=[[0,0]for i in range(NUM_CHROMOSOME)]
selected_chromosome=[[0 for i in range(N)] for j in range(NUM_SELECTION)]

def print_optimal_chromosome():
    global generation
    print("GENERATION : ",generation)
    print("Optimal Chromosome : ",end='')
    for i in range(0,len(chromosome[score_fe[0][0]])):
        print(chromosome[score_fe[0][0]][i]," ",end='')
    print('\n')

def print_answere():
    global generation
    print("The answere of "+str(N)+"-Queen is [",end='')
    for i in range(0,len(chromosome[score_fe[0][0]])-1):
        print(chromosome[score_fe[0][0]][i],"",end='')
    print(chromosome[score_fe[0][0]][-1],end='')
    print("]."'\n'"It's generation is "+str(generation)+".")

def initialization():
    for i in range(0,len(chromosome)):
        for j in range(0,len(chromosome[i])):
            chromosome[i][j] = random.randint(0, N-1)


def num_duplication(this_chromosome):
    dup_num = 0
    dup_cnt = [0 for i in range(N)]

    for i in range(0,len(chromosome[this_chromosome])):
        dup_cnt[chromosome[this_chromosome][i]] += 1

    for i in range(0,len(dup_cnt)):
        if (dup_cnt[i] > 1):
            dup_num += dup_cnt[i]

    return dup_num


def num_good_neighbor(this_chromosome):
    num_nei = 0;

    for i in range(0,len(chromosome[this_chromosome])-1):
        for j in range(i+1,len(chromosome[this_chromosome])):
            if (not ( chromosome[this_chromosome][i] == chromosome[this_chromosome][j] or
                      j-i == abs(chromosome[this_chromosome][i] - chromosome[this_chromosome][j]) )):
                num_nei += 1

    return num_nei


def fitness_evaluation():
    for i in range(0,len(score_fe)):
        score_fe[i][0] = i
        bad_score = num_duplication(i) * BAD_WEIGHT;
        good_score = num_good_neighbor(i) * GOOD_WEIGHT;
        score_fe[i][1] = good_score - bad_score;
        # 점수가 MAX_SCORE일 경우 해를 찾은 것.

    score_fe.sort(key=lambda x: x[1],reverse=True)


def selection():
    for i in range(0,NUM_SELECTION):
        for j in range(0,N):
            selected_chromosome[i][j] = chromosome[score_fe[i][0]][j]


def push_crossover_after():
    for i in range(0,len(selected_chromosome),2):
        cross_begin = random.randint(0, N)
        cross_end = random.randint(0, N)
        if (cross_begin > cross_end):
            cross_begin, cross_end = cross_end, cross_begin #swap


        # cross_begin이상 cross_end미만 구간 crossover.
        for j in range(0,cross_begin):
            chromosome[i][j] = selected_chromosome[i][j]
            chromosome[i+1][j] = selected_chromosome[i+1][j]

        for j in range(cross_begin,cross_end):
            chromosome[i][j] = selected_chromosome[i+1][j]
            chromosome[i+1][j] = selected_chromosome[i][j]

        for j in range(cross_end,len(chromosome[i])):
            chromosome[i][j] = selected_chromosome[i][j]
            chromosome[i+1][j] = selected_chromosome[i+1][j]


def push_crossover_before():
    for i,k in zip(range(NUM_SELECTION,NUM_SELECTION+len(selected_chromosome)),
                range(0,len(selected_chromosome)) ):
        for j in range(0,len(selected_chromosome[k])):
            chromosome[i][j] = selected_chromosome[k][j]

def crossover():
	push_crossover_after()
	push_crossover_before()


def mutate(mutation_chromosome):
    num_mutation = random.randint(0, N)
    for i in range(0,num_mutation):
        pos = random.randint(0, N-1)
        new_val = random.randint(0, N-1)
        mutation_chromosome[pos] = new_val;


def push_mutation(round):
    mutation_chromosome = [0 for i in range(N)]

    for i in range(0,NUM_AFTER_CROSS):
        for j in range(0,len(chromosome[i])):
            mutation_chromosome[j] = chromosome[i][j]

        mutate(mutation_chromosome)

        for j in range(0,len(mutation_chromosome)):
            chromosome[i+round*NUM_AFTER_CROSS][j] = mutation_chromosome[j]


def mutation():
    NUM_ROUND = (NUM_CHROMOSOME - NUM_AFTER_CROSS) // NUM_AFTER_CROSS;
    for i in range(1,NUM_ROUND+1):
        push_mutation(i)


def update_generation():
    global generation
    generation += 1

    selection()
    crossover()
    mutation()
    fitness_evaluation()

    print_optimal_chromosome()

def draw_answer():
    cell_text = [['' for i in range(N)] for j in range(N)]

    for i in range(0,N):
        cell_text[(N-1)-chromosome[score_fe[0][0]][i]][i] = 'Q'

    fig, ax = plt.subplots()
    ax.axis('off')

    the_table = ax.table(cellText=cell_text,loc='center',cellLoc='center')
    the_table.set_fontsize(16)
    the_table.scale(1,25/N)

    plt.savefig('201724557_장수현.png', dpi=300)
    plt.show()

def n_queen_with_genetic_algorithm():
    initialization()
    fitness_evaluation()
    print_optimal_chromosome()

    while(not(score_fe[0][1]==MAX_SCORE)):
        update_generation()

    print_answere()
    draw_answer()

def main():
    os.system('cls')
    if N > 3:
        n_queen_with_genetic_algorithm()
    else:
        print("It cannot be run. Please change value of N.")

if __name__ == '__main__':
    main()
