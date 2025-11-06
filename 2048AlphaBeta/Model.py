import random
from enum import Enum
from GameManager import Node, Player
import math


class Game(object):
    spawn_probability = [[4, 0.1], [2, 0.9]]
    probability = {4: 0.1, 2: 0.9}
    dim = 4
    nr_of_tiles = 16
    all_min_children = False


class GameState(object):
    def __init__(self, root=False):
        self.board = []
        self.nr_empty_tile = Game.nr_of_tiles
        if root:
            for i in range(Game.dim * Game.dim):
                self.board.append(0)
            self.set_random_tile()
            self.set_random_tile()

    def set_random_tile(self):
        empty = self.get_empty_tiles()
        random.shuffle(empty)
        i = empty.pop()
        n = self.pick_random()
        self.set(i, n)

    def pick_random(self):
        r, s = random.random(), 0
        for num in Game.spawn_probability:
            s += num[1]
            if s >= r:
                return num[0]
        return 2

    def get_XY(self, i):
        return i % Game.dim, math.floor(i / Game.dim)

    def get_index(self, x, y):
        return (Game.dim * y) + x

    def get(self, x, y):
        return self.board[(Game.dim * y) + x]

    def set(self, i, value):
        self.board[i] = value
        self.nr_empty_tile -= 1

    def copy_state(self):
        child = GameState()
        child.board = self.board[:]
        child.nr_empty_tile = self.nr_empty_tile
        return child

    def get_empty_tiles(self):
        empty_indices = []
        for i in range(Game.dim * Game.dim):
            if self.board[i] == 0:
                empty_indices.append(i)
        return empty_indices

    def create_representation(self):
        return self.board

    def perform_action(self, direction):
        movement = False
        for row in range(Game.dim):
            combined = False
            for col in self.calc_range(direction):
                i = self.calc_index(direction, row, col)
                for c in self.calc_range2(direction, col):
                    j = self.calc_index(direction, row, c)
                    if self.board[i] > 0 and self.board[j] > 0:
                        if not combined and self.board[i] == self.board[j]:
                            self.combine(i, j)
                            combined = True
                            movement = True
                        break
                    elif self.board[i] == 0 and self.board[j] > 0:
                        movement = True
                        self.move(i, j)
        return movement

    def calc_range2(self, d, col):
        if d is Direction.RIGHT or d is Direction.DOWN:
            return range(col - 1, -1, -1)
        elif d is Direction.LEFT or d is Direction.UP:
            return range(col + 1, Game.dim)

        raise Exception("Not a valid Enum")

    def calc_range(self, d):
        if d is Direction.RIGHT or d is Direction.DOWN:
            return range(Game.dim - 1, -1, -1)
        elif d is Direction.LEFT or d is Direction.UP:
            return range(0, Game.dim)

        raise Exception("Not a valid enum")

    def calc_index(self, d, row, col):
        if d is Direction.LEFT or d is Direction.RIGHT:
            return (Game.dim * row) + col
        else:
            return (Game.dim * col) + row

    def combine(self, s, t):
        new_value = self.board[t] + self.board[s]
        self.board[s] = new_value
        self.board[t] = 0
        self.nr_empty_tile += 1

    def terminal_state(self):
        if self.nr_empty_tile > 0:
            return False
        else:
            dim = Game.dim
            for i in range(0, dim):
                for j in range(1, dim):
                    if self.get(j, i) == self.get(j - 1, i) or self.get(i, j) == self.get(i, j - 1):
                        return False
            return True

    def move(self, to_index, from_index):
        self.board[to_index] = self.board[from_index]
        self.board[from_index] = 0

    def __repr__(self):
        representation = ""
        for i in range(0, Game.dim):
            representation += "|"
            for j in range(0, Game.dim):
                value = self.board[(Game.dim * i) + j]
                representation += str(value) + "\t"
            representation += "|\n"
        return representation


class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class GameNode(Node):
    def __init__(self, state, parent=None, player=Player.MAX, tile=None):
        super().__init__(parent=parent, player=player)
        self.state = state
        self.last_tile = tile
        self.all_children = True

    def __repr__(self):
        return self.state.__repr__()

    def get_heuristic_value(self):
        corner = self.largest_in_corner()
        available = self.available_tiles()
        monotonicity = self.monotonicity()
        merges = self.merge_possibilities()
        score = (4500 * available) + (500 * corner) + (4000 * monotonicity) + (1000 * merges)
        # print("------------------------------------")
        # print(self.state)
        # print("AVAILABLE: " + str(available))
        # print("CORNER: " + str(corner))
        # print("SMOOTHNESS: " + str(smoothness))
        # print("MONOTONICITY: " + str(monotonicity))
        # print("TOTAL-SCORE: " + str(score))
        # print("------------------------------------")
        return score

    def available_tiles(self):
        open_tiles = self.state.nr_empty_tile
        return float(open_tiles / 16)

    def monotonicity(self):
        score = 0
        # max_score = 24
        max_score = 48
        for i in range(0, Game.dim):
            for j in range(1, Game.dim):
                if self.state.get(j - 1, i) < self.state.get(j, i):
                    # score += 1
                    score += j
                elif self.state.get(j - 1, i) > self.state.get(j, i):
                    # score -= 1
                    score -= j

                if self.state.get(i, j - 1) < self.state.get(i, j):
                    score += j
                elif self.state.get(i, j - 1) > self.state.get(i, j):
                    score -= j
        return float(score / max_score)

    def largest_in_corner(self, ):
        largest_value = max(self.state.board)
        if self.state.get(3, 3) >= largest_value:
            return 1
        else:
            return 0

    def merge_possibilities(self):
        largest_value = math.log2(max(self.state.board))
        score = 0
        for i in range(0, Game.dim):
            for j in range(1, Game.dim):
                if self.state.get(j - 1, i) == self.state.get(j, i) and self.state.get(j, i) > 0:
                    score += float(math.log2(self.state.get(j, i)) / largest_value)
                if self.state.get(i, j - 1) == self.state.get(i, j) and self.state.get(i, j) > 0:
                    score += float(math.log2(self.state.get(i, j)) / largest_value)
        return score

    def is_state_terminal(self):
        return self.state.terminal_state()

    def probability(self, n):
        return float((1 / n) * Game.probability[self.last_tile])

    def generate_successors(self, p):
        succ = []
        if p is Player.MIN:
            empty_slots = self.state.get_empty_tiles()
            for i in empty_slots:
                if Game.all_min_children or len(empty_slots) <= 4:
                    new_state = self.state.copy_state()
                    new_state.set(i, 2)
                    succ.append(GameNode(
                        new_state,
                        parent=self,
                        player=Player.MIN,
                        tile=2
                    ))
                    new_state = self.state.copy_state()
                    new_state.set(i, 2)
                    succ.append(GameNode(new_state,
                                         parent=self,
                                         player=Player.MIN,
                                         tile=4
                                         ))
                else:
                    new_state = self.state.copy_state()
                    tile_value = self.state.pick_random()
                    new_state.board[i] = tile_value
                    succ.append(GameNode(new_state,
                                         parent=self,
                                         player=Player.MIN,
                                         tile=tile_value
                                         ))
        elif p is Player.MAX:
            for i in range(1, Game.dim + 1):
                new_state = self.state.copy_state()
                movement = new_state.perform_action(Direction(i))
                if movement:
                    succ.append(GameNode(
                        new_state,
                        parent=self,
                        player=Player.MAX
                    ))
        return succ


board = [
    64, 32, 16, 8,
    32, 16, 8, 4,
    16, 8, 4, 2,
    8, 16, 2, 4,
]

board2 = [
    0, 0, 0, 0,
    2, 2, 2, 0,
    2, 4, 2, 2,
    4, 2, 1028, 1028,
]

state = GameState()
state.board = board2
node = GameNode(state)
print(node.monotonicity())
print(node.largest_in_corner())
print(node.available_tiles())
print(node.merge_possibilities())
