import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from PIL import Image, ImageTk
import re
import threading
from lexer import Lexer  # Import your lexer


class CelerityCompiler:
    def __init__(self, root):
        self.root = root
        self.root.title("Celerity Compiler")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1e1e1e")
        
        # Color palette from logo
        self.colors = {
            'bg_dark': '#1e1e1e',
            'bg_medium': '#252526',
            'bg_light': '#2d2d30',
            'orange': '#FF6B35',
            'pink': '#FF2E63',
            'text_white': '#ffffff',
            'text_gray': '#858585',
            'comment_green': '#6A9955',
            'keyword_orange': '#FF6B35',
            'string_brown': '#CE9178',
            'number_blue': '#B5CEA8',
            'line_numbers': '#858585',
            'indent_line': '#404040'
        }
        
        self.current_view = 'lexical'  # Track current output view
        self.lexer = Lexer()
        self.tokens = []
        self.errors = []
        self.lexer_thread = None
        self.is_running = False
        
        self.create_widgets()
        self.insert_default_code()
        
    def create_widgets(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg=self.colors['bg_medium'], height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        # Logo placeholder
        try:
            logo_image = Image.open("icon/Celerity.png")
            logo_image = logo_image.resize((45, 45), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(header_frame, image=self.logo_photo, bg=self.colors['bg_medium'])
            logo_label.pack(side=tk.LEFT, padx=15, pady=7)
        except Exception as e:
            print(f"Logo not found: {e}")
        
        # Celerity Name
        name_label = tk.Label(
            header_frame, 
            text="Celerity", 
            font=("Segoe UI", 24, "bold"),
            fg=self.colors['orange'],
            bg=self.colors['bg_medium']
        )
        name_label.pack(side=tk.LEFT, padx=(15, 0), pady=7)
        
        # Main Container
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left Panel (Code Editor)
        left_panel = tk.Frame(main_container, bg=self.colors['bg_dark'])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Code Editor Header
        editor_header = tk.Frame(left_panel, bg=self.colors['bg_medium'], height=40)
        editor_header.pack(fill=tk.X)
        editor_header.pack_propagate(False)
        
        editor_label = tk.Label(
            editor_header,
            text="Code Editor",
            font=("Segoe UI", 11, "bold"),
            fg=self.colors['text_white'],
            bg=self.colors['bg_medium']
        )
        editor_label.pack(side=tk.LEFT, padx=15, pady=8)
        
        # Run Button with play icon
        self.run_button = tk.Button(
            editor_header,
            text="▶ Run",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors['text_white'],
            bg=self.colors['orange'],
            activebackground=self.colors['pink'],
            activeforeground=self.colors['text_white'],
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=5,
            command=self.run_code
        )
        self.run_button.pack(side=tk.RIGHT, padx=(5, 0), pady=5)
        
        # Stop Button
        self.stop_button = tk.Button(
            editor_header,
            text="⏹ Stop",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors['text_white'],
            bg="#C8675C",
            activebackground="#930000",
            activeforeground=self.colors['text_white'],
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=5,
            command=self.stop_code,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.RIGHT, padx=15, pady=5)
        
        # Code Editor Frame with line numbers
        editor_container = tk.Frame(left_panel, bg=self.colors['bg_dark'])
        editor_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Line Numbers
        self.line_numbers = tk.Text(
            editor_container,
            width=4,
            padx=5,
            pady=10,
            font=("Consolas", 11),
            bg=self.colors['bg_medium'],
            fg=self.colors['line_numbers'],
            state=tk.DISABLED,
            relief=tk.FLAT,
            wrap=tk.NONE
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Code Text Area
        self.code_text = tk.Text(
            editor_container,
            font=("Consolas", 11),
            bg=self.colors['bg_light'],
            fg=self.colors['text_white'],
            insertbackground=self.colors['text_white'],
            selectbackground='#3E3E42',  # Light grey selection
            selectforeground=self.colors['text_white'],
            relief=tk.FLAT,
            wrap=tk.NONE,
            padx=10,
            pady=10,
            undo=True,
            tabs=('1c', '2c', '3c', '4c')
        )
        self.code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars for code editor
        code_scrollbar_y = ttk.Scrollbar(editor_container, command=self.code_text.yview)
        code_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.code_text.config(yscrollcommand=code_scrollbar_y.set)
        
        code_scrollbar_x = ttk.Scrollbar(left_panel, orient=tk.HORIZONTAL, command=self.code_text.xview)
        code_scrollbar_x.pack(fill=tk.X)
        self.code_text.config(xscrollcommand=code_scrollbar_x.set)
        
        # Bind events for syntax highlighting, line numbers, and indent guides
        self.code_text.bind('<KeyRelease>', self.on_key_release)
        self.code_text.bind('<MouseWheel>', self.on_scroll)
        self.code_text.bind('<Tab>', self.handle_tab)
        self.code_text.bind('<Return>', self.handle_return)
        self.code_text.bind('<BackSpace>', self.handle_backspace)
        self.code_text.bind('<Key>', self.handle_bracket_autocompletion)
        
        # Right Panel (Output)
        right_panel = tk.Frame(main_container, bg=self.colors['bg_dark'], width=500)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right_panel.pack_propagate(False)
        
        # Output Header with buttons
        output_header = tk.Frame(right_panel, bg=self.colors['bg_medium'], height=40)
        output_header.pack(fill=tk.X)
        output_header.pack_propagate(False)
        
        # View Buttons
        self.lexical_btn = tk.Button(
            output_header,
            text="Lexical",
            font=("Segoe UI", 9, "bold"),
            fg=self.colors['text_white'],
            bg=self.colors['orange'],
            activebackground=self.colors['orange'],
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=3,
            command=lambda: self.switch_view('lexical')
        )
        self.lexical_btn.pack(side=tk.LEFT, padx=(15, 3), pady=5)
        
        self.syntax_btn = tk.Button(
            output_header,
            text="Syntax",
            font=("Segoe UI", 9, "bold"),
            fg=self.colors['text_white'],
            bg=self.colors['bg_light'],
            activebackground=self.colors['orange'],
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=3,
            command=lambda: self.switch_view('syntax')
        )
        self.syntax_btn.pack(side=tk.LEFT, padx=3, pady=5)
        
        self.semantic_btn = tk.Button(
            output_header,
            text="Semantic",
            font=("Segoe UI", 9, "bold"),
            fg=self.colors['text_white'],
            bg=self.colors['bg_light'],
            activebackground=self.colors['pink'],
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=3,
            command=lambda: self.switch_view('semantic')
        )
        self.semantic_btn.pack(side=tk.LEFT, padx=3, pady=5)
        
        # Output Text Area
        self.output_text = scrolledtext.ScrolledText(
            right_panel,
            font=("Consolas", 10),
            bg=self.colors['bg_light'],
            fg=self.colors['text_white'],
            relief=tk.FLAT,
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Bottom Panel (Errors/Terminal/Output)
        bottom_panel = tk.Frame(self.root, bg=self.colors['bg_dark'], height=200)
        bottom_panel.pack(fill=tk.BOTH, side=tk.BOTTOM, padx=5, pady=(0, 5))
        bottom_panel.pack_propagate(False)
        
        # Bottom Tabs
        bottom_notebook = ttk.Notebook(bottom_panel)
        bottom_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Style for notebook
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=self.colors['bg_medium'], borderwidth=0)
        style.configure('TNotebook.Tab', background=self.colors['bg_light'], 
                       foreground=self.colors['text_white'], padding=[20, 5])
        style.map('TNotebook.Tab', background=[('selected', self.colors['bg_medium'])],
                 foreground=[('selected', self.colors['orange'])])
        
        # Error Display Tab
        error_frame = tk.Frame(bottom_notebook, bg=self.colors['bg_light'])
        self.error_text = scrolledtext.ScrolledText(
            error_frame,
            font=("Consolas", 9),
            bg=self.colors['bg_light'],
            fg='#F48771',
            relief=tk.FLAT,
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.error_text.pack(fill=tk.BOTH, expand=True)
        bottom_notebook.add(error_frame, text="Errors")
        
        # Terminal Tab
        terminal_frame = tk.Frame(bottom_notebook, bg=self.colors['bg_light'])
        terminal_layout = tk.Frame(terminal_frame, bg=self.colors['bg_light'])
        terminal_layout.pack(fill=tk.BOTH, expand=True)
        
        self.terminal_text = scrolledtext.ScrolledText(
            terminal_layout,
            font=("Consolas", 9),
            bg=self.colors['bg_light'],
            fg=self.colors['text_white'],
            relief=tk.FLAT,
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.terminal_text.pack(fill=tk.BOTH, expand=True)
        
        # Input field and submit button
        input_container = tk.Frame(terminal_layout, bg=self.colors['bg_light'])
        input_container.pack(fill=tk.X, padx=5, pady=5)
        
        self.input_field = tk.Entry(
            input_container,
            font=("Consolas", 10),
            bg=self.colors['bg_medium'],
            fg=self.colors['text_white'],
            insertbackground=self.colors['text_white'],
            relief=tk.FLAT
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_field.bind('<Return>', lambda e: self.submit_input())
        
        self.submit_button = tk.Button(
            input_container,
            text="Submit",
            font=("Segoe UI", 9, "bold"),
            fg=self.colors['text_white'],
            bg=self.colors['orange'],
            activebackground=self.colors['pink'],
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=3,
            command=self.submit_input
        )
        self.submit_button.pack(side=tk.RIGHT)
        
        bottom_notebook.add(terminal_frame, text="Terminal")
        
        # Output Code Tab
        output_code_frame = tk.Frame(bottom_notebook, bg=self.colors['bg_light'])
        self.output_code_text = scrolledtext.ScrolledText(
            output_code_frame,
            font=("Consolas", 9),
            bg=self.colors['bg_light'],
            fg=self.colors['text_white'],
            relief=tk.FLAT,
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.output_code_text.pack(fill=tk.BOTH, expand=True)
        bottom_notebook.add(output_code_frame, text="Generated Code")
        
        # Configure tags for syntax highlighting
        self.code_text.tag_configure('comment', foreground=self.colors['comment_green'])
        self.code_text.tag_configure('keyword', foreground=self.colors['keyword_orange'])
        self.code_text.tag_configure('string', foreground=self.colors['string_brown'])
        self.code_text.tag_configure('number', foreground=self.colors['number_blue'])
        self.code_text.tag_configure('indent_guide', foreground=self.colors['indent_line'])
    
    def submit_input(self):
        """Handle user input submission"""
        user_input = self.input_field.get()
        if user_input:
            self.terminal_text.insert(tk.END, f"> {user_input}\n")
            self.terminal_text.see(tk.END)
            self.input_field.delete(0, tk.END)
            # Process the input as needed for your compiler
    
    def handle_tab(self, event):
        """Handle Tab key press for 4-space indentation"""
        self.code_text.insert(tk.INSERT, "    ")
        self.update_line_numbers()
        self.highlight_syntax()
        self.draw_indent_guides()
        return "break"
    
    def handle_return(self, event):
        """Handle Return key press for auto-indentation"""
        cursor_pos = self.code_text.index(tk.INSERT)
        line_num = int(cursor_pos.split('.')[0])
        current_line = self.code_text.get(f"{line_num}.0", f"{line_num}.end")
        
        # Calculate current indentation
        indent = len(current_line) - len(current_line.lstrip())
        
        # Check if line ends with opening bracket
        stripped_line = current_line.strip()
        if stripped_line.endswith('{') or stripped_line.endswith('(') or stripped_line.endswith('['):
            self.code_text.insert(tk.INSERT, "\n" + " " * (indent + 4))
        else:
            self.code_text.insert(tk.INSERT, "\n" + " " * indent)
        
        self.update_line_numbers()
        self.highlight_syntax()
        self.draw_indent_guides()
        return "break"
    
    def handle_backspace(self, event):
        """Handle Backspace to delete 4 spaces at once if at indent position"""
        cursor_pos = self.code_text.index(tk.INSERT)
        line_num, col_num = map(int, cursor_pos.split('.'))
        
        if col_num >= 4:
            # Check if the previous 4 characters are spaces
            prev_chars = self.code_text.get(f"{line_num}.{col_num-4}", f"{line_num}.{col_num}")
            if prev_chars == "    ":
                self.code_text.delete(f"{line_num}.{col_num-4}", f"{line_num}.{col_num}")
                self.update_line_numbers()
                self.highlight_syntax()
                self.draw_indent_guides()
                return "break"
        return None
    
    def handle_bracket_autocompletion(self, event):
        """Handle auto-completion of brackets"""
        bracket_pairs = {
            '(': ')',
            '[': ']',
            '{': '}',
            '"': '"',
            "'": "'"
        }
        
        if event.char in bracket_pairs:
            cursor_pos = self.code_text.index(tk.INSERT)
            self.code_text.insert(cursor_pos, bracket_pairs[event.char])
            self.code_text.mark_set(tk.INSERT, cursor_pos)
            self.update_line_numbers()
            self.highlight_syntax()
    
    def draw_indent_guides(self):
        """Draw vertical indent guide lines like VS Code"""
        self.code_text.tag_remove('indent_guide', '1.0', tk.END)
        
        lines = self.code_text.get('1.0', tk.END).split('\n')
        for line_num, line in enumerate(lines, 1):
            if not line.strip():
                continue
            
            # Count leading spaces
            leading_spaces = len(line) - len(line.lstrip())
            
            # Draw a guide every 4 spaces
            for i in range(4, leading_spaces + 1, 4):
                try:
                    self.code_text.tag_add('indent_guide', f"{line_num}.{i-1}", f"{line_num}.{i}")
                except:
                    pass
        
    def insert_default_code(self):
        """Insert default template code"""
        default_code = """main() {
    #Write Code here:
    out("Welcome to Celerity Compiler");
}
"""
        self.code_text.insert('1.0', default_code)
        self.update_line_numbers()
        self.highlight_syntax()
        self.draw_indent_guides()
        
    def on_key_release(self, event=None):
        """Update UI elements on key release"""
        self.update_line_numbers()
        self.highlight_syntax()
        self.draw_indent_guides()
        
    def on_scroll(self, event=None):
        """Update line numbers on scroll"""
        self.update_line_numbers()
        
    def update_line_numbers(self):
        """Update line number display"""
        line_count = self.code_text.get('1.0', 'end-1c').count('\n') + 1
        line_numbers_string = "\n".join(str(i) for i in range(1, line_count + 1))
        
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete('1.0', tk.END)
        self.line_numbers.insert('1.0', line_numbers_string)
        self.line_numbers.config(state=tk.DISABLED)
        
    def highlight_syntax(self):
        """Apply syntax highlighting to code editor"""
        # Remove all tags
        for tag in ['comment', 'keyword', 'string', 'number']:
            self.code_text.tag_remove(tag, '1.0', tk.END)
        
        code = self.code_text.get('1.0', tk.END)
        
        # Keywords based on your lexer
        keywords = ['bool', 'const', 'deci', 'def', 'do', 'else', 'elseif', 'false', 
                   'for', 'function', 'if', 'in', 'is', 'isnot', 'main', 'match', 
                   'num', 'out', 'pick', 'resume', 'return', 'single', 'split', 
                   'struct', 'true', 'vacant', 'while', 'word']
        
        # Highlight comments (starting with #)
        for match in re.finditer(r'#.*', code):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.code_text.tag_add('comment', start, end)
        
        # Highlight strings
        for match in re.finditer(r'"[^"]*"', code):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.code_text.tag_add('string', start, end)
        
        # Highlight single-quoted strings
        for match in re.finditer(r"'[^']*'", code):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.code_text.tag_add('string', start, end)
        
        # Highlight numbers
        for match in re.finditer(r'\b\d+\.?\d*\b', code):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.code_text.tag_add('number', start, end)
        
        # Highlight keywords
        for keyword in keywords:
            pattern = r'\b' + keyword + r'\b'
            for match in re.finditer(pattern, code):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.code_text.tag_add('keyword', start, end)
    
    def switch_view(self, view):
        """Switch between different output views"""
        self.current_view = view
        
        # Reset all button colors
        self.lexical_btn.config(bg=self.colors['bg_light'])
        self.syntax_btn.config(bg=self.colors['bg_light'])
        self.semantic_btn.config(bg=self.colors['bg_light'])
        
        # Highlight selected button
        if view == 'lexical':
            self.lexical_btn.config(bg=self.colors['orange'])
            self.display_lexical_output()
        elif view == 'syntax':
            self.syntax_btn.config(bg=self.colors['orange'])
            self.display_syntax_output()
        elif view == 'semantic':
            self.semantic_btn.config(bg=self.colors['pink'])
            self.display_semantic_output()
    
    def run_code(self):
        """Run the lexical analysis in a separate thread"""
        if self.is_running:
            messagebox.showwarning("Already Running", "Compilation is already in progress!")
            return
        
        # Disable the run button and enable stop button
        self.is_running = True
        self.run_button.config(state=tk.DISABLED, text="⏳ Running...")
        self.stop_button.config(state=tk.NORMAL)
        
        # Clear previous outputs
        self.output_text.delete('1.0', tk.END)
        self.error_text.delete('1.0', tk.END)
        self.terminal_text.delete('1.0', tk.END)
        
        # Get current code from editor
        code = self.code_text.get('1.0', 'end-1c')
        
        # Terminal output
        self.terminal_text.insert(tk.END, "Running Celerity Compiler...\n")
        self.terminal_text.insert(tk.END, "=" * 50 + "\n\n")
        
        # Run lexer in a separate thread with timeout
        self.lexer_thread = threading.Thread(target=self._run_lexer, args=(code,), daemon=True)
        self.lexer_thread.start()
    
    def stop_code(self):
        """Stop the running compilation"""
        self.is_running = False
        self.stop_button.config(state=tk.DISABLED)
        self.run_button.config(state=tk.NORMAL, text="▶ Run")
        
        self.terminal_text.insert(tk.END, "\n⏹ Compilation stopped by user.\n")
        self.terminal_text.see(tk.END)
    
    def _run_lexer(self, code):
        """Execute lexical analysis in background thread"""
        try:
            # Check if stop was requested
            if not self.is_running:
                self.root.after(0, self._compilation_cancelled)
                return
            
            # Set a timeout for lexer execution (10 seconds)
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError("Lexer execution timed out after 10 seconds")
            
            # Run lexical analysis with timeout protection
            tokens, errors = self.lexer.lexeme(code)
            
            # Check again if stop was requested
            if not self.is_running:
                self.root.after(0, self._compilation_cancelled)
                return
            
            # Update GUI from main thread
            self.root.after(0, self._update_results, tokens, errors)
            
        except TimeoutError as e:
            self.root.after(0, self._update_error, str(e))
        except Exception as e:
            # Handle errors
            self.root.after(0, self._update_error, str(e))
    
    def _compilation_cancelled(self):
        """Handle cancelled compilation"""
        self.terminal_text.insert(tk.END, "Compilation cancelled.\n")
        self.is_running = False
        self.run_button.config(state=tk.NORMAL, text="▶ Run")
        self.stop_button.config(state=tk.DISABLED)
    
    def _update_results(self, tokens, errors):
        """Update GUI with lexical analysis results"""
        self.tokens = tokens
        self.errors = errors
        
        # Display based on current view
        if self.current_view == 'lexical':
            self.display_lexical_output()
        elif self.current_view == 'syntax':
            self.display_syntax_output()
        elif self.current_view == 'semantic':
            self.display_semantic_output()
        
        # Display errors
        if errors:
            self.error_text.insert(tk.END, "LEXICAL ERRORS:\n")
            self.error_text.insert(tk.END, "=" * 50 + "\n\n")
            for error in errors:
                self.error_text.insert(tk.END, f"❌ {error}\n")
            self.terminal_text.insert(tk.END, f"\nCompilation failed with {len(errors)} error(s).\n")
        else:
            self.error_text.insert(tk.END, "✓ No errors found!\n")
            self.terminal_text.insert(tk.END, "\nCompilation successful!\n")
        
        # Re-enable the run button and disable stop button
        self.is_running = False
        self.run_button.config(state=tk.NORMAL, text="▶ Run")
        self.stop_button.config(state=tk.DISABLED)
    
    def _update_error(self, error_msg):
        """Display error message in GUI"""
        self.error_text.insert(tk.END, f"ERROR: {error_msg}\n")
        self.terminal_text.insert(tk.END, f"\nCompilation failed: {error_msg}\n")
        self.is_running = False
        self.run_button.config(state=tk.NORMAL, text="▶ Run")
        self.stop_button.config(state=tk.DISABLED)
    
    def display_lexical_output(self):
        """Display lexical analysis tokens in table format"""
        self.output_text.delete('1.0', tk.END)
        
        if self.tokens:
            # Header
            self.output_text.insert(tk.END, "LEXICAL ANALYSIS - TOKENS\n")
            self.output_text.insert(tk.END, "=" * 64 + "\n\n")
            
            # Table header
            header = f"{'Lexeme':<20} | {'Token':<20} | {'Line':<6} | {'Col':<6}\n"
            separator = "-" * 64 + "\n"
            
            self.output_text.insert(tk.END, header)
            self.output_text.insert(tk.END, separator)
            
            # Table rows
            for token in self.tokens:
                lexeme, token_type, line, column = token
                
                # Truncate long lexemes and add ellipsis
                display_lexeme = lexeme if len(lexeme) <= 18 else lexeme[:15] + "..."
                
                row = f"{display_lexeme:<20} | {token_type:<20} | {line:<6} | {column:<6}\n"
                self.output_text.insert(tk.END, row)
            
            # Summary
            self.output_text.insert(tk.END, "\n" + separator)
            self.output_text.insert(tk.END, f"Total Tokens: {len(self.tokens)}\n")
        else:
            self.output_text.insert(tk.END, "No tokens to display. Click 'Run' to analyze code.")
    
    def display_syntax_output(self):
        """Display syntax analysis results"""
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, "SYNTAX ANALYSIS\n")
        self.output_text.insert(tk.END, "=" * 64 + "\n\n")
        self.output_text.insert(tk.END, "Coming soon...\n")
    
    def display_semantic_output(self):
        """Display semantic analysis results"""
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, "SEMANTIC ANALYSIS\n")
        self.output_text.insert(tk.END, "=" * 64 + "\n\n")
        self.output_text.insert(tk.END, "Coming soon...\n")


def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = CelerityCompiler(root)
    root.mainloop()


if __name__ == "__main__":
    main()





































# import tkinter as tk
# from tkinter import ttk, scrolledtext, messagebox
# from PIL import Image, ImageTk
# import re
# import threading
# from lexer import Lexer  # Import your lexer


# class CelerityCompiler:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Celerity Compiler")
#         self.root.geometry("1400x900")
#         self.root.configure(bg="#1e1e1e")
        
#         # Color palette from logo
#         self.colors = {
#             'bg_dark': '#1e1e1e',
#             'bg_medium': '#252526',
#             'bg_light': '#2d2d30',
#             'orange': '#FF6B35',
#             'pink': '#FF2E63',
#             'text_white': '#ffffff',
#             'text_gray': '#858585',
#             'comment_green': '#6A9955',
#             'keyword_orange': '#FF6B35',
#             'string_brown': '#CE9178',
#             'number_blue': '#B5CEA8',
#             'line_numbers': '#858585',
#             'indent_line': '#404040'
#         }
        
#         self.current_view = 'lexical'  # Track current output view
#         self.lexer = Lexer()
#         self.tokens = []
#         self.errors = []
        
#         self.create_widgets()
#         self.insert_default_code()
        
#     def create_widgets(self):
#         # Header Frame
#         header_frame = tk.Frame(self.root, bg=self.colors['bg_medium'], height=60)
#         header_frame.pack(fill=tk.X, side=tk.TOP)
#         header_frame.pack_propagate(False)
        
#         # Logo placeholder
#         try:
#             logo_image = Image.open("icon/Celerity.png")
#             logo_image = logo_image.resize((45, 45), Image.Resampling.LANCZOS)
#             self.logo_photo = ImageTk.PhotoImage(logo_image)
#             logo_label = tk.Label(header_frame, image=self.logo_photo, bg=self.colors['bg_medium'])
#             logo_label.pack(side=tk.LEFT, padx=15, pady=7)
#         except Exception as e:
#             print(f"Logo not found: {e}")
        
#         # Celerity Name
#         name_label = tk.Label(
#             header_frame, 
#             text="Celerity", 
#             font=("Segoe UI", 24, "bold"),
#             fg=self.colors['orange'],
#             bg=self.colors['bg_medium']
#         )
#         name_label.pack(side=tk.LEFT, padx=(15, 0), pady=7)
        
#         # Main Container
#         main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
#         main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
#         # Left Panel (Code Editor)
#         left_panel = tk.Frame(main_container, bg=self.colors['bg_dark'])
#         left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
#         # Code Editor Header
#         editor_header = tk.Frame(left_panel, bg=self.colors['bg_medium'], height=40)
#         editor_header.pack(fill=tk.X)
#         editor_header.pack_propagate(False)
        
#         editor_label = tk.Label(
#             editor_header,
#             text="Code Editor",
#             font=("Segoe UI", 11, "bold"),
#             fg=self.colors['text_white'],
#             bg=self.colors['bg_medium']
#         )
#         editor_label.pack(side=tk.LEFT, padx=15, pady=8)
        
#         # Run Button with play icon
#         self.run_button = tk.Button(
#             editor_header,
#             text="▶ Run",
#             font=("Segoe UI", 10, "bold"),
#             fg=self.colors['text_white'],
#             bg=self.colors['orange'],
#             activebackground=self.colors['pink'],
#             activeforeground=self.colors['text_white'],
#             relief=tk.FLAT,
#             cursor="hand2",
#             padx=20,
#             pady=5,
#             command=self.run_code
#         )
#         self.run_button.pack(side=tk.RIGHT, padx=15, pady=5)
        
#         # Code Editor Frame with line numbers
#         editor_container = tk.Frame(left_panel, bg=self.colors['bg_dark'])
#         editor_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
#         # Line Numbers
#         self.line_numbers = tk.Text(
#             editor_container,
#             width=4,
#             padx=5,
#             pady=10,
#             font=("Consolas", 11),
#             bg=self.colors['bg_medium'],
#             fg=self.colors['line_numbers'],
#             state=tk.DISABLED,
#             relief=tk.FLAT,
#             wrap=tk.NONE
#         )
#         self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
#         # Code Text Area
#         self.code_text = tk.Text(
#             editor_container,
#             font=("Consolas", 11),
#             bg=self.colors['bg_light'],
#             fg=self.colors['text_white'],
#             insertbackground=self.colors['text_white'],
#             selectbackground='#3E3E42',  # Light grey selection
#             selectforeground=self.colors['text_white'],
#             relief=tk.FLAT,
#             wrap=tk.NONE,
#             padx=10,
#             pady=10,
#             undo=True,
#             tabs=('1c', '2c', '3c', '4c')
#         )
#         self.code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
#         # Scrollbars for code editor
#         code_scrollbar_y = ttk.Scrollbar(editor_container, command=self.code_text.yview)
#         code_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
#         self.code_text.config(yscrollcommand=code_scrollbar_y.set)
        
#         code_scrollbar_x = ttk.Scrollbar(left_panel, orient=tk.HORIZONTAL, command=self.code_text.xview)
#         code_scrollbar_x.pack(fill=tk.X)
#         self.code_text.config(xscrollcommand=code_scrollbar_x.set)
        
#         # Bind events for syntax highlighting, line numbers, and indent guides
#         self.code_text.bind('<KeyRelease>', self.on_key_release)
#         self.code_text.bind('<MouseWheel>', self.on_scroll)
#         self.code_text.bind('<Tab>', self.handle_tab)
#         self.code_text.bind('<Return>', self.handle_return)
#         self.code_text.bind('<BackSpace>', self.handle_backspace)
#         self.code_text.bind('<Key>', self.handle_bracket_autocompletion)
        
#         # Right Panel (Output)
#         right_panel = tk.Frame(main_container, bg=self.colors['bg_dark'], width=500)
#         right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
#         right_panel.pack_propagate(False)
        
#         # Output Header with buttons
#         output_header = tk.Frame(right_panel, bg=self.colors['bg_medium'], height=40)
#         output_header.pack(fill=tk.X)
#         output_header.pack_propagate(False)
        
#         # View Buttons
#         self.lexical_btn = tk.Button(
#             output_header,
#             text="Lexical",
#             font=("Segoe UI", 9, "bold"),
#             fg=self.colors['text_white'],
#             bg=self.colors['orange'],
#             activebackground=self.colors['orange'],
#             relief=tk.FLAT,
#             cursor="hand2",
#             padx=15,
#             pady=3,
#             command=lambda: self.switch_view('lexical')
#         )
#         self.lexical_btn.pack(side=tk.LEFT, padx=(15, 3), pady=5)
        
#         self.syntax_btn = tk.Button(
#             output_header,
#             text="Syntax",
#             font=("Segoe UI", 9, "bold"),
#             fg=self.colors['text_white'],
#             bg=self.colors['bg_light'],
#             activebackground=self.colors['orange'],
#             relief=tk.FLAT,
#             cursor="hand2",
#             padx=15,
#             pady=3,
#             command=lambda: self.switch_view('syntax')
#         )
#         self.syntax_btn.pack(side=tk.LEFT, padx=3, pady=5)
        
#         self.semantic_btn = tk.Button(
#             output_header,
#             text="Semantic",
#             font=("Segoe UI", 9, "bold"),
#             fg=self.colors['text_white'],
#             bg=self.colors['bg_light'],
#             activebackground=self.colors['pink'],
#             relief=tk.FLAT,
#             cursor="hand2",
#             padx=15,
#             pady=3,
#             command=lambda: self.switch_view('semantic')
#         )
#         self.semantic_btn.pack(side=tk.LEFT, padx=3, pady=5)
        
#         # Output Text Area
#         self.output_text = scrolledtext.ScrolledText(
#             right_panel,
#             font=("Consolas", 10),
#             bg=self.colors['bg_light'],
#             fg=self.colors['text_white'],
#             relief=tk.FLAT,
#             wrap=tk.WORD,
#             padx=10,
#             pady=10
#         )
#         self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
#         # Bottom Panel (Errors/Terminal/Output)
#         bottom_panel = tk.Frame(self.root, bg=self.colors['bg_dark'], height=200)
#         bottom_panel.pack(fill=tk.BOTH, side=tk.BOTTOM, padx=5, pady=(0, 5))
#         bottom_panel.pack_propagate(False)
        
#         # Bottom Tabs
#         bottom_notebook = ttk.Notebook(bottom_panel)
#         bottom_notebook.pack(fill=tk.BOTH, expand=True)
        
#         # Style for notebook
#         style = ttk.Style()
#         style.theme_use('default')
#         style.configure('TNotebook', background=self.colors['bg_medium'], borderwidth=0)
#         style.configure('TNotebook.Tab', background=self.colors['bg_light'], 
#                        foreground=self.colors['text_white'], padding=[20, 5])
#         style.map('TNotebook.Tab', background=[('selected', self.colors['bg_medium'])],
#                  foreground=[('selected', self.colors['orange'])])
        
#         # Error Display Tab
#         error_frame = tk.Frame(bottom_notebook, bg=self.colors['bg_light'])
#         self.error_text = scrolledtext.ScrolledText(
#             error_frame,
#             font=("Consolas", 9),
#             bg=self.colors['bg_light'],
#             fg='#F48771',
#             relief=tk.FLAT,
#             wrap=tk.WORD,
#             padx=10,
#             pady=10
#         )
#         self.error_text.pack(fill=tk.BOTH, expand=True)
#         bottom_notebook.add(error_frame, text="Errors")
        
#         # Terminal Tab
#         terminal_frame = tk.Frame(bottom_notebook, bg=self.colors['bg_light'])
#         terminal_layout = tk.Frame(terminal_frame, bg=self.colors['bg_light'])
#         terminal_layout.pack(fill=tk.BOTH, expand=True)
        
#         self.terminal_text = scrolledtext.ScrolledText(
#             terminal_layout,
#             font=("Consolas", 9),
#             bg=self.colors['bg_light'],
#             fg=self.colors['text_white'],
#             relief=tk.FLAT,
#             wrap=tk.WORD,
#             padx=10,
#             pady=10
#         )
#         self.terminal_text.pack(fill=tk.BOTH, expand=True)
        
#         # Input field and submit button
#         input_container = tk.Frame(terminal_layout, bg=self.colors['bg_light'])
#         input_container.pack(fill=tk.X, padx=5, pady=5)
        
#         self.input_field = tk.Entry(
#             input_container,
#             font=("Consolas", 10),
#             bg=self.colors['bg_medium'],
#             fg=self.colors['text_white'],
#             insertbackground=self.colors['text_white'],
#             relief=tk.FLAT
#         )
#         self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
#         self.input_field.bind('<Return>', lambda e: self.submit_input())
        
#         self.submit_button = tk.Button(
#             input_container,
#             text="Submit",
#             font=("Segoe UI", 9, "bold"),
#             fg=self.colors['text_white'],
#             bg=self.colors['orange'],
#             activebackground=self.colors['pink'],
#             relief=tk.FLAT,
#             cursor="hand2",
#             padx=15,
#             pady=3,
#             command=self.submit_input
#         )
#         self.submit_button.pack(side=tk.RIGHT)
        
#         bottom_notebook.add(terminal_frame, text="Terminal")
        
#         # Output Code Tab
#         output_code_frame = tk.Frame(bottom_notebook, bg=self.colors['bg_light'])
#         self.output_code_text = scrolledtext.ScrolledText(
#             output_code_frame,
#             font=("Consolas", 9),
#             bg=self.colors['bg_light'],
#             fg=self.colors['text_white'],
#             relief=tk.FLAT,
#             wrap=tk.WORD,
#             padx=10,
#             pady=10
#         )
#         self.output_code_text.pack(fill=tk.BOTH, expand=True)
#         bottom_notebook.add(output_code_frame, text="Generated Code")
        
#         # Configure tags for syntax highlighting
#         self.code_text.tag_configure('comment', foreground=self.colors['comment_green'])
#         self.code_text.tag_configure('keyword', foreground=self.colors['keyword_orange'])
#         self.code_text.tag_configure('string', foreground=self.colors['string_brown'])
#         self.code_text.tag_configure('number', foreground=self.colors['number_blue'])
#         self.code_text.tag_configure('indent_guide', foreground=self.colors['indent_line'])
    
#     def submit_input(self):
#         """Handle user input submission"""
#         user_input = self.input_field.get()
#         if user_input:
#             self.terminal_text.insert(tk.END, f"> {user_input}\n")
#             self.terminal_text.see(tk.END)
#             self.input_field.delete(0, tk.END)
#             # Process the input as needed for your compiler
    
#     def handle_tab(self, event):
#         """Handle Tab key press for 4-space indentation"""
#         self.code_text.insert(tk.INSERT, "    ")
#         self.update_line_numbers()
#         self.highlight_syntax()
#         self.draw_indent_guides()
#         return "break"
    
#     def handle_return(self, event):
#         """Handle Return key press for auto-indentation"""
#         cursor_pos = self.code_text.index(tk.INSERT)
#         line_num = int(cursor_pos.split('.')[0])
#         current_line = self.code_text.get(f"{line_num}.0", f"{line_num}.end")
        
#         # Calculate current indentation
#         indent = len(current_line) - len(current_line.lstrip())
        
#         # Check if line ends with opening bracket
#         stripped_line = current_line.strip()
#         if stripped_line.endswith('{') or stripped_line.endswith('(') or stripped_line.endswith('['):
#             self.code_text.insert(tk.INSERT, "\n" + " " * (indent + 4))
#         else:
#             self.code_text.insert(tk.INSERT, "\n" + " " * indent)
        
#         self.update_line_numbers()
#         self.highlight_syntax()
#         self.draw_indent_guides()
#         return "break"
    
#     def handle_backspace(self, event):
#         """Handle Backspace to delete 4 spaces at once if at indent position"""
#         cursor_pos = self.code_text.index(tk.INSERT)
#         line_num, col_num = map(int, cursor_pos.split('.'))
        
#         if col_num >= 4:
#             # Check if the previous 4 characters are spaces
#             prev_chars = self.code_text.get(f"{line_num}.{col_num-4}", f"{line_num}.{col_num}")
#             if prev_chars == "    ":
#                 self.code_text.delete(f"{line_num}.{col_num-4}", f"{line_num}.{col_num}")
#                 self.update_line_numbers()
#                 self.highlight_syntax()
#                 self.draw_indent_guides()
#                 return "break"
#         return None
    
#     def handle_bracket_autocompletion(self, event):
#         """Handle auto-completion of brackets"""
#         bracket_pairs = {
#             '(': ')',
#             '[': ']',
#             '{': '}',
#             '"': '"',
#             "'": "'"
#         }
        
#         if event.char in bracket_pairs:
#             cursor_pos = self.code_text.index(tk.INSERT)
#             self.code_text.insert(cursor_pos, bracket_pairs[event.char])
#             self.code_text.mark_set(tk.INSERT, cursor_pos)
#             self.update_line_numbers()
#             self.highlight_syntax()
    
#     def draw_indent_guides(self):
#         """Draw vertical indent guide lines like VS Code"""
#         self.code_text.tag_remove('indent_guide', '1.0', tk.END)
        
#         lines = self.code_text.get('1.0', tk.END).split('\n')
#         for line_num, line in enumerate(lines, 1):
#             if not line.strip():
#                 continue
            
#             # Count leading spaces
#             leading_spaces = len(line) - len(line.lstrip())
            
#             # Draw a guide every 4 spaces
#             for i in range(4, leading_spaces + 1, 4):
#                 try:
#                     self.code_text.tag_add('indent_guide', f"{line_num}.{i-1}", f"{line_num}.{i}")
#                 except:
#                     pass
        
#     def insert_default_code(self):
#         """Insert default template code"""
#         default_code = """main() {
#     #Write Code here:
#     out("Welcome to Celerity Compiler");
# }"""
#         self.code_text.insert('1.0', default_code)
#         self.update_line_numbers()
#         self.highlight_syntax()
#         self.draw_indent_guides()
        
#     def on_key_release(self, event=None):
#         """Update UI elements on key release"""
#         self.update_line_numbers()
#         self.highlight_syntax()
#         self.draw_indent_guides()
        
#     def on_scroll(self, event=None):
#         """Update line numbers on scroll"""
#         self.update_line_numbers()
        
#     def update_line_numbers(self):
#         """Update line number display"""
#         line_count = self.code_text.get('1.0', 'end-1c').count('\n') + 1
#         line_numbers_string = "\n".join(str(i) for i in range(1, line_count + 1))
        
#         self.line_numbers.config(state=tk.NORMAL)
#         self.line_numbers.delete('1.0', tk.END)
#         self.line_numbers.insert('1.0', line_numbers_string)
#         self.line_numbers.config(state=tk.DISABLED)
        
#     def highlight_syntax(self):
#         """Apply syntax highlighting to code editor"""
#         # Remove all tags
#         for tag in ['comment', 'keyword', 'string', 'number']:
#             self.code_text.tag_remove(tag, '1.0', tk.END)
        
#         code = self.code_text.get('1.0', tk.END)
        
#         # Keywords based on your lexer
#         keywords = ['bool', 'const', 'deci', 'def', 'do', 'else', 'elseif', 'false', 
#                    'for', 'function', 'if', 'in', 'is', 'isnot', 'main', 'match', 
#                    'num', 'out', 'pick', 'resume', 'return', 'single', 'split', 
#                    'struct', 'true', 'vacant', 'while', 'word']
        
#         # Highlight comments (starting with #)
#         for match in re.finditer(r'#.*', code):
#             start = f"1.0+{match.start()}c"
#             end = f"1.0+{match.end()}c"
#             self.code_text.tag_add('comment', start, end)
        
#         # Highlight strings
#         for match in re.finditer(r'"[^"]*"', code):
#             start = f"1.0+{match.start()}c"
#             end = f"1.0+{match.end()}c"
#             self.code_text.tag_add('string', start, end)
        
#         # Highlight single-quoted strings
#         for match in re.finditer(r"'[^']*'", code):
#             start = f"1.0+{match.start()}c"
#             end = f"1.0+{match.end()}c"
#             self.code_text.tag_add('string', start, end)
        
#         # Highlight numbers
#         for match in re.finditer(r'\b\d+\.?\d*\b', code):
#             start = f"1.0+{match.start()}c"
#             end = f"1.0+{match.end()}c"
#             self.code_text.tag_add('number', start, end)
        
#         # Highlight keywords
#         for keyword in keywords:
#             pattern = r'\b' + keyword + r'\b'
#             for match in re.finditer(pattern, code):
#                 start = f"1.0+{match.start()}c"
#                 end = f"1.0+{match.end()}c"
#                 self.code_text.tag_add('keyword', start, end)
    
#     def switch_view(self, view):
#         """Switch between different output views"""
#         self.current_view = view
        
#         # Reset all button colors
#         self.lexical_btn.config(bg=self.colors['bg_light'])
#         self.syntax_btn.config(bg=self.colors['bg_light'])
#         self.semantic_btn.config(bg=self.colors['bg_light'])
        
#         # Highlight selected button
#         if view == 'lexical':
#             self.lexical_btn.config(bg=self.colors['orange'])
#             self.display_lexical_output()
#         elif view == 'syntax':
#             self.syntax_btn.config(bg=self.colors['orange'])
#             self.display_syntax_output()
#         elif view == 'semantic':
#             self.semantic_btn.config(bg=self.colors['pink'])
#             self.display_semantic_output()
    
#     def run_code(self):
#         """Run the lexical analysis in a separate thread"""
#         # Disable the run button to prevent multiple clicks
#         self.run_button.config(state=tk.DISABLED, text="⏳ Running...")
        
#         # Clear previous outputs
#         self.output_text.delete('1.0', tk.END)
#         self.error_text.delete('1.0', tk.END)
#         self.terminal_text.delete('1.0', tk.END)
        
#         # Get current code from editor
#         code = self.code_text.get('1.0', 'end-1c')
        
#         # Terminal output
#         self.terminal_text.insert(tk.END, "Running Celerity Compiler...\n")
#         self.terminal_text.insert(tk.END, "=" * 50 + "\n\n")
        
#         # Run lexer in a separate thread
#         thread = threading.Thread(target=self._run_lexer, args=(code,), daemon=True)
#         thread.start()
    
#     def _run_lexer(self, code):
#         """Execute lexical analysis in background thread"""
#         try:
#             # Run lexical analysis
#             tokens, errors = self.lexer.lexeme(code)
            
#             # Update GUI from main thread
#             self.root.after(0, self._update_results, tokens, errors)
            
#         except Exception as e:
#             # Handle errors
#             self.root.after(0, self._update_error, str(e))
    
#     def _update_results(self, tokens, errors):
#         """Update GUI with lexical analysis results"""
#         self.tokens = tokens
#         self.errors = errors
        
#         # Display based on current view
#         if self.current_view == 'lexical':
#             self.display_lexical_output()
#         elif self.current_view == 'syntax':
#             self.display_syntax_output()
#         elif self.current_view == 'semantic':
#             self.display_semantic_output()
        
#         # Display errors
#         if errors:
#             self.error_text.insert(tk.END, "LEXICAL ERRORS:\n")
#             self.error_text.insert(tk.END, "=" * 50 + "\n\n")
#             for error in errors:
#                 self.error_text.insert(tk.END, f"❌ {error}\n")
#             self.terminal_text.insert(tk.END, f"\nCompilation failed with {len(errors)} error(s).\n")
#         else:
#             self.error_text.insert(tk.END, "✓ No errors found!\n")
#             self.terminal_text.insert(tk.END, "\nCompilation successful!\n")
        
#         # Re-enable the run button
#         self.run_button.config(state=tk.NORMAL, text="▶ Run")
    
#     def _update_error(self, error_msg):
#         """Display error message in GUI"""
#         self.error_text.insert(tk.END, f"ERROR: {error_msg}\n")
#         self.terminal_text.insert(tk.END, f"\nCompilation failed: {error_msg}\n")
#         self.run_button.config(state=tk.NORMAL, text="▶ Run")
    
#     def display_lexical_output(self):
#         """Display lexical analysis tokens in table format"""
#         self.output_text.delete('1.0', tk.END)
        
#         if self.tokens:
#             # Header
#             self.output_text.insert(tk.END, "LEXICAL ANALYSIS - TOKENS\n")
#             self.output_text.insert(tk.END, "=" * 50 + "\n\n")
            
#             # Table header
#             header = f"{'Lexeme':<20} | {'Token':<20} | {'Line':<6} | {'Col':<6}\n"
#             separator = "-" * 70 + "\n"
            
#             self.output_text.insert(tk.END, header)
#             self.output_text.insert(tk.END, separator)
            
#             # Table rows
#             for token in self.tokens:
#                 lexeme, token_type, line, column = token
                
#                 # Truncate long lexemes and add ellipsis
#                 display_lexeme = lexeme if len(lexeme) <= 18 else lexeme[:15] + "..."
                
#                 row = f"{display_lexeme:<20} | {token_type:<20} | {line:<6} | {column:<6}\n"
#                 self.output_text.insert(tk.END, row)
            
#             # Summary
#             self.output_text.insert(tk.END, "\n" + separator)
#             self.output_text.insert(tk.END, f"Total Tokens: {len(self.tokens)}\n")
#         else:
#             self.output_text.insert(tk.END, "No tokens to display. Click 'Run' to analyze code.")
    
#     def display_syntax_output(self):
#         """Display syntax analysis results"""
#         self.output_text.delete('1.0', tk.END)
#         self.output_text.insert(tk.END, "SYNTAX ANALYSIS\n")
#         self.output_text.insert(tk.END, "=" * 50 + "\n\n")
#         self.output_text.insert(tk.END, "Coming soon...\n")
    
#     def display_semantic_output(self):
#         """Display semantic analysis results"""
#         self.output_text.delete('1.0', tk.END)
#         self.output_text.insert(tk.END, "SEMANTIC ANALYSIS\n")
#         self.output_text.insert(tk.END, "=" * 50 + "\n\n")
#         self.output_text.insert(tk.END, "Coming soon...\n")


# def main():
#     """Main entry point for the application"""
#     root = tk.Tk()
#     app = CelerityCompiler(root)
#     root.mainloop()


# if __name__ == "__main__":
#     main()
