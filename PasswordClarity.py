import tkinter as tk
from tkinter import font as tkfont
import re
import math


class PasswordVisualizer:
    def __init__(self, master):
        self.master = master
        master.title("Password Clarity")
        master.geometry("600x350")
        master.resizable(False, False)

        # Configure fonts
        self.title_font = tkfont.Font(family="DejaVu Sans", size=14)
        self.input_font = tkfont.Font(family="Monospace", size=18)
        self.display_font = tkfont.Font(family="Monospace", size=24)
        self.stats_font = tkfont.Font(family="DejaVu Sans", size=12)
        self.count_font = tkfont.Font(family="DejaVu Sans", size=12, weight="bold")

        # Colors for character types
        self.colors = {
            'capital': "#00AA00",  # Green
            'lower': "#0000AA",  # Blue
            'number': "#AA0000",  # Red
            'symbol': "#000000"  # Black
        }

        # Create frames for layout
        self.main_frame = tk.Frame(master, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        self.title_label = tk.Label(
            self.main_frame,
            text="Enter password to clarify:",
            font=self.title_font
        )
        self.title_label.pack(anchor=tk.W, pady=(0, 10))

        # Input box
        self.input_var = tk.StringVar()
        self.input_var.trace_add("write", self.update_display)
        self.input_box = tk.Entry(
            self.main_frame,
            textvariable=self.input_var,
            font=self.input_font,
            width=40
        )
        self.input_box.pack(fill=tk.X, pady=(0, 10))

        # Password display (using Canvas with text items for colored characters)
        self.display_frame = tk.Frame(self.main_frame, height=80)
        self.display_frame.pack(fill=tk.X, pady=10)
        self.display_frame.pack_propagate(False)

        self.display_canvas = tk.Canvas(self.display_frame, bg="white")
        self.display_canvas.pack(fill=tk.BOTH, expand=True)

        # Strength score
        self.strength_frame = tk.Frame(self.main_frame)
        self.strength_frame.pack(fill=tk.X, pady=(0, 10))

        self.strength_label = tk.Label(
            self.strength_frame,
            text="Strength: 0/100",
            font=self.count_font,
            fg="#AA0000"  # Default to red
        )
        self.strength_label.pack(side=tk.RIGHT)

        # Character counts
        self.counts_frame = tk.Frame(self.main_frame)
        self.counts_frame.pack(pady=(0, 20))

        # Capital count
        tk.Label(
            self.counts_frame,
            text="Capital:",
            font=self.stats_font,
            fg=self.colors['capital']
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.capital_count = tk.Label(
            self.counts_frame,
            text="0",
            font=self.count_font,
            fg=self.colors['capital']
        )
        self.capital_count.pack(side=tk.LEFT, padx=(0, 15))

        # Lowercase count
        tk.Label(
            self.counts_frame,
            text="Lower:",
            font=self.stats_font,
            fg=self.colors['lower']
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.lower_count = tk.Label(
            self.counts_frame,
            text="0",
            font=self.count_font,
            fg=self.colors['lower']
        )
        self.lower_count.pack(side=tk.LEFT, padx=(0, 15))

        # Number count
        tk.Label(
            self.counts_frame,
            text="Number:",
            font=self.stats_font,
            fg=self.colors['number']
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.number_count = tk.Label(
            self.counts_frame,
            text="0",
            font=self.count_font,
            fg=self.colors['number']
        )
        self.number_count.pack(side=tk.LEFT, padx=(0, 15))

        # Symbol count
        tk.Label(
            self.counts_frame,
            text="Symbol:",
            font=self.stats_font,
            fg=self.colors['symbol']
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.symbol_count = tk.Label(
            self.counts_frame,
            text="0",
            font=self.count_font,
            fg=self.colors['symbol']
        )
        self.symbol_count.pack(side=tk.LEFT)

        # OK button
        self.ok_button = tk.Button(
            self.main_frame,
            text="OK",
            command=self.on_ok,
            width=10,
            height=2,
            font=self.title_font
        )
        self.ok_button.pack()

        # Handle Enter key
        self.input_box.bind("<Return>", lambda event: self.on_ok())

        # Set focus to input box
        self.input_box.focus_set()

        # Result variable
        self.result = None

    def get_password_strength(self, password):
        """Calculate password strength and character counts"""
        if not password:
            return {
                'score': 0,
                'capitals': 0,
                'lowers': 0,
                'numbers': 0,
                'symbols': 0
            }

        # Count character types
        capitals = len(re.findall(r'[A-Z]', password))
        lowers = len(re.findall(r'[a-z]', password))
        numbers = len(re.findall(r'\d', password))
        symbols = len(re.findall(r'[^A-Za-z0-9]', password))
        length = len(password)

        # Basic scoring algorithm
        score = 0

        # Length points (up to 40 points)
        score += min(length * 4, 40)

        # Character type points
        if capitals > 0:
            score += min(capitals * 2, 10)
        if lowers > 0:
            score += min(lowers * 2, 10)
        if numbers > 0:
            score += min(numbers * 2, 10)
        if symbols > 0:
            score += min(symbols * 3, 15)

        # Bonus for mixture of character types (up to 15 points)
        types_used = 0
        if capitals > 0:
            types_used += 1
        if lowers > 0:
            types_used += 1
        if numbers > 0:
            types_used += 1
        if symbols > 0:
            types_used += 1
        score += types_used * 5

        return {
            'score': min(score, 100),
            'capitals': capitals,
            'lowers': lowers,
            'numbers': numbers,
            'symbols': symbols
        }

    def update_display(self, *args):
        """Update the display when the password changes"""
        # Clear the canvas
        self.display_canvas.delete("all")

        password = self.input_var.get()

        # Calculate password strength and counts
        strength = self.get_password_strength(password)

        # Update character counts
        self.capital_count.config(text=str(strength['capitals']))
        self.lower_count.config(text=str(strength['lowers']))
        self.number_count.config(text=str(strength['numbers']))
        self.symbol_count.config(text=str(strength['symbols']))

        # Update strength score with color
        score = strength['score']
        self.strength_label.config(text=f"Strength: {score}/100")

        # Set strength score color
        if score < 40:
            self.strength_label.config(fg="#AA0000")  # Red
        elif score < 70:
            self.strength_label.config(fg="#AA6600")  # Orange
        else:
            self.strength_label.config(fg="#00AA00")  # Green

        # Calculate display metrics
        if not password:
            return

        # Display the password with color coding
        canvas_width = self.display_canvas.winfo_width()
        if canvas_width < 10:  # Not yet properly sized
            self.master.update_idletasks()
            canvas_width = self.display_canvas.winfo_width()

        char_width = self.display_font.measure('M')  # Monospace character width
        total_width = char_width * len(password)

        # Center position
        start_x = (canvas_width - total_width) / 2
        if start_x < 0:
            start_x = 10

        # Draw each character with appropriate color
        for i, char in enumerate(password):
            if re.match(r'[A-Z]', char):
                color = self.colors['capital']
            elif re.match(r'[a-z]', char):
                color = self.colors['lower']
            elif re.match(r'\d', char):
                color = self.colors['number']
            else:
                color = self.colors['symbol']

            x_pos = start_x + (i * char_width)
            self.display_canvas.create_text(
                x_pos,
                40,  # Vertical center of canvas
                text=char,
                fill=color,
                font=self.display_font,
                anchor=tk.W
            )

    def on_ok(self):
        """Handle OK button click or Enter key"""
        self.result = self.input_var.get()
        self.master.destroy()

    def get_result(self):
        """Return the entered password"""
        return self.result


def show_password_window():
    """Show the password visualizer window and return the result"""
    root = tk.Tk()
    app = PasswordVisualizer(root)
    root.mainloop()
    return app.get_result()


if __name__ == "__main__":
    password = show_password_window()
    if password:
        print(f"Password entered: {password}")
    else:
        print("No password entered or window closed.")