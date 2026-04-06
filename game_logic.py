import random

#Class definition
class PegSolitaireGame:
    #creates initialization for game object, stores board size, sets to English by default
    def __init__(self, size=7, board_type="English"):
        self.size = size
        self.board_type = board_type
        self.board = []
        self.initialize_board()

    #This function checks valid positions in the board
    def is_valid_position(self, r, c):
        #This first part checks if row and column are inside the boundaries
        #Meaning, negative rows/columns are invalid, and rows/columns are too large.
        center = self.size // 2

        if not (0 <= r < self.size and 0 <= c < self.size):
            return False
    
        #This creates a classic cross shape english board
        if self.board_type == "English":
            # Standard cross shape for size 7
            if (r < 2 or r > self.size - 3) and (c < 2 or c > self.size - 3):
                return False
            return True
    
        if self.board_type == "Diamond":
            return abs(r - center) + abs(c - center) <= center

        if self.board_type == "Hexagon":
            return abs(r - center) + abs(c - center) <= center + 1

        return True

    def initialize_board(self):
        self.board = [[None] * self.size for _ in range(self.size)]

        for r in range(self.size):
            for c in range(self.size):
                if self.is_valid_position(r, c):
                    self.board[r][c] = 1

        center = self.size // 2
        if self.is_valid_position(center, center):
            self.board[center][center] = 0

    def make_move(self, r1, c1, r2, c2):
        if not self.is_valid_position(r1, c1) or not self.is_valid_position(r2, c2):
            return False

        if not (0 <= r1 < self.size and 0 <= c1 < self.size and 0 <= r2 < self.size and 0 <= c2 < self.size):
            return False

        rm = (r1 + r2) // 2
        cm = (c1 + c2) // 2

        # Horizontal or vertical jump by exactly 2
        if not ((abs(r1 - r2) == 2 and c1 == c2) or (abs(c1 - c2) == 2 and r1 == r2)):
            return False

        if self.board[r1][c1] == 1 and self.board[rm][cm] == 1 and self.board[r2][c2] == 0:
            self.board[r1][c1] = 0
            self.board[rm][cm] = 0
            self.board[r2][c2] = 1
            return True

        return False

    def get_valid_moves(self):
        moves = []
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]

        for r in range(self.size):
            for c in range(self.size):
                if not self.is_valid_position(r, c):
                    continue
                if self.board[r][c] != 1:
                    continue

                for dr, dc in directions:
                    r2 = r + dr
                    c2 = c + dc

                    if self.make_move_preview(r, c, r2, c2):
                        moves.append((r, c, r2, c2))

        return moves

    def make_move_preview(self, r1, c1, r2, c2):
        if not self.is_valid_position(r1, c1) or not self.is_valid_position(r2, c2):
            return False

        if not (0 <= r2 < self.size and 0 <= c2 < self.size):
            return False

        rm = (r1 + r2) // 2
        cm = (c1 + c2) // 2

        if not ((abs(r1 - r2) == 2 and c1 == c2) or (abs(c1 - c2) == 2 and r1 == r2)):
            return False

        return self.board[r1][c1] == 1 and self.board[rm][cm] == 1 and self.board[r2][c2] == 0

    def is_game_over(self):
        return len(self.get_valid_moves()) == 0

    def peg_count(self):
        count = 0
        for row in self.board:
            for cell in row:
                if cell == 1:
                    count += 1
        return count


class ManualPegSolitaireGame(PegSolitaireGame):
    def randomize_board(self, steps=5):
        """
        Randomize by making a few random valid moves from the current state.
        This keeps the board in a reachable/valid configuration.
        """
        for _ in range(steps):
            moves = self.get_valid_moves()
            if not moves:
                break
            r1, c1, r2, c2 = random.choice(moves)
            self.make_move(r1, c1, r2, c2)


class AutomatedPegSolitaireGame(PegSolitaireGame):
    def auto_move(self):
        moves = self.get_valid_moves()
        if not moves:
            return False

        r1, c1, r2, c2 = random.choice(moves)
        return self.make_move(r1, c1, r2, c2)