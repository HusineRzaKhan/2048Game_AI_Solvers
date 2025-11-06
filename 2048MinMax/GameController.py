from Model import GameState, Direction, GameNode, Game
from Search import AlphaBetaSearch
import sys
import time


class GameController(object):
    def __init__(self, display, solver=None):
        self.model = GameState(root=True)
        self.display = display
        self.running = False
        self.plies = 4
        self.display.event({"state": self.model.create_representation()})
        if not solver:
            self.solver = AlphaBetaSearch()
        else:
            self.solver = solver

    def set_solver(self, solver, all_min_children=False):
        Game.all_min_children = all_min_children
        self.solver = solver

    def action(self, direction):
        moved = self.model.perform_action(direction)
        self.display.event({"state": self.model.create_representation()})
        if moved:
            self.model.set_random_tile()
            self.display.event({"state": self.model.create_representation()})

    def start_solving(self):
        self.running = True
        while self.running:
            node = GameNode(self.model)
            selected_child = self.solver.search(node, self.plies)
            if not selected_child:
                print(max(node.state.board))
                self.running = False
                break
            self.model = selected_child.state
            self.send_state_snapshot()
            self.model.set_random_tile()
            self.send_state_snapshot()
            time.sleep(0.04)

    def stop_solving(self):
        self.running = False

    def set_new_board(self, board):
        if Game.nr_of_tiles == len(board):
            self.model.board = board
            print("Setting new board")
            self.send_state_snapshot()

    def send_state_snapshot(self):
        self.display.event({"state": self.model.create_representation()})
