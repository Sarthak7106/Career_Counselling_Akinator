import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
from PIL import Image, ImageTk

class TicTacToeGame:
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete
        self.board = ['' for _ in range(9)]
        self.current_player = 'X'  # Player is X, AI is O
        self.game_over = False
        
        self.game_frame = tk.Frame(self.root, bg='#ffffff', padx=20, pady=20)
        self.game_frame.configure(highlightbackground='#4a90e2', highlightthickness=2)
        self.game_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        self.title_label = tk.Label(
            self.game_frame,
            text="Tic Tac Toe Challenge!\nCan you beat the AI?",
            font=("Helvetica", 16, "bold"),
            bg='#ffffff',
            fg='#4a90e2'
        )
        self.title_label.pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.game_frame,
            orient="horizontal",
            length=200,
            mode="determinate"
        )
        self.progress.pack(pady=5)
        self.progress["value"] = 33  # First game out of three
        
        # Game board
        self.board_frame = tk.Frame(self.game_frame, bg='#ffffff')
        self.board_frame.pack(pady=10)
        
        self.buttons = []
        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    self.board_frame,
                    text='',
                    font=("Helvetica", 20, "bold"),
                    width=3,
                    height=1,
                    bg='white',
                    command=lambda row=i, col=j: self.make_move(row * 3 + col)
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                self.buttons.append(btn)
        
        # Status label
        self.status_label = tk.Label(
            self.game_frame,
            text="Your turn! (X)",
            font=("Helvetica", 12),
            bg='#ffffff',
            fg='#333333'
        )
        self.status_label.pack(pady=10)

    def make_move(self, position):
        if self.board[position] == '' and not self.game_over:
            # Player's move
            self.board[position] = self.current_player
            self.buttons[position].config(text=self.current_player, fg='#4a90e2')
            
            if self.check_winner():
                self.show_result("Congratulations! You won!", "win")
                return
            
            if self.is_board_full():
                self.show_result("It's a draw!", "tie")
                return
            
            # AI's move
            self.status_label.config(text="AI is thinking...")
            self.root.update()
            self.root.after(500, self.ai_move)

    def ai_move(self):
        if self.game_over:
            return
            
        best_score = float('-inf')
        best_move = None
        
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'O'
                score = self.minimax(self.board, 0, False)
                self.board[i] = ''
                
                if score > best_score:
                    best_score = score
                    best_move = i
        
        if best_move is not None:
            self.board[best_move] = 'O'
            self.buttons[best_move].config(text='O', fg='#ff4757')
            
            if self.check_winner_board(self.board, 'O'):
                self.show_result("AI wins! Better luck next time!", "loss")
                return
            
            if self.is_board_full():
                self.show_result("It's a draw!", "tie")
                return
            
            self.status_label.config(text="Your turn! (X)")

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner_board(board, 'O'):
            return 1
        if self.check_winner_board(board, 'X'):
            return -1
        if self.is_board_full():
            return 0
            
        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'O'
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ''
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'X'
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ''
                    best_score = min(score, best_score)
            return best_score

    def check_winner_board(self, board, player):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        
        for combo in winning_combinations:
            if all(board[i] == player for i in combo):
                return True
        return False

    def check_winner(self):
        return self.check_winner_board(self.board, self.current_player)

    def is_board_full(self):
        return '' not in self.board

    def show_result(self, message, result):
        self.game_over = True
        self.status_label.config(text=message)
        
        # Highlight winning combination if there is one
        if self.check_winner():
            winning_combinations = [
                [0, 1, 2], [3, 4, 5], [6, 7, 8],
                [0, 3, 6], [1, 4, 7], [2, 5, 8],
                [0, 4, 8], [2, 4, 6]
            ]
            
            for combo in winning_combinations:
                if all(self.board[i] == self.current_player for i in combo):
                    for pos in combo:
                        self.buttons[pos].config(bg='#a8e6cf')
        
        # Create frame for buttons
        button_frame = tk.Frame(self.game_frame, bg='#ffffff')
        button_frame.pack(pady=10)
        
        # Play Again button
        play_again_btn = tk.Button(
            button_frame,
            text="Play Again",
            font=("Helvetica", 12, "bold"),
            bg='#4a90e2',
            fg='white',
            command=self.reset_game
        )
        play_again_btn.pack(side=tk.LEFT, padx=5)
        
        # Next button
        next_btn = tk.Button(
            button_frame,
            text="Next",
            font=("Helvetica", 12, "bold"),
            bg='#4a90e2',
            fg='white',
            command=lambda: self.complete_game(result)
        )
        next_btn.pack(side=tk.LEFT, padx=5)

    def reset_game(self):
        # Clear the board
        self.board = ['' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        
        # Reset all buttons
        for button in self.buttons:
            button.config(text='', bg='white', fg='black')
        
        # Reset status
        self.status_label.config(text="Your turn! (X)")
        
        # Remove result buttons if they exist
        for widget in self.game_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget != self.board_frame:
                widget.destroy()

    def complete_game(self, result):
        self.cleanup()
        self.on_complete({"tictactoe_result": result})

    def cleanup(self):
        if hasattr(self, 'game_frame'):
            self.game_frame.destroy()

class ReactionTimeGame:
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete
        self.start_time = None
        self.active = True
        
        self.game_frame = tk.Frame(self.root, bg='#ffffff', padx=20, pady=20)
        self.game_frame.configure(highlightbackground='#4a90e2', highlightthickness=2)
        self.game_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.game_frame,
            orient="horizontal",
            length=200,
            mode="determinate"
        )
        self.progress.pack(pady=5)
        self.progress["value"] = 66  # Second game out of three
        
        self.instruction_label = tk.Label(
            self.game_frame,
            text="Wait for the green screen, then click!",
            font=("Helvetica", 14),
            bg='#ffffff',
            fg='#333333'
        )
        self.instruction_label.pack(pady=10)
        
        self.color_frame = tk.Frame(self.game_frame, width=200, height=200, bg="red")
        self.color_frame.pack(pady=10)
        self.color_frame.bind("<Button-1>", self.check_reaction)

        self.flash_green()

    def flash_green(self):
        if not self.active:
            return
        wait_time = random.randint(2000, 5000)
        self.timer_id = self.root.after(wait_time, self.change_to_green)

    def change_to_green(self):
        if not self.active:
            return
        try:
            self.color_frame.config(bg="green")
            self.start_time = time.time()
        except tk.TclError:
            return  # Frame was destroyed, exit silently

    def check_reaction(self, event):
        if not self.active:
            return
        try:
            if self.color_frame.cget("bg") == "green":
                reaction_time = time.time() - self.start_time
                self.show_result(reaction_time)
            else:
                self.show_result(None)
        except tk.TclError:
            return  # Frame was destroyed, exit silently

    def show_result(self, reaction_time):
        if not self.active:
            return
        
        # Clear existing widgets
        for widget in self.game_frame.winfo_children():
            widget.destroy()
            
        result_text = (
            f"Your reaction time was: {reaction_time:.2f} seconds!"
            if reaction_time is not None
            else "You clicked too early! Try again!"
        )
        
        result_label = tk.Label(
            self.game_frame,
            text=result_text,
            font=("Helvetica", 14, "bold"),
            bg='#ffffff',
            fg='#333333'
        )
        result_label.pack(pady=20)
        
        button_frame = tk.Frame(self.game_frame, bg='#ffffff')
        button_frame.pack(pady=10)
        
        # Play Again button
        play_again_btn = tk.Button(
            button_frame,
            text="Play Again",
            font=("Helvetica", 12, "bold"),
            bg='#4a90e2',
            fg='white',
            command=self.reset_game
        )
        play_again_btn.pack(side=tk.LEFT, padx=5)
        
        # Next button
        next_btn = tk.Button(
            button_frame,
            text="Next",
            font=("Helvetica", 12, "bold"),
            bg='#4a90e2',
            fg='white',
            command=lambda: self.complete_game(reaction_time)
        )
        next_btn.pack(side=tk.LEFT, padx=5)

    def reset_game(self):
        if not self.active:
            return
        self.__init__(self.root, self.on_complete)

    def complete_game(self, reaction_time):
        self.active = False
        self.on_complete({"reaction_time": reaction_time})

    def cleanup(self):
        self.active = False
        if hasattr(self, 'timer_id'):
            self.root.after_cancel(self.timer_id)
        if hasattr(self, 'game_frame'):
            self.game_frame.destroy()

class MathPuzzleGame:
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete
        self.questions = [
            {"question": "What is 8 x 7?", "answer": "56"},
            {"question": "What is 15 + 23?", "answer": "38"},
            {"question": "What is 12 x 6?", "answer": "72"},
            {"question": "What is 81 ÷ 9?", "answer": "9"},
            {"question": "What is 7 x 5?", "answer": "35"},
        ]
        self.current_question = random.choice(self.questions)
        
        self.game_frame = tk.Frame(self.root, bg='#ffffff', padx=20, pady=20)
        self.game_frame.configure(highlightbackground='#4a90e2', highlightthickness=2)
        self.game_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.instruction_label = tk.Label(
            self.game_frame,
            text=f"Solve the puzzle:\n{self.current_question['question']}",
            font=("Helvetica", 14),
            bg='#ffffff',
            fg='#333333'
        )
        self.instruction_label.pack(pady=10)

        self.answer_entry = tk.Entry(
            self.game_frame,
            font=("Helvetica", 12),
            justify='center'
        )
        self.answer_entry.pack(pady=5)
        self.answer_entry.focus()

        self.submit_button = self.create_styled_button(
            self.game_frame,
            "Submit Answer",
            self.check_answer
        )
        self.submit_button.pack(pady=5)

    def create_styled_button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            font=("Helvetica", 12, "bold"),
            bg='#4a90e2',
            fg='white',
            activebackground='#357abd',
            activeforeground='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=command
        )
        btn.bind('<Enter>', lambda e: btn.configure(bg='#357abd'))
        btn.bind('<Leave>', lambda e: btn.configure(bg='#4a90e2'))
        return btn

    def check_answer(self):
        if not hasattr(self, 'answer_entry'):
            return
        answer = self.answer_entry.get()
        is_correct = answer == self.current_question["answer"]
        if is_correct:
            messagebox.showinfo("Correct!", "Well done! That's the correct answer.")
        else:
            messagebox.showerror("Incorrect", "Oops! That's not the right answer.")
        self.on_complete({"puzzle_correct": is_correct})

    def cleanup(self):
        if hasattr(self, 'game_frame'):
            self.game_frame.destroy()

class CareerCounselorGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Career Counselor Game")
        self.root.geometry("800x600")
        
        try:
            bg_image = Image.open("game.png")
            bg_image = bg_image.resize((800, 600), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(relwidth=1, relheight=1)
        except:
            self.root.configure(bg='#1a1a2e')
            
        self.questions = self.get_question_tree()
        self.current_node = self.questions
        self.game_results = {}
        self.show_welcome_screen()

    def create_styled_frame(self):
        frame = tk.Frame(self.root, bg='#ffffff', padx=20, pady=20)
        frame.configure(highlightbackground='#4a90e2', highlightthickness=2)
        return frame

    def create_styled_button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            font=("Helvetica", 12, "bold"),
            bg='#4a90e2',
            fg='white',
            activebackground='#357abd',
            activeforeground='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=command
        )
        btn.bind('<Enter>', lambda e: btn.configure(bg='#357abd'))
        btn.bind('<Leave>', lambda e: btn.configure(bg='#4a90e2'))
        return btn

    def show_welcome_screen(self):
        self.welcome_frame = self.create_styled_frame()
        self.welcome_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        title_frame = tk.Frame(self.welcome_frame, bg='#ffffff')
        title_frame.pack(pady=(0, 20))
        
        title = tk.Label(
            title_frame,
            text="Career Counselor",
            font=("Helvetica", 32, "bold"),
            fg='#4a90e2',
            bg='#ffffff'
        )
        title.pack()
        
        welcome_text = """Welcome to the Career Counselor Game!
        
Discover your ideal career path through an interactive journey of questions and mini-games. Your choices and performance will help determine the perfect career match for you.

Click 'Start' to begin your career discovery adventure!"""
        
        welcome_label = tk.Label(
            self.welcome_frame,
            text=welcome_text,
            font=("Helvetica", 12),
            wraplength=400,
            justify="center",
            bg='#ffffff',
            fg='#333333'
        )
        welcome_label.pack(pady=20)
        
        start_button = self.create_styled_button(
            self.welcome_frame,
            "Start Journey",
            self.start_game
        )
        start_button.pack(pady=10)

    def setup_ui(self):
        if hasattr(self, 'main_frame'):
            self.main_frame.destroy()
            
        self.main_frame = self.create_styled_frame()
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        self.question_label = tk.Label(
            self.main_frame,
            text="",
            font=("Helvetica", 14, "bold"),
            wraplength=400,
            justify="center",
            bg='#ffffff',
            fg='#333333'
        )
        self.question_label.pack(pady=20)
        
        self.options_frame = tk.Frame(self.main_frame, bg='#ffffff')
        self.options_frame.pack(pady=10)
        
        self.display_question()

    def get_question_tree(self):
        return {
            "question": "Which of these areas do you enjoy the most?",
            "options": {
                "Analytical & Research": {
                    "question": "Do you enjoy analyzing patterns or trends in data?",
                    "options": {
                        "Yes": "Data Scientist",
                        "No": {
                            "question": "Do you enjoy researching new ideas or conducting experiments?",
                            "options": {
                                "Yes": "Research Scientist",
                                "No": "Economist",
                            },
                        },
                    },
                },
                "Creative & Design": {
                    "question": "Do you enjoy creating visual art or designs?",
                    "options": {
                        "Yes": "Graphic Designer",
                        "No": {
                            "question": "Do you enjoy storytelling or filmmaking?",
                            "options": {
                                "Yes": "Film Director",
                                "No": "Writer",
                            },
                        },
                    },
                },
            },
        }

    def display_question(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        if isinstance(self.current_node, str):
            self.show_result(self.current_node)
            return

        self.question_label.config(text=self.current_node["question"])
        
        for option in self.current_node["options"]:
            button = self.create_styled_button(
                self.options_frame,
                option,
                lambda opt=option: self.next_question(opt)
            )
            button.pack(pady=5, fill="x")

        if random.choice([True, False]) and not hasattr(self, "mini_game_instance"):
            self.root.after(100, self.insert_mini_game)

    def show_result(self, career):
        if hasattr(self, 'main_frame'):
            self.main_frame.destroy()
                
        result_frame = self.create_styled_frame()
        result_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        reaction_time = self.game_results.get("reaction_time", None)
        puzzle_correct = self.game_results.get("puzzle_correct", None)
        tictactoe_result = self.game_results.get("tictactoe_result", None)

        # Modify career recommendation based on game results
        career_notes = []
        
        if reaction_time and reaction_time < 0.5:
            career_notes.append("excellent reaction skills")
        if puzzle_correct is not None and not puzzle_correct:
            career_notes.append("could improve problem-solving skills")
        if tictactoe_result == "win":
            career_notes.append("strong strategic thinking")
        elif tictactoe_result == "loss":
            career_notes.append("keep developing strategic planning")

        if career_notes:
            career = f"{career}\n(" + ", ".join(career_notes) + ")"

        result_label = tk.Label(
            result_frame,
            text="Your Career Match",
            font=("Helvetica", 24, "bold"),
            bg='#ffffff',
            fg='#4a90e2'
        )
        result_label.pack(pady=(0, 20))
        
        career_label = tk.Label(
            result_frame,
            text=career,
            font=("Helvetica", 18),
            bg='#ffffff',
            fg='#333333',
            wraplength=400,
            justify="center"
        )
        career_label.pack(pady=20)
        
        close_button = self.create_styled_button(
            result_frame,
            "Close",
            self.root.destroy
        )
        close_button.pack(pady=10)

    def start_game(self):
        if hasattr(self, 'welcome_frame'):
            self.welcome_frame.destroy()
        self.setup_ui()

    def next_question(self, option):
        self.current_node = self.current_node["options"][option]
        self.display_question()

    def insert_mini_game(self):
        if hasattr(self, 'main_frame'):
            self.main_frame.destroy()
        game_class = random.choice([ReactionTimeGame, MathPuzzleGame, TicTacToeGame])
        self.mini_game_instance = game_class(self.root, self.capture_game_result)

    def capture_game_result(self, result):
        self.game_results.update(result)
        if hasattr(self, 'mini_game_instance'):
            self.mini_game_instance.cleanup()
            del self.mini_game_instance
        self.setup_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = CareerCounselorGame(root)
    root.mainloop()