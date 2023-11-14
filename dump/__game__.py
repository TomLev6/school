import pygame


class Game:
    def __init__(self, id):
        self.p1_moved = False
        self.p2_moved = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    def get_player_move(self, p):
        return self.moves[p]

    def player(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1_moved = True
        else:
            self.p2_moved = True

    def connected(self):
        return self.ready

    def both_went(self):
        return self.p1_moved and self.p2_moved

    def winner(self):
        p1 = self.moves[0]
        p1 = self.moves[1]
        winner = -1
        if p1 == "r"



