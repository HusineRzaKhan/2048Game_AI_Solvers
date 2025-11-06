from GameManager import Node
from GameManager import Player


class AlphaBetaSearch(object):
    def __init__(self):
        self.evaluations = []

    def search(self, root, depth=3):
        Node.max_depth = depth
        self.evaluations = []
        value = self.max_value(root, -float("inf"), float("inf"))
        if len(self.evaluations) > 0:
            best = max(self.evaluations, key=lambda t: t[0])
            print("\n----------PREVIOUS------------")
            print(root)
            print("----------BEST NEXT------------")
            print(best[1])
            print(best[1].get_heuristic_value())
            print("\n----------ALTERNATIVES------------")
            for tile in self.evaluations:
                print(tile[1])
                print("HEURISTIC: " + str(tile[1].get_heuristic_value()))
                print("EVAL: " + str(tile[0]))
                print("-----------------")
            print("------------------------------")
            print("\n\n")
            return best[1]
        return None

    def max_value(self, node, alpha, beta):
        if node.terminal_state():
            return node.get_heuristic_value()

        value = -float("inf")
        for child in node.get_max_children():
            value = max(value, self.min_value(child, alpha, beta))
            if node.root:
                self.evaluations.append((value, child))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, node, alpha, beta):
        if node.terminal_state():
            return node.get_heuristic_value()
        value = float("inf")
        for child in node.get_min_children():
            value = min(value, self.max_value(child, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value
