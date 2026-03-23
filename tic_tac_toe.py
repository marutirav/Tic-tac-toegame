

import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
 

class TicTacToe:
    """Tic Tac Toe game with Tkinter GUI"""
    
    def __init__(self, root):
        """Initialize the game"""
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f0f0")
        
        # Game state
        self.board = [" " for _ in range(9)]  # 3x3 board
        self.current_player = "X"  # X always starts
        self.game_over = False
        self.winning_cells = []  # To highlight winning combination
        
        # Color scheme for X and O
        self.colors = {
            "X": "#FF6B6B",  # Red for X
            "O": "#4ECDC4",  # Cyan for O
            "empty": "#FFFFFF"  # White for empty cells
        }
        
        # Set up the GUI
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Title label
        title_font = tkFont.Font(family="Helvetica", size=20, weight="bold")
        title_label = tk.Label(self.root, text="Tic Tac Toe", 
                              font=title_font, bg="#f0f0f0")
        title_label.pack(pady=10)
        
        # Status label showing whose turn it is
        self.status_font = tkFont.Font(family="Helvetica", size=14)
        self.status_label = tk.Label(self.root, text="Player X's Turn",
                                     font=self.status_font, bg="#f0f0f0")
        self.status_label.pack(pady=5)
        
        # Game board frame
        board_frame = tk.Frame(self.root, bg="#f0f0f0")
        board_frame.pack(pady=10)
        
        # Create 3x3 grid of buttons
        self.buttons = []
        button_font = tkFont.Font(family="Helvetica", size=18, weight="bold")
        
        for row in range(3):
            button_row = []
            for col in range(3):
                # Calculate button index (0-8)
                btn_index = row * 3 + col
                
                # Create button
                btn = tk.Button(board_frame, text="", width=6, height=3,
                               font=button_font,
                               bg=self.colors["empty"],
                               command=lambda idx=btn_index: self.on_click(idx),
                               relief=tk.RAISED, bd=2)
                btn.grid(row=row, column=col, padx=5, pady=5)
                button_row.append(btn)
            
            self.buttons.append(button_row)
        
        # Control buttons frame
        control_frame = tk.Frame(self.root, bg="#f0f0f0")
        control_frame.pack(pady=15)
        
        # Reset button
        reset_btn = tk.Button(control_frame, text="Reset Game", 
                             command=self.reset_game,
                             bg="#95E1D3", fg="black",
                             font=tkFont.Font(family="Helvetica", size=12),
                             padx=15, pady=10)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Quit button
        quit_btn = tk.Button(control_frame, text="Exit", 
                            command=self.root.quit,
                            bg="#F8B195", fg="black",
                            font=tkFont.Font(family="Helvetica", size=12),
                            padx=15, pady=10)
        quit_btn.pack(side=tk.LEFT, padx=5)
    
    def on_click(self, index):
        """Handle button click"""
        # Don't allow moves if game is over
        if self.game_over:
            messagebox.showinfo("Game Over", "Please reset the game to play again.")
            return
        
        # Calculate row and column from index
        row = index // 3
        col = index % 3
        
        # Check if cell is already filled
        if self.board[index] != " ":
            messagebox.showwarning("Invalid Move", "This cell is already taken!")
            return
        
        # Place the player's mark
        self.board[index] = self.current_player
        
        # Update the button display
        button = self.buttons[row][col]
        button.config(text=self.current_player,
                     fg=self.colors[self.current_player],
                     bg=self.colors["empty"],
                     state=tk.DISABLED)
        
        # Check for winner
        winner = self.check_winner()
        if winner:
            self.game_over = True
            self.highlight_winning_cells()
            messagebox.showinfo("Winner!", f"Player {winner} wins!")
            return
        
        # Check for draw
        if self.is_board_full():
            self.game_over = True
            messagebox.showinfo("Draw", "It's a draw!")
            return
        
        # Switch player
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_label.config(text=f"Player {self.current_player}'s Turn")
    
    def check_winner(self):
        """Check if there's a winner and store winning cells"""
        # Define all winning combinations (indices)
        winning_combinations = [
            # Rows
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            # Columns
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            # Diagonals
            [0, 4, 8],
            [2, 4, 6]
        ]
        
        # Check each winning combination
        for combo in winning_combinations:
            if (self.board[combo[0]] != " " and
                self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]):
                # Store winning cells for highlighting
                self.winning_cells = combo
                return self.board[combo[0]]
        
        return None
    
    def is_board_full(self):
        """Check if the board is full (draw condition)"""
        return " " not in self.board
    
    def highlight_winning_cells(self):
        """Highlight the winning combination"""
        for index in self.winning_cells:
            row = index // 3
            col = index % 3
            button = self.buttons[row][col]
            # Add a green background to winning cells
            button.config(bg="#90EE90")  # Light green
    
    def reset_game(self):
        """Reset the game to initial state"""
        # Reset game variables
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.game_over = False
        self.winning_cells = []
        
        # Reset all buttons
        for row in range(3):
            for col in range(3):
                button = self.buttons[row][col]
                button.config(text="", bg=self.colors["empty"], 
                            fg="black", state=tk.NORMAL)
        
        # Reset status label
        self.status_label.config(text="Player X's Turn")


def main():
    """Main function to run the game"""
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()


if __name__ == "__main__":
    main()


def check_winner(board, player):
    """Check if the current player has won"""
    # All possible winning combinations
    winning_combinations = [
        [0, 1, 2],  # Top row
        [3, 4, 5],  # Middle row
        [6, 7, 8],  # Bottom row
        [0, 3, 6],  # Left column
        [1, 4, 7],  # Middle column
        [2, 5, 8],  # Right column
        [0, 4, 8],  # Diagonal top-left to bottom-right
        [2, 4, 6],  # Diagonal top-right to bottom-left
    ]
    
    for combination in winning_combinations:
        if all(board[i] == player for i in combination):
            return True
    return False


def is_board_full(board):
    """Check if the board is completely filled (draw condition)"""
    return all(cell != " " for cell in board)


def play_game():
    """Main game loop"""
    # Initialize empty board
    board = [" " for _ in range(9)]
    current_player = "X"
    
    print("=" * 30)
    print("  WELCOME TO TIC TAC TOE!")
    print("=" * 30)
    print("\nPositions are numbered 1-9:")
    display_board(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
    
    # Game loop
    while True:
        display_board(board)
        
        # Get player's move
        position = get_player_move(board, current_player)
        make_move(board, position, current_player)
        
        # Check if current player won
        if check_winner(board, current_player):
            display_board(board)
            print(f"🎉 Player {current_player} wins! Congratulations!")
            break
        
        # Check if it's a draw
        if is_board_full(board):
            display_board(board)
            print("🤝 It's a draw! Good game!")
            break
        
        # Switch to other player
        current_player = "O" if current_player == "X" else "X"
    
    # Ask if players want to play again
    while True:
        play_again = input("\nDo you want to play again? (yes/no): ").lower()
        if play_again in ["yes", "y"]:
            play_game()
            break
        elif play_again in ["no", "n"]:
            print("Thanks for playing! Goodbye!")
            break
        else:
            print("Invalid input! Please enter 'yes' or 'no'.")


if __name__ == "__main__":
    play_game()
