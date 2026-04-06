import unittest
from game_logic import ManualPegSolitaireGame, AutomatedPegSolitaireGame


class TestPegSolitaireGame(unittest.TestCase):

    def test_board_initialization(self):
        game = ManualPegSolitaireGame(size=7, board_type="English")
        center = game.size // 2

        self.assertEqual(game.board[center][center], 0)

        peg_count = game.peg_count()
        self.assertGreater(peg_count, 0)

    def test_valid_move(self):
        game = ManualPegSolitaireGame(size=7, board_type="English")
        center = game.size // 2

        r1, c1 = center, center - 2
        r2, c2 = center, center

        result = game.make_move(r1, c1, r2, c2)

        self.assertTrue(result)
        self.assertEqual(game.board[r1][c1], 0)
        self.assertEqual(game.board[center][center - 1], 0)
        self.assertEqual(game.board[r2][c2], 1)

    def test_game_over(self):
        game = ManualPegSolitaireGame(size=7, board_type="English")
        game.board = [[None] * game.size for _ in range(game.size)]

        for r in range(game.size):
            for c in range(game.size):
                if game.is_valid_position(r, c):
                    game.board[r][c] = 0

        game.board[3][3] = 1
        self.assertTrue(game.is_game_over())

    def test_get_valid_moves_initial_board(self):
        game = ManualPegSolitaireGame(size=7, board_type="English")
        moves = game.get_valid_moves()
        self.assertGreater(len(moves), 0)

    def test_randomize_board_changes_state(self):
        game = ManualPegSolitaireGame(size=7, board_type="English")
        before = [row[:] for row in game.board]

        game.randomize_board(steps=3)
        after = game.board

        self.assertNotEqual(before, after)

    def test_automated_move(self):
        game = AutomatedPegSolitaireGame(size=7, board_type="English")
        before_pegs = game.peg_count()

        moved = game.auto_move()

        self.assertTrue(moved)
        self.assertEqual(game.peg_count(), before_pegs - 1)


if __name__ == "__main__":
    unittest.main()