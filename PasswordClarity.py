import os
import platform
import re
import sys
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

# Handle PyInstaller's temp folder vs running from source
if getattr(sys, '_MEIPASS', None):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class PasswordVisualizer:
    def __init__(self, master):
        self.master = master
        master.title("Password Clarity")
        master.geometry("800x420")
        master.resizable(True, False)

        # --- Set window icon ---
        icon_path = os.path.join(BASE_PATH, "BK_Beard_Hair_Icon.ico")
        if os.path.exists(icon_path):
            master.iconbitmap(icon_path)

        # --- Cross-platform font selection ---
        os_name = platform.system()
        if os_name == "Windows":
            sans_family = "Segoe UI"
            mono_family = "Consolas"
        elif os_name == "Darwin":
            sans_family = "Helvetica Neue"
            mono_family = "Menlo"
        else:
            sans_family = "DejaVu Sans"
            mono_family = "DejaVu Sans Mono"

        self.title_font = tkfont.Font(family=sans_family, size=14)
        self.input_font = tkfont.Font(family=mono_family, size=16)
        self.display_font = tkfont.Font(family=mono_family, size=32)
        self.stats_font = tkfont.Font(family=sans_family, size=12)
        self.count_font = tkfont.Font(family=sans_family, size=12, weight="bold")

        self.colors = {
            'capital': "#00AA00",
            'lower': "#0000AA",
            'number': "#AA0000",
            'symbol': "#000000"
        }

        # --- ttk style setup ---
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure("Gray.TButton",
                             font=(sans_family, 11),
                             background="#757575",
                             foreground="white",
                             borderwidth=1,
                             focuscolor="none")
        self.style.map("Gray.TButton",
                       background=[("active", "#424242"),
                                   ("disabled", "#BDBDBD")],
                       foreground=[("disabled", "#666666")])

        self.style.configure("OK.TButton",
                             font=(sans_family, 14),
                             padding=(20, 8))

        # Main frame
        self.main_frame = tk.Frame(master, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(
            self.main_frame, text="Enter password to clarify:", font=self.title_font)
        self.title_label.pack(anchor=tk.W, pady=(0, 5))

        # Input row: entry + copy button
        self.input_row = tk.Frame(self.main_frame)
        self.input_row.pack(fill=tk.X, pady=(0, 10))

        self.input_var = tk.StringVar()
        self.input_var.trace_add("write", self.update_display)
        self.input_box = tk.Entry(
            self.input_row, textvariable=self.input_var,
            font=self.input_font, width=40, justify='left')
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

        self.copy_pw_button = ttk.Button(
            self.input_row, text="Copy Password",
            command=self.copy_password, style="Gray.TButton")
        self.copy_pw_button.pack(side=tk.LEFT)

        # Color-coded display
        self.display_frame = tk.Frame(self.main_frame, height=90)
        self.display_frame.pack(fill=tk.X, pady=10)
        self.display_frame.pack_propagate(False)

        self.password_text = tk.Text(
            self.display_frame, font=self.display_font, height=2,
            wrap=tk.NONE, state=tk.DISABLED, bg="white",
            relief=tk.SUNKEN, bd=1, cursor="arrow")

        self.h_scrollbar = tk.Scrollbar(
            self.display_frame, orient=tk.HORIZONTAL, command=self.password_text.xview)
        self.password_text.configure(xscrollcommand=self.h_scrollbar.set)

        self.password_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.password_text.tag_configure("uppercase", foreground=self.colors['capital'])
        self.password_text.tag_configure("lowercase", foreground=self.colors['lower'])
        self.password_text.tag_configure("digit", foreground=self.colors['number'])
        self.password_text.tag_configure("symbol", foreground=self.colors['symbol'])

        # Strength bar + label + counts
        self.strength_frame = tk.Frame(self.main_frame)
        self.strength_frame.pack(fill=tk.X, pady=(0, 10))

        self.strength_label = tk.Label(
            self.strength_frame, text="Strength: 0/100",
            font=self.count_font, fg="#AA0000", width=14, anchor=tk.E)
        self.strength_label.pack(side=tk.RIGHT)

        self.strength_bar = ttk.Progressbar(
            self.strength_frame, orient=tk.HORIZONTAL,
            length=200, mode='determinate', maximum=100, value=0)
        self.strength_bar.pack(side=tk.RIGHT, padx=(0, 8))

        self.counts_frame = tk.Frame(self.strength_frame)
        self.counts_frame.pack(side=tk.LEFT)

        tk.Label(self.counts_frame, text="Capital:", font=self.stats_font,
                 fg=self.colors['capital']).pack(side=tk.LEFT, padx=(0, 5))
        self.capital_count = tk.Label(self.counts_frame, text="0",
                                      font=self.count_font, fg=self.colors['capital'])
        self.capital_count.pack(side=tk.LEFT, padx=(0, 15))

        tk.Label(self.counts_frame, text="Lower:", font=self.stats_font,
                 fg=self.colors['lower']).pack(side=tk.LEFT, padx=(0, 5))
        self.lower_count = tk.Label(self.counts_frame, text="0",
                                     font=self.count_font, fg=self.colors['lower'])
        self.lower_count.pack(side=tk.LEFT, padx=(0, 15))

        tk.Label(self.counts_frame, text="Number:", font=self.stats_font,
                 fg=self.colors['number']).pack(side=tk.LEFT, padx=(0, 5))
        self.number_count = tk.Label(self.counts_frame, text="0",
                                      font=self.count_font, fg=self.colors['number'])
        self.number_count.pack(side=tk.LEFT, padx=(0, 15))

        tk.Label(self.counts_frame, text="Symbol:", font=self.stats_font,
                 fg=self.colors['symbol']).pack(side=tk.LEFT, padx=(0, 5))
        self.symbol_count = tk.Label(self.counts_frame, text="0",
                                      font=self.count_font, fg=self.colors['symbol'])
        self.symbol_count.pack(side=tk.LEFT)

        self.ok_button = ttk.Button(
            self.main_frame, text="OK", command=self.on_ok,
            width=10, style="OK.TButton")
        self.ok_button.pack(pady=(10, 0))

        self.input_box.bind("<Return>", lambda event: self.on_ok())
        self.input_box.focus_set()

        self.result = None

    def copy_password(self):
        pw = self.input_var.get()
        if pw:
            self.master.clipboard_clear()
            self.master.clipboard_append(pw)
            original = self.copy_pw_button.cget("text")
            self.copy_pw_button.config(text="Copied!")
            self.master.after(1500, lambda: self.copy_pw_button.config(text=original))

    def get_password_strength(self, password):
        if not password:
            return {'score': 0, 'capitals': 0, 'lowers': 0, 'numbers': 0, 'symbols': 0}

        capitals = len(re.findall(r'[A-Z]', password))
        lowers = len(re.findall(r'[a-z]', password))
        numbers = len(re.findall(r'\d', password))
        symbols = len(re.findall(r'[^A-Za-z0-9]', password))
        length = len(password)

        score = min(length * 4, 40)
        if capitals > 0: score += min(capitals * 2, 10)
        if lowers > 0: score += min(lowers * 2, 10)
        if numbers > 0: score += min(numbers * 2, 10)
        if symbols > 0: score += min(symbols * 3, 15)

        types_used = sum(1 for x in [capitals, lowers, numbers, symbols] if x > 0)
        score += types_used * 5

        return {
            'score': min(score, 100),
            'capitals': capitals, 'lowers': lowers,
            'numbers': numbers, 'symbols': symbols
        }

    def update_display(self, *args):
        password = self.input_var.get()
        strength = self.get_password_strength(password)

        self.capital_count.config(text=str(strength['capitals']))
        self.lower_count.config(text=str(strength['lowers']))
        self.number_count.config(text=str(strength['numbers']))
        self.symbol_count.config(text=str(strength['symbols']))

        score = strength['score']
        self.strength_label.config(text=f"Strength: {score}/100")
        self.strength_bar['value'] = score

        if score < 40:
            self.strength_label.config(fg="#AA0000")
            self.style.configure("Horizontal.TProgressbar", troughcolor="#f0f0f0", background="#AA0000")
        elif score < 70:
            self.strength_label.config(fg="#FF8800")
            self.style.configure("Horizontal.TProgressbar", troughcolor="#f0f0f0", background="#FF8800")
        else:
            self.strength_label.config(fg="#00AA00")
            self.style.configure("Horizontal.TProgressbar", troughcolor="#f0f0f0", background="#00AA00")

        if not password:
            self.password_text.config(state=tk.NORMAL)
            self.password_text.delete(1.0, tk.END)
            self.password_text.config(state=tk.DISABLED)
            return

        self.password_text.config(state=tk.NORMAL)
        self.password_text.delete(1.0, tk.END)

        for char in password:
            if re.match(r'[A-Z]', char): tag = "uppercase"
            elif re.match(r'[a-z]', char): tag = "lowercase"
            elif re.match(r'\d', char): tag = "digit"
            else: tag = "symbol"
            self.password_text.insert(tk.END, char, tag)

        self.password_text.tag_add("center", "1.0", "end")
        self.password_text.tag_configure("center", justify='center')
        self.password_text.config(state=tk.DISABLED)

    def on_ok(self):
        self.result = self.input_var.get()
        self.master.destroy()

    def get_result(self):
        return self.result


def show_password_window():
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
