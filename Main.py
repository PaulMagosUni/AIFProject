import sys
import pandas as pd
from algorithms import *
import numpy as np
from tqdm import tqdm
from typing import Callable
from algorithms.pseudo_heuristics import NNHeuristic

df = pd.DataFrame(columns=['name', 'path', 'visited', 'time', 'maze', 'explored', 'solution', 'score'], dtype=object)

num_examples = 10000

env_name1 = 'MiniHack-MazeWalk-Mapped-45x19-v0'
env_name2 = "MiniHack-MazeWalk-Mapped-15x15-v0"
env_name3 = "MiniHack-MazeWalk-Mapped-9x9-v0"

algorithms = [
    # BFS(env_name1),
    # DFS(env_name1),
    # AStar(env_name1),
    # AStar(env_name1, h='euclidean', name='ASTAR-EUCLIDEAN'),
    # Greedy(env_name1),
    # Dijkstra(env_name1),
    # BFS(env_name2),
    # DFS(env_name2),
    # AStar(env_name2),
    # AStar(env_name2, h='euclidean', name='ASTAR-EUCLIDEAN'),
    # Greedy(env_name2),
    # Dijkstra(env_name2),
    # BFS(env_name3),
    # DFS(env_name3),
    # AStar(env_name3),
    # AStar(env_name3, h='euclidean', name='ASTAR-EUCLIDEAN'),
    # Greedy(env_name3),
    # Dijkstra(env_name3),
    # MiniMax(env_name1),
    # MiniMax(env_name2),
    # MiniMax(env_name3),
    AStar(env_name1, h=NNHeuristic(), name='ASTAR-NN'),
    # QLSTM(env_name),
    # Genetic(env_name),
    # Qlearning(env_name)
    # AlphaBeta(env_name, depth=5),
]
def call(algorithm: Callable, seed: int, i: int, name: str, env_name: str, pbar: tqdm):
    output = tuple([name]) + algorithm(seed) + tuple([f'{env_name}_{i}']) + tuple([seed])
    pbar.update(1)
    return output

results = []
mean = 0
with tqdm(total=num_examples * len(algorithms)) as pbar:
    for i in range(num_examples):
        rand_seed = np.random.randint(0, sys.maxsize)
        # insert into df
        df = pd.DataFrame([call(algorithm=alg, seed=rand_seed, i=i, name=alg.name, env_name=alg.env_name, pbar=pbar) for alg in algorithms],
                          columns=['name', 'pixels', 'solved', 'path', 'visited', 'time', 'maze', 'seed'])
        # Save for each maze keep only the one with the lowest path length
        df['path_length'] = df['path'].apply(lambda x: len(x))
        df = df.sort_values(by=['maze', 'path_length'])
        df = df.drop_duplicates(subset=['maze'], keep='first')
        df = df.reset_index(drop=True)
        # Save the best path

        # mean = sum([np.mean([result.solved]) for result in results])/len(results)
        # pbar.set_description(f'Completed Maze {i}, Completed Maze Solved: {round(np.mean([results[-1].solved]), 3)}, Mean: {round(mean, 3)}')

# df = pd.concat(results).reset_index(drop=True)
# df.to_csv('results.csv')
#
# df.to_csv('results_all.csv')
# df = df[['name', 'time', 'explored', 'solution', 'ex_sol_score', 'score']]
# df = df.groupby('name').agg(
#     {'time': ['mean', 'std'], 'explored': ['mean', 'std'], 'solution': ['mean', 'std'], 'ex_sol_score': ['mean', 'std'],
#      'score': ['mean', 'std']})
# df.columns = ['_'.join(col) for col in df.columns.values]
# df = df.reset_index()
# df.to_csv('results.csv')
