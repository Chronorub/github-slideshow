import tkinter as tk
from tkinter import messagebox


class ReversiApp:
    EMPTY = 0
    BLACK = 1
    WHITE = 2

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Reversi (Adjustable Size)")

        self.size_var = tk.StringVar(value="8")
        self.turn = self.BLACK
        self.board = []
        self.buttons = []

        self._build_ui()
        self.new_game()

    def _build_ui(self):
        top = tk.Frame(self.root, padx=8, pady=8)
        top.pack(fill="x")

        tk.Label(top, text="Board size (even, >=4):").pack(side="left")
        tk.Entry(top, textvariable=self.size_var, width=5).pack(side="left", padx=(6, 10))
        tk.Button(top, text="New Game", command=self.new_game).pack(side="left")

        self.status_label = tk.Label(top, text="", anchor="w")
        self.status_label.pack(side="left", padx=10)

        self.grid_frame = tk.Frame(self.root, padx=8, pady=8)
        self.grid_frame.pack()

    def new_game(self):
        try:
            size = int(self.size_var.get())
        except ValueError:
            messagebox.showerror("Invalid size", "Board size must be a number.")
            return

        if size < 4 or size % 2 != 0:
            messagebox.showerror("Invalid size", "Board size must be an even number >= 4.")
            return

        self.size = size
        self.turn = self.BLACK
        self.board = [[self.EMPTY for _ in range(self.size)] for _ in range(self.size)]

        mid = self.size // 2
        self.board[mid - 1][mid - 1] = self.WHITE
        self.board[mid][mid] = self.WHITE
        self.board[mid - 1][mid] = self.BLACK
        self.board[mid][mid - 1] = self.BLACK

        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.buttons = []
        for r in range(self.size):
            row_buttons = []
            for c in range(self.size):
                btn = tk.Button(
                    self.grid_frame,
                    width=3,
                    height=1,
                    font=("Arial", 12, "bold"),
                    bg="#0b7d2b",
                    activebackground="#0e8f33",
                    command=lambda rr=r, cc=c: self.play_move(rr, cc),
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        self.refresh_board()

    def refresh_board(self):
        for r in range(self.size):
            for c in range(self.size):
                cell = self.board[r][c]
                if cell == self.BLACK:
                    text, fg = "●", "black"
                elif cell == self.WHITE:
                    text, fg = "●", "white"
                else:
                    text, fg = "", "black"
                self.buttons[r][c].config(text=text, fg=fg)

        black_count, white_count = self.score()
        current = "Black" if self.turn == self.BLACK else "White"
        self.status_label.config(text=f"Turn: {current}   Black: {black_count}  White: {white_count}")

    def in_bounds(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size

    def opponent(self, player):
        return self.WHITE if player == self.BLACK else self.BLACK

    def flippable_in_direction(self, r, c, dr, dc, player):
        flips = []
        rr, cc = r + dr, c + dc
        opp = self.opponent(player)

        while self.in_bounds(rr, cc) and self.board[rr][cc] == opp:
            flips.append((rr, cc))
            rr += dr
            cc += dc

        if self.in_bounds(rr, cc) and self.board[rr][cc] == player and flips:
            return flips
        return []

    def valid_moves(self, player):
        moves = {}
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] != self.EMPTY:
                    continue
                all_flips = []
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        all_flips.extend(self.flippable_in_direction(r, c, dr, dc, player))
                if all_flips:
                    moves[(r, c)] = all_flips
        return moves

    def play_move(self, r, c):
        moves = self.valid_moves(self.turn)
        if (r, c) not in moves:
            return

        self.board[r][c] = self.turn
        for rr, cc in moves[(r, c)]:
            self.board[rr][cc] = self.turn

        self.turn = self.opponent(self.turn)
        next_moves = self.valid_moves(self.turn)

        if not next_moves:
            # Opponent passes if no move available.
            self.turn = self.opponent(self.turn)
            if not self.valid_moves(self.turn):
                self.finish_game()
                return
            messagebox.showinfo("Pass", f"{('Black' if self.opponent(self.turn) == self.BLACK else 'White')} has no valid moves and must pass.")

        self.refresh_board()

    def score(self):
        black = sum(cell == self.BLACK for row in self.board for cell in row)
        white = sum(cell == self.WHITE for row in self.board for cell in row)
        return black, white

    def finish_game(self):
        self.refresh_board()
        black, white = self.score()
        if black > white:
            winner = "Black wins!"
        elif white > black:
            winner = "White wins!"
        else:
            winner = "It's a draw!"
        messagebox.showinfo("Game Over", f"Black: {black}\nWhite: {white}\n\n{winner}")


def main():
    root = tk.Tk()
    ReversiApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
