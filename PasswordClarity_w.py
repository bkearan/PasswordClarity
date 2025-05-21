import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import re
import math
import random
import hashlib


class PasswordVisualizer:
    def __init__(self, master):
        self.master = master
        master.title("Password Clarity")
        master.geometry("800x500")
        master.resizable(True, False)  # Allow horizontal resizing

        # Configure fonts
        self.title_font = tkfont.Font(family="DejaVu Sans", size=14)
        self.input_font = tkfont.Font(family="Monospace", size=16)
        self.display_font = tkfont.Font(family="Monospace", size=32)  # Increased from 20 to 32
        self.stats_font = tkfont.Font(family="DejaVu Sans", size=12)
        self.count_font = tkfont.Font(family="DejaVu Sans", size=12, weight="bold")
        self.small_font = tkfont.Font(family="DejaVu Sans", size=10)

        # Colors for character types
        self.colors = {
            'capital': "#00AA00",  # Green
            'lower': "#0000AA",  # Blue
            'number': "#AA0000",  # Red
            'symbol': "#000000"  # Black
        }

        # Load word lists and common passwords
        self.word_list = self.load_word_list()
        self.symbol_list = ['@', '#', '$', '%', '&', '*', '!', '?', '>', '<', '+']
        self.common_passwords = self.load_common_passwords()

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
            width=40,
            justify='left'  # Ensure left alignment
        )
        self.input_box.pack(fill=tk.X, pady=(0, 10))

        # Password display (using Text widget instead of Canvas for better text handling)
        self.display_frame = tk.Frame(self.main_frame, height=90)
        self.display_frame.pack(fill=tk.X, pady=10)
        self.display_frame.pack_propagate(False)

        # Create a Text widget for the password display
        self.password_text = tk.Text(
            self.display_frame,
            font=self.display_font,
            height=2,
            wrap=tk.NONE,  # No word wrapping
            state=tk.DISABLED,
            bg="white",
            relief=tk.SUNKEN,
            bd=1,
            cursor="arrow"
        )

        # Add horizontal scrollbar for long passwords
        self.h_scrollbar = tk.Scrollbar(self.display_frame, orient=tk.HORIZONTAL, command=self.password_text.xview)
        self.password_text.configure(xscrollcommand=self.h_scrollbar.set)

        # Pack the text widget and scrollbar
        self.password_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Configure text tags for colors
        self.password_text.tag_configure("uppercase", foreground=self.colors['capital'])
        self.password_text.tag_configure("lowercase", foreground=self.colors['lower'])
        self.password_text.tag_configure("digit", foreground=self.colors['number'])
        self.password_text.tag_configure("symbol", foreground=self.colors['symbol'])

        # Security warnings frame
        self.warning_frame = tk.Frame(self.main_frame)
        self.warning_frame.pack(fill=tk.X, pady=(0, 10))

        self.warning_label = tk.Label(
            self.warning_frame,
            text="",
            font=self.small_font,
            fg="#CC0000",
            wraplength=750,  # Increased from 650 to 750
            justify=tk.LEFT
        )
        self.warning_label.pack(anchor=tk.W)

        # Strength and counts frame
        self.stats_frame = tk.Frame(self.main_frame)
        self.stats_frame.pack(fill=tk.X, pady=(0, 10))

        # Strength score
        self.strength_label = tk.Label(
            self.stats_frame,
            text="Strength: 0/100",
            font=self.count_font,
            fg="#AA0000"  # Default to red
        )
        self.strength_label.pack(side=tk.RIGHT)

        # Character counts
        self.counts_frame = tk.Frame(self.stats_frame)
        self.counts_frame.pack(side=tk.LEFT)

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

        # Suggestion frame
        self.suggestion_frame = tk.Frame(self.main_frame)
        self.suggestion_frame.pack(fill=tk.X, pady=(10, 0))

        # Generate suggestion button
        self.generate_button = tk.Button(
            self.suggestion_frame,
            text="Generate Secure Passphrase",
            command=self.generate_passphrase,
            font=self.stats_font,
            bg="#4CAF50",
            fg="white",
            relief=tk.RAISED,
            bd=2
        )
        self.generate_button.pack(side=tk.LEFT, padx=(0, 10))

        # Use suggestion button
        self.use_button = tk.Button(
            self.suggestion_frame,
            text="Use Suggestion",
            command=self.use_suggestion,
            font=self.stats_font,
            bg="#2196F3",
            fg="white",
            relief=tk.RAISED,
            bd=2,
            state=tk.DISABLED
        )
        self.use_button.pack(side=tk.LEFT)

        # Suggestion display
        self.suggestion_text = tk.Text(
            self.main_frame,
            height=3,
            font=self.input_font,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#f0f0f0",
            relief=tk.SUNKEN,
            bd=1
        )
        self.suggestion_text.pack(fill=tk.X, pady=(10, 10))

        # OK button
        self.ok_button = tk.Button(
            self.main_frame,
            text="OK",
            command=self.on_ok,
            width=10,
            height=2,
            font=self.title_font
        )
        self.ok_button.pack(pady=(10, 0))

        # Handle Enter key
        self.input_box.bind("<Return>", lambda event: self.on_ok())

        # Set focus to input box
        self.input_box.focus_set()

        # Result variable
        self.result = None
        self.current_suggestion = ""

    def load_word_list(self):
        """Load a comprehensive word list"""
        # This is a sample word list - you can replace with your Excel word list
        words = [
            "abandon", "ability", "absence", "academy", "account", "accused", "achieve", "acquire", "address",
            "advance",
            "advocate", "african", "against", "already", "ancient", "another", "anxiety", "anybody", "application",
            "approach",
            "arrange", "article", "attempt", "attract", "auction", "average", "balance", "battery", "beneath",
            "benefit",
            "between", "bicycle", "brother", "brought", "builder", "burning", "cabinet", "caliber", "calcium",
            "campaign",
            "capable", "capacity", "capital", "captain", "capture", "careful", "carrier", "catalog", "ceiling",
            "central",
            "century", "certain", "chamber", "channel", "chapter", "charity", "chemical", "chicken", "circuit",
            "citizen",
            "classic", "climate", "clothes", "college", "combine", "comfort", "command", "comment", "company",
            "compare",
            "compile", "complex", "compute", "concept", "concern", "confirm", "connect", "consent", "consist",
            "contact",
            "contain", "content", "contest", "context", "control", "convert", "council", "counter", "country",
            "courage",
            "crystal", "culture", "current", "custody", "dealing", "decline", "default", "defense", "deliver",
            "density",
            "deposit", "desktop", "despite", "destroy", "diagram", "digital", "dignity", "diploma", "disable",
            "disease",
            "dismiss", "display", "dispute", "divorce", "domestic", "drawing", "dynamic", "eastern", "economy",
            "element",
            "enhance", "evening", "exclude", "execute", "exhibit", "explain", "explore", "extreme", "factory",
            "failure",
            "fantasy", "fashion", "feature", "federal", "finance", "finding", "fishing", "fitness", "foreign",
            "formula",
            "fortune", "forward", "freedom", "freight", "funeral", "gallery", "gateway", "general", "genetic",
            "genuine",
            "glimpse", "grocery", "growing", "habitat", "harmony", "heading", "hearing", "heating", "holiday",
            "horizon",
            "husband", "illegal", "imagery", "imagine", "immune", "impact", "improve", "initial", "inquiry", "insight",
            "install", "instead", "intense", "interim", "involve", "journal", "journey", "justice", "justify",
            "kitchen",
            "landing", "largely", "leading", "learning", "leaving", "lecture", "leisure", "license", "limited",
            "listing",
            "logical", "loyalty", "machine", "manager", "mandate", "martial", "maximum", "meaning", "measure",
            "medical",
            "meeting", "mental", "message", "mineral", "minimal", "minimum", "mission", "mistake", "mixture", "monitor",
            "morning", "musical", "mystery", "natural", "neither", "network", "neutral", "nuclear", "nursing",
            "obvious",
            "offense", "opening", "operate", "opinion", "optimal", "organic", "outline", "outlook", "overall",
            "overlap",
            "package", "parking", "partial", "partner", "passion", "patient", "pattern", "payment", "penalty",
            "pending",
            "perfect", "perform", "perhaps", "phantom", "picture", "plastic", "platform", "popular", "portion",
            "poverty",
            "precise", "predict", "premium", "prepare", "present", "prevent", "primary", "privacy", "private",
            "problem",
            "process", "produce", "product", "profile", "project", "promise", "promote", "protect", "provide",
            "publish",
            "purpose", "qualify", "quality", "quarter", "radical", "railway", "rainbow", "random", "readily", "reality",
            "receipt", "receive", "recover", "reflect", "regular", "related", "release", "relevant", "remain",
            "removal",
            "replace", "request", "require", "rescue", "reserve", "respect", "respond", "restore", "revenue", "reverse",
            "routine", "science", "scratch", "section", "segment", "serious", "service", "session", "setting",
            "shelter",
            "silence", "similar", "smoking", "society", "somehow", "speaker", "special", "station", "storage",
            "strange",
            "stretch", "student", "subject", "success", "suggest", "summary", "support", "suppose", "supreme",
            "surface",
            "survive", "suspect", "sustain", "symptom", "tactics", "teacher", "theater", "therapy", "through",
            "tonight",
            "traffic", "training", "transit", "trouble", "uniform", "unique", "unknown", "upgrade", "utility",
            "variety",
            "vehicle", "venture", "version", "village", "virtual", "visible", "vitamin", "welfare", "western",
            "whisper",
            "willing", "windows", "winning", "wireless", "witness", "working", "writing", "written", "achieve",
            "blanket",
            "brother", "cabinet", "channel", "command", "crystal", "diamond", "digital", "drawing", "element",
            "evening",
            "explore", "factory", "fishing", "freedom", "gallery", "genetic", "harvest", "heading", "install",
            "journey",
            "kitchen", "landing", "machine", "manager", "morning", "mystery", "network", "operate", "package",
            "parking",
            "perfect", "picture", "plastic", "popular", "present", "primary", "privacy", "problem", "protect",
            "publish",
            "railway", "reality", "regular", "replace", "request", "science", "section", "service", "setting",
            "similar",
            "society", "station", "strange", "student", "suggest", "support", "surface", "teacher", "theater",
            "through",
            "tonight", "traffic", "trouble", "uniform", "upgrade", "utility", "variety", "vehicle", "venture",
            "version",
            "village", "virtual", "visible", "welfare", "western", "willing", "windows", "winning", "witness",
            "working",
            "writing", "written", "abandon", "ability", "absence", "academy", "account", "accused", "acquire",
            "address",
            "advance", "advocate", "african", "against", "already", "ancient", "another", "anxiety", "anybody",
            "attempt",
            "attract", "auction", "average", "balance", "battery", "beneath", "benefit", "between", "bicycle",
            "brought",
            "builder", "burning", "calcium", "campaign", "capable", "capacity", "capital", "captain", "capture",
            "careful",
            "carrier", "catalog", "ceiling", "central", "century", "certain", "chamber", "chapter", "charity",
            "chemical",
            "chicken", "circuit", "citizen", "classic", "climate", "clothes", "college", "combine", "comfort",
            "comment",
            "company", "compare", "compile", "complex", "compute", "concept", "concern", "confirm", "connect",
            "consent",
            "consist", "contact", "contain", "content", "contest", "context", "control", "convert", "council",
            "counter",
            "country", "courage", "culture", "current", "custody", "dealing", "decline", "default", "defense",
            "deliver",
            "density", "deposit", "desktop", "despite", "destroy", "diagram", "dignity", "diploma", "disable",
            "disease",
            "dismiss", "display", "dispute", "divorce", "domestic", "dynamic", "eastern", "economy", "enhance",
            "evening",
            "exclude", "execute", "exhibit", "explain", "extreme", "failure", "fantasy", "fashion", "feature",
            "federal",
            "finance", "finding", "fitness", "foreign", "formula", "fortune", "forward", "freight", "funeral",
            "gateway",
            "general", "genuine", "glimpse", "grocery", "growing", "habitat", "harmony", "hearing", "heating",
            "holiday",
            "horizon", "husband", "illegal", "imagery", "imagine", "immune", "impact", "improve", "initial", "inquiry",
            "insight", "instead", "intense", "interim", "involve", "journal", "justice", "justify", "largely",
            "leading",
            "learning", "leaving", "lecture", "leisure", "license", "limited", "listing", "logical", "loyalty",
            "mandate",
            "martial", "maximum", "meaning", "measure", "medical", "meeting", "mental", "message", "mineral", "minimal",
            "minimum", "mission", "mistake", "mixture", "monitor", "musical", "natural", "neither", "neutral",
            "nuclear",
            "nursing", "obvious", "offense", "opening", "opinion", "optimal", "organic", "outline", "outlook",
            "overall",
            "overlap", "partial", "partner", "passion", "patient", "pattern", "payment", "penalty", "pending",
            "perform",
            "perhaps", "phantom", "portion", "poverty", "precise", "predict", "premium", "prepare", "prevent",
            "privacy",
            "private", "process", "produce", "product", "profile", "project", "promise", "promote", "provide",
            "purpose",
            "qualify", "quality", "quarter", "radical", "railway", "rainbow", "random", "readily", "receipt", "receive",
            "recover", "reflect", "related", "release", "relevant", "remain", "removal", "require", "rescue", "reserve",
            "respect", "respond", "restore", "revenue", "reverse", "routine", "scratch", "segment", "serious",
            "session",
            "shelter", "silence", "smoking", "somehow", "speaker", "special", "storage", "stretch", "subject",
            "success",
            "summary", "suppose", "supreme", "survive", "suspect", "sustain", "symptom", "tactics", "therapy",
            "training",
            "transit", "unique", "unknown", "village", "virtual", "visible", "vitamin", "welfare", "western", "whisper",
            "willing", "windows", "winning", "wireless", "witness", "working", "writing", "written"
        ]
        return words

    def load_common_passwords(self):
        """Load common passwords for checking"""
        # This is a sample list - you can expand this with more comprehensive lists
        common = [
            "123456", "password", "123456789", "12345678", "12345", "1234567", "1234567890",
            "qwerty", "abc123", "password1", "111111", "123123", "admin", "letmein", "welcome",
            "monkey", "1234", "dragon", "master", "login", "princess", "solo", "sunshine",
            "passw0rd", "football", "baseball", "jordan", "freedom", "batman", "trustno1",
            "password123", "welcome1", "hello", "charlie", "access", "shadow", "flower",
            "123qwe", "iloveyou", "superman", "whatever", "killer", "summer", "michael",
            "ranger", "lovely", "babygirl", "ashley", "nicole", "cheese", "computer",
            "soccer", "internet", "service", "canada", "hello123", "guest", "buster",
            "test", "love", "0000", "2000", "jordan23", "eagle1", "pass", "fuckme",
            "badboy", "hunter", "test123", "cricket", "pass@word1", "changeme", "secret",
            "orange", "fuckyou", "starwars", "password!", "Password", "Password1",
            "Password123", "password@123", "p@ssw0rd", "P@ssw0rd", "P@ssword",
            "password1!", "qwertyuiop", "asdfghjkl", "zxcvbnm", "qwerty123",
            "123456a", "a123456", "password12", "admin123", "root", "toor",
            "administrator", "default", "guest123", "user", "temp", "demo"
        ]
        return set(common)

    def check_common_patterns(self, password):
        """Check for common password patterns and weaknesses"""
        warnings = []

        # Check against common passwords
        if password.lower() in self.common_passwords:
            warnings.append("WARNING: This is a commonly used password")

        # Check for keyboard patterns
        keyboard_patterns = [
            "qwerty", "qwertyuiop", "asdfghjkl", "zxcvbnm", "12345",
            "abcde", "1qaz", "2wsx", "3edc", "4rfv", "5tgb", "6yhn"
        ]

        for pattern in keyboard_patterns:
            if pattern in password.lower():
                warnings.append("WARNING: Contains keyboard pattern")
                break

        # Check for sequential numbers
        if re.search(r'(012|123|234|345|456|567|678|789|890)', password):
            warnings.append("WARNING: Contains sequential numbers")

        # Check for repeated characters
        if re.search(r'(.)\1{2,}', password):
            warnings.append("WARNING: Contains repeated characters")

        # Check for dictionary words
        password_lower = password.lower()
        for word in self.word_list:
            if len(word) > 3 and word.lower() in password_lower:
                warnings.append("WARNING: Contains dictionary word")
                break

        # Check for personal info patterns
        personal_patterns = [
            r'\b(19|20)\d{2}\b',  # Years
            r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)',  # Months
            r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)',  # Days
            r'\b(password|login|admin|user|guest|test|demo)\b'  # Common words
        ]

        for pattern in personal_patterns:
            if re.search(pattern, password.lower()):
                warnings.append("WARNING: Contains predictable pattern")
                break

        # Check for insufficient length
        if len(password) < 8:
            warnings.append("WARNING: Password is too short (minimum 8 characters)")

        # Check for missing character types
        if not re.search(r'[A-Z]', password) and len(password) > 0:
            warnings.append("TIP: Consider adding uppercase letters")
        if not re.search(r'[a-z]', password) and len(password) > 0:
            warnings.append("TIP: Consider adding lowercase letters")
        if not re.search(r'\d', password) and len(password) > 0:
            warnings.append("TIP: Consider adding numbers")
        if not re.search(r'[^A-Za-z0-9]', password) and len(password) > 0:
            warnings.append("TIP: Consider adding symbols")

        return warnings

    def generate_passphrase(self):
        """Generate a secure passphrase using one of the Excel-style formulas randomly"""
        # Randomly select one of your Excel formulas:

        # Formula 1: word + num + symbol + WORD + symbol + word + num
        # =INDEX(WordList!A:A,RANDBETWEEN(1,1500),1)&(RANDBETWEEN(10,99)&INDEX(SymbolList!A:A,RANDBETWEEN(1,11),1))&UPPER(INDEX(WordList!A:A,RANDBETWEEN(1,1500),1))&INDEX(SymbolList!A:A,RANDBETWEEN(1,11),1)&INDEX(WordList!A:A,RANDBETWEEN(1,1500),1)&(RANDBETWEEN(10,99))

        # Formula 2: word + symbol + WORD + num + symbol + word + num
        # =INDEX(WordList!A:A,RANDBETWEEN(1,1500),1)&INDEX(SymbolList!A:A,RANDBETWEEN(1,11),1)&UPPER(INDEX(WordList!A:A,RANDBETWEEN(1,1500),1))&(RANDBETWEEN(10,99))&INDEX(SymbolList!A:A,RANDBETWEEN(1,11),1)&INDEX(WordList!A:A,RANDBETWEEN(1,1500),1)&(RANDBETWEEN(10,99))

        # Formula 3: word + num + symbol + WORD + num + symbol + word
        # =INDEX(WordList!A:A,RANDBETWEEN(1,1500),1)&(RANDBETWEEN(10,99)&INDEX(SymbolList!A:A,RANDBETWEEN(1,11),1))&UPPER(INDEX(WordList!A:A,RANDBETWEEN(1,1500),1))&(RANDBETWEEN(10,99))&INDEX(SymbolList!A:A,RANDBETWEEN(1,11),1)&INDEX(WordList!A:A,RANDBETWEEN(1,1500),1)

        word1 = random.choice(self.word_list)
        word2 = random.choice(self.word_list).upper()
        word3 = random.choice(self.word_list)
        num1 = random.randint(10, 99)
        num2 = random.randint(10, 99)
        symbol1 = random.choice(self.symbol_list)
        symbol2 = random.choice(self.symbol_list)

        # Randomly choose one of the formula patterns
        formula_choice = random.randint(1, 3)

        if formula_choice == 1:
            # Formula 1: word + num + symbol + WORD + symbol + word + num
            passphrase = f"{word1}{num1}{symbol1}{word2}{symbol2}{word3}{num2}"
            pattern = "Pattern 1: word+num+symbol+WORD+symbol+word+num"

        elif formula_choice == 2:
            # Formula 2: word + symbol + WORD + num + symbol + word + num
            passphrase = f"{word1}{symbol1}{word2}{num1}{symbol2}{word3}{num2}"
            pattern = "Pattern 2: word+symbol+WORD+num+symbol+word+num"

        else:
            # Formula 3: word + num + symbol + WORD + num + symbol + word
            passphrase = f"{word1}{num1}{symbol1}{word2}{num2}{symbol2}{word3}"
            pattern = "Pattern 3: word+num+symbol+WORD+num+symbol+word"

        self.current_suggestion = passphrase

        # Display the suggestion without pattern info
        self.suggestion_text.config(state=tk.NORMAL)
        self.suggestion_text.delete(1.0, tk.END)
        self.suggestion_text.insert(tk.END, f"Suggestion: {passphrase}")
        self.suggestion_text.config(state=tk.DISABLED)

        # Enable the use button
        self.use_button.config(state=tk.NORMAL)

    def use_suggestion(self):
        """Use the generated suggestion as the password"""
        if self.current_suggestion:
            # Clear the input box first
            self.input_box.delete(0, tk.END)
            # Insert the suggestion normally
            self.input_box.insert(0, self.current_suggestion)
            # Set focus to the input box
            self.input_box.focus_set()
            # Position cursor at the end
            self.input_box.icursor(tk.END)

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
        score += min(length * 3, 40)

        # Character type points
        if capitals > 0:
            score += min(capitals * 2, 10)
        if lowers > 0:
            score += min(lowers * 2, 10)
        if numbers > 0:
            score += min(numbers * 2, 10)
        if symbols > 0:
            score += min(symbols * 3, 15)

        # Bonus for mixture of character types (up to 20 points)
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

        # Penalty for common passwords and patterns
        warnings = self.check_common_patterns(password)
        penalty = 0
        for warning in warnings:
            if "commonly used" in warning:
                penalty += 30
            elif "keyboard pattern" in warning or "sequential" in warning:
                penalty += 15
            elif "repeated characters" in warning:
                penalty += 10
            elif "dictionary word" in warning:
                penalty += 5

        score = max(0, score - penalty)

        return {
            'score': min(score, 100),
            'capitals': capitals,
            'lowers': lowers,
            'numbers': numbers,
            'symbols': symbols
        }

    def update_display(self, *args):
        """Update the display when the password changes"""
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
        if score < 30:
            self.strength_label.config(fg="#AA0000")  # Red
        elif score < 60:
            self.strength_label.config(fg="#FF8800")  # Orange
        elif score < 80:
            self.strength_label.config(fg="#CCAA00")  # Yellow
        else:
            self.strength_label.config(fg="#00AA00")  # Green

        # Check for warnings
        warnings = self.check_common_patterns(password)
        if warnings:
            warning_text = " | ".join(warnings[:3])  # Show first 3 warnings, separated by |
            if len(warnings) > 3:
                warning_text += f" | +{len(warnings) - 3} more issues"
            self.warning_label.config(text=warning_text)
        else:
            self.warning_label.config(text="")

        # Update password display
        if not password:
            # Clear display if no password
            self.password_text.config(state=tk.NORMAL)
            self.password_text.delete(1.0, tk.END)
            self.password_text.config(state=tk.DISABLED)
            return

        # Enable text widget for editing
        self.password_text.config(state=tk.NORMAL)

        # Clear current content
        self.password_text.delete(1.0, tk.END)

        # Add each character with appropriate color
        for char in password:
            if re.match(r'[A-Z]', char):
                tag = "uppercase"
            elif re.match(r'[a-z]', char):
                tag = "lowercase"
            elif re.match(r'\d', char):
                tag = "digit"
            else:
                tag = "symbol"

            self.password_text.insert(tk.END, char, tag)

        # Center the text
        self.password_text.tag_add("center", "1.0", "end")
        self.password_text.tag_configure("center", justify='center')

        # Disable text widget to prevent editing
        self.password_text.config(state=tk.DISABLED)

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