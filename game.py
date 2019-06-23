import uuid
import random
from copy import deepcopy

class Game:
    player_to_game = {}
    open_games = []
    active_games = {}

    def __init__(self, player_id):
        self.players = [player_id]
        self.id = str(uuid.uuid4())

        Game.open_games.append(self)

        self._board = [[None] * 3 for i in range(3)]
        self._turn = random.choice((True, False))


    @staticmethod
    def get_game(game_id):
        if game_id not in Game.active_games:
            return None

        return Game.active_games[game_id]


    @staticmethod
    def join_game(player_id):
        if player_id in Game.player_to_game:
            return Game.player_to_game[player_id]

        try:
            game = Game.open_games.pop()
        except IndexError:
            return Game(player_id)

        game.players.append(player_id)
        Game.player_to_game[player_id] = game
        Game.active_games[game.id] = game
        return game


    def get(self, x, y):
        return self._board[x][y]


    def place(self, x, y):
        if self._board[x][y] != None:
            return False

        self._board[x][y] = self._turn
        self._turn = not self._turn
        return True


    def who_won(self):
        if self.is_won():
            return self.players[not self._turn]
        return None


    def is_won(self):
        # rows
        for i in range(3):
            if self._board[i][0] == self._board[i][1] == self._board[i][2] != None:
                return True

        # columns
        for i in range(3):
            if self._board[0][i] == self._board[1][i] == self._board[2][i] != None:
                return True

        # diagonals
        if self._board[0][0] == self._board[1][1] == self._board[2][2] != None:
            return True

        if self._board[2][0] == self._board[1][1] == self._board[0][2] != None:
            return True

        return False


    def whose_turn(self):
        return self.players[int(self._turn)]


    def to_list(self):
        return deepcopy(self._board)
