from gym.core import Env
from .utils import get_valid_moves
from .Algorithm import Algorithm
import time

__all__ = ['BFS', 'DFS']


class FS(Algorithm):
    def __init__(self, env_name: str = "MiniHack-MazeWalk-15x15-v0", informed: bool = True, name: str = "BFS", pop_index=0):
        super().__init__(env_name, name)
        self.informed = informed
        self.pop_index = pop_index  # BFS default

    def __call__(self, seed: int):
        start_time = time.time()
        local_env, local_state, local_game_map, start, target = super().initialize_env(seed, self.informed)

        queue = [start]
        visited = set(start)
        path = []

        while queue:
            node = queue.pop(self.pop_index)
            for neighbor in get_valid_moves(local_game_map, node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    path.append(neighbor)
                    if neighbor == target or neighbor == '@':
                        return list(path), list(visited), time.time() - start_time


class BFS(FS):
    def __init__(self, env_name: str = "MiniHack-MazeWalk-15x15-v0", informed: bool = True):
        super().__init__(env_name=env_name, informed=informed, name='BFS', pop_index=0)

    def __call__(self, seed: int, return_visited: bool = False, return_time: bool = False):
        return super().__call__(seed)


class DFS(FS):
    def __init__(self, env_name: str = "MiniHack-MazeWalk-15x15-v0", informed: bool = True):
        super().__init__(env_name=env_name, informed=informed, name='DFS', pop_index=-1)

    def __call__(self, seed: int, return_visited: bool = False, return_time: bool = False):
        return super().__call__(seed)
