import numpy as np
import math

__all__ = ['get_player_location', 'get_target_location', 'get_edges_location', 'is_wall', 'get_heuristic',
           'get_valid_moves', 'actions_from_path', 'euclidean_distance', 'manhattan_distance']

from typing import Tuple, List, Any, Union


def get_player_location(game_map: np.ndarray, symbol: str = "@") -> tuple[
    np.ndarray[Any, np.dtype[Union[np.signedinteger[Any], np.longlong]]],
    np.ndarray[Any, np.dtype[Union[np.signedinteger[Any], np.longlong]]]]:
    x, y = np.where(game_map == ord(symbol))
    return x[0], y[0]


def get_target_location(game_map: np.ndarray, symbol: str = ">") -> tuple[
    np.ndarray[Any, np.dtype[Union[np.signedinteger[Any], np.longlong]]],
    np.ndarray[Any, np.dtype[Union[np.signedinteger[Any], np.longlong]]]]:
    x, y = np.where(game_map == ord(symbol))
    return x[0], y[0]


def get_edges_location(game_map: np.ndarray, symbol: str = "X") -> tuple[
    np.ndarray[Any, np.dtype[Union[np.signedinteger[Any], np.longlong]]],
    np.ndarray[Any, np.dtype[Union[np.signedinteger[Any], np.longlong]]]]:
    x, y = np.where(game_map == ord(symbol))
    return x, y


def is_wall(position_element: Union[int, chr]) -> bool:
    obstacles = "|- "
    return chr(position_element) in obstacles


def get_valid_moves(game_map: np.ndarray, current_position: Tuple[int, int]) -> List[Tuple[int, int]]:
    x_limit, y_limit = game_map.shape
    valid = []
    x, y = current_position
    # North
    if (y - 1 > 0) and not is_wall(game_map[x, y - 1]):
        valid.append((x, y - 1))
        # East
    if x + 1 < x_limit and not is_wall(game_map[x + 1, y]):
        valid.append((x + 1, y))
        # South
    if y + 1 < y_limit and not is_wall(game_map[x, y + 1]):
        valid.append((x, y + 1))
        # West
    if x - 1 > 0 and not is_wall(game_map[x - 1, y]):
        valid.append((x - 1, y))

    return valid


def actions_from_path(start: Tuple[int, int], path: List[Tuple[int, int]]) -> List[int]:
    action_map = {
        "N": 0,
        "E": 1,
        "S": 2,
        "W": 3
    }
    actions = []
    x_s, y_s = start
    for (x, y) in path:
        if x_s == x:
            if y_s > y:
                actions.append(action_map["W"])
            else:
                actions.append(action_map["E"])
        elif y_s == y:
            if x_s > x:
                actions.append(action_map["N"])
            else:
                actions.append(action_map["S"])
        else:
            raise Exception("x and y can't change at the same time. oblique moves not allowed!")
        x_s = x
        y_s = y

    return actions


def euclidean_distance(point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def manhattan_distance(point1: Tuple[int, int], point2: Tuple[int, int]) -> int:
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)


heuristics = {
    'manhattan': manhattan_distance,
    'euclidean': euclidean_distance
}


def get_heuristic(heuristic: str):
    if heuristic in heuristics.keys():
        return heuristics[heuristic]
    else:
        raise Exception("Heuristic not supported!")