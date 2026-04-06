import tkinter as tk
from tkinter import ttk, messagebox
from game_logic import ManualPegSolitaireGame, AutomatedPegSolitaireGame


def main():
    root = tk.Tk()
    root.title("Peg Solitaire Game")
    root.geometry("750x650")

    title = ttk.Label(root, text="Peg Solitaire", font=("Segoe UI", 16))
    title.pack(pady=10)

    top_frame = ttk.Frame(root)
    top_frame.pack()

    board_var = tk.StringVar(value="English")
    size_var = tk.IntVar(value=7)
    mode_var = tk.StringVar(value="Manual")

    board_type_frame = ttk.LabelFrame(top_frame, text="Board Type")
    board_type_frame.grid(row=0, column=0, padx=20)

    ttk.Radiobutton(board_type_frame, text="English", variable=board_var, value="English").pack(anchor="w")
    ttk.Radiobutton(board_type_frame, text="Hexagon", variable=board_var, value="Hexagon").pack(anchor="w")
    ttk.Radiobutton(board_type_frame, text="Diamond", variable=board_var, value="Diamond").pack(anchor="w")

    mode_frame = ttk.LabelFrame(top_frame, text="Game Mode")
    mode_frame.grid(row=0, column=1, padx=20)

    ttk.Radiobutton(mode_frame, text="Manual", variable=mode_var, value="Manual").pack(anchor="w")
    ttk.Radiobutton(mode_frame, text="Automated", variable=mode_var, value="Automated").pack(anchor="w")

    size_frame = ttk.Frame(top_frame)
    size_frame.grid(row=0, column=2, padx=20)

    ttk.Label(size_frame, text="Board size").pack(side="left")
    ttk.Entry(size_frame, textvariable=size_var, width=5).pack(side="left")

    board_frame = ttk.Frame(root)
    board_frame.pack(pady=20)

    status_var = tk.StringVar(value="Welcome to Peg Solitaire")
    ttk.Label(root, textvariable=status_var).pack(pady=5)

    game = None
    buttons = []
    selected = [None, None]
    autoplay_job = [None]

    def create_game():
        size = size_var.get()
        board_type = board_var.get()
        mode = mode_var.get()

        if mode == "Manual":
            return ManualPegSolitaireGame(size=size, board_type=board_type)
        return AutomatedPegSolitaireGame(size=size, board_type=board_type)

    def clear_selection():
        if selected[0] is not None and buttons[selected[0]][selected[1]] is not None:
            buttons[selected[0]][selected[1]].config(bg=root.cget("bg"))
        selected[0] = None
        selected[1] = None

    def click_cell(r, c):
        nonlocal game

        if mode_var.get() != "Manual":
            messagebox.showinfo("Automated Mode", "Manual clicking is disabled in automated mode.")
            return

        if game.board[r][c] is None:
            return

        if game.board[r][c] == 1 and selected[0] is None:
            selected[0] = r
            selected[1] = c
            buttons[r][c].config(bg="yellow")
            return

        if selected[0] is not None:
            r1, c1 = selected
            success = game.make_move(r1, c1, r, c)
            clear_selection()

            if success:
                draw_board()
                check_game_over()

    def draw_board():
        for r in range(game.size):
            for c in range(game.size):
                btn = buttons[r][c]
                if btn is None:
                    continue

                cell = game.board[r][c]
                if cell == 1:
                    btn.config(text="●", state="normal")
                elif cell == 0:
                    btn.config(text="", state="normal")
                else:
                    btn.config(text="", state="disabled")

        status_var.set(
            f"Mode: {mode_var.get()} | Board: {board_var.get()} | Size: {game.size} | Pegs left: {game.peg_count()}"
        )

    def build_board():
        for widget in board_frame.winfo_children():
            widget.destroy()

        buttons.clear()

        for r in range(game.size):
            row = []
            for c in range(game.size):
                if not game.is_valid_position(r, c):
                    label = tk.Label(board_frame, text=" ", width=4)
                    label.grid(row=r, column=c, padx=1, pady=1)
                    row.append(None)
                else:
                    btn = tk.Button(
                        board_frame,
                        width=4,
                        command=lambda r=r, c=c: click_cell(r, c)
                    )
                    btn.grid(row=r, column=c, padx=1, pady=1)
                    row.append(btn)
            buttons.append(row)

    def check_game_over():
        if game.is_game_over():
            messagebox.showinfo("Game Over", f"No more valid moves!\nPegs remaining: {game.peg_count()}")
            stop_autoplay()

    def start_new_game():
        nonlocal game
        stop_autoplay()
        game = create_game()
        clear_selection()
        build_board()
        draw_board()

    def randomize_board():
        nonlocal game
        if mode_var.get() != "Manual":
            messagebox.showinfo("Randomize", "Randomize is only for manual mode.")
            return

        game.randomize_board(steps=5)
        draw_board()
        check_game_over()

    def autoplay_step():
        nonlocal game
        if not isinstance(game, AutomatedPegSolitaireGame):
            return

        moved = game.auto_move()
        draw_board()

        if not moved or game.is_game_over():
            check_game_over()
            autoplay_job[0] = None
            return

        autoplay_job[0] = root.after(500, autoplay_step)

    def autoplay():
        if mode_var.get() != "Automated":
            messagebox.showinfo("Autoplay", "Switch to Automated mode first.")
            return

        if autoplay_job[0] is None:
            autoplay_step()

    def stop_autoplay():
        if autoplay_job[0] is not None:
            root.after_cancel(autoplay_job[0])
            autoplay_job[0] = None

    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)

    ttk.Button(button_frame, text="New Game", command=start_new_game).grid(row=0, column=0, padx=5)
    ttk.Button(button_frame, text="Randomize", command=randomize_board).grid(row=0, column=1, padx=5)
    ttk.Button(button_frame, text="Autoplay", command=autoplay).grid(row=0, column=2, padx=5)
    ttk.Button(button_frame, text="Stop", command=stop_autoplay).grid(row=0, column=3, padx=5)

    game = create_game()
    build_board()
    draw_board()

    root.mainloop()


if __name__ == "__main__":
    main()