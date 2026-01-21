import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QLabel,
    QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QSplitter, QPlainTextEdit,
    QHBoxLayout, QGridLayout
)
from PyQt5.QtGui import QColor, QPainter, QFont, QTextFormat, QSyntaxHighlighter, QTextCharFormat, QTextCursor, QIcon, QPixmap
from PyQt5.QtCore import Qt, QRect, QSize, QRegExp

# Import your modules
from lexer import Lexer
import CFG


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent.document())

        # Define text styles
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor("#FF2222"))  # Red
        self.keyword_format.setFontWeight(QFont.Bold)

        self.datatype_format = QTextCharFormat()
        self.datatype_format.setForeground(QColor("#007960"))  # Cyan

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#6A9955"))  # Green
        self.comment_format.setFontItalic(True)

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#CE9178"))  # Orange

        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor("#202000"))  # Light green

        # Define patterns (based on your grammar)
        keywords = ["if", "else", "elseif", "for", "while", "do", "function", 
                   "return", "main", "vacant", "const", "struct", "match", 
                   "pick", "def", "split", "in", "out", "is", "isnot",
                   "true", "false"]
        
        datatypes = ["num", "deci", "word", "single", "bool"]
        
        self.keyword_pattern = r"\b(" + "|".join(keywords) + r")\b"
        self.datatype_pattern = r"\b(" + "|".join(datatypes) + r")\b"
        self.number_pattern = r"\b\d+(\.\d+)?\b"
        
        # Comment patterns
        self.comment_start = QRegExp(r"#\*")
        self.comment_end = QRegExp(r"\*#")
        self.single_comment = QRegExp(r"#[^*].*")
        
        # String patterns
        self.double_quote_pattern = QRegExp(r'"[^"]*"')
        self.single_quote_pattern = QRegExp(r"'[^']*'")

    def highlightBlock(self, text):
        # Track string positions to avoid highlighting keywords inside them
        string_ranges = []
        
        # Handle multi-line comments first
        self.setCurrentBlockState(0)
        
        # FIRST: Collect string positions BEFORE processing anything else
        for pattern in [self.double_quote_pattern, self.single_quote_pattern]:
            index = 0
            while index >= 0:
                index = pattern.indexIn(text, index)
                if index >= 0:
                    length = pattern.matchedLength()
                    string_ranges.append((index, index + length))
                    index += length
        
        # Helper function to check if position is inside a string
        def is_in_string(pos):
            for start, end in string_ranges:
                if start <= pos < end:
                    return True
            return False
        
        # NOW handle multi-line comments (skip if in string)
        start_index = 0
        if self.previousBlockState() != 1:
            start_index = self.comment_start.indexIn(text)
        
        while start_index >= 0:
            if not is_in_string(start_index):
                end_index = self.comment_end.indexIn(text, start_index)
                
                if end_index == -1:
                    self.setCurrentBlockState(1)
                    comment_length = len(text) - start_index
                else:
                    comment_length = end_index - start_index + self.comment_end.matchedLength()
                
                self.setFormat(start_index, comment_length, self.comment_format)
                start_index = self.comment_start.indexIn(text, start_index + comment_length)
            else:
                start_index = self.comment_start.indexIn(text, start_index + 1)
        
        # Skip other highlighting if we're in a comment block
        if self.currentBlockState() == 1:
            return
        
        # Single-line comments (skip if in string)
        comment_index = self.single_comment.indexIn(text)
        while comment_index >= 0 and is_in_string(comment_index):
            comment_index = self.single_comment.indexIn(text, comment_index + 1)
        
        if comment_index >= 0:
            self.setFormat(comment_index, len(text) - comment_index, self.comment_format)
            text_to_process = text[:comment_index]
        else:
            text_to_process = text
        
        # Keywords (skip if inside strings)
        keyword_regex = QRegExp(self.keyword_pattern)
        index = 0
        while index >= 0:
            index = keyword_regex.indexIn(text_to_process, index)
            if index >= 0:
                length = keyword_regex.matchedLength()
                if not is_in_string(index):
                    self.setFormat(index, length, self.keyword_format)
                index += length
        
        # Data types (skip if inside strings)
        datatype_regex = QRegExp(self.datatype_pattern)
        index = 0
        while index >= 0:
            index = datatype_regex.indexIn(text_to_process, index)
            if index >= 0:
                length = datatype_regex.matchedLength()
                if not is_in_string(index):
                    self.setFormat(index, length, self.datatype_format)
                index += length
        
        # Numbers (skip if inside strings)
        number_regex = QRegExp(self.number_pattern)
        index = 0
        while index >= 0:
            index = number_regex.indexIn(text_to_process, index)
            if index >= 0:
                length = number_regex.matchedLength()
                if not is_in_string(index):
                    self.setFormat(index, length, self.number_format)
                index += length
        
        # Apply string formatting LAST to override any previous formatting
        for pattern in [self.double_quote_pattern, self.single_quote_pattern]:
            index = 0
            while index >= 0:
                index = pattern.indexIn(text_to_process, index)
                if index >= 0:
                    length = pattern.matchedLength()
                    self.setFormat(index, length, self.string_format)
                    index += length


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setStyleSheet("background: #D4C4B0; color: #666;")

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), QColor("#D4C4B0"))

        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
        bottom = top + self.editor.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor("#666"))
                painter.setFont(QFont("Consolas", 12))
                painter.drawText(0, int(top), self.width() - 5, 
                               self.editor.fontMetrics().height(), 
                               Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.editor.blockBoundingRect(block).height()
            block_number += 1


class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Consolas", 14))
        self.setStyleSheet("""
            QPlainTextEdit {
                background: #E8DCC8;
                color: #333;
                border: 2px solid #8B7355;
                padding-left: 5px;
            }
        """)
        
        # Set tab stop width to 2 spaces worth of width
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * 2)
        
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.update_line_number_area_width()
        
        self.highlighter = SyntaxHighlighter(self)

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), 
                                        self.line_number_area.width(), 
                                        rect.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), 
                                                self.line_number_area_width(), 
                                                cr.height()))


class CelerityCompiler(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lexer = Lexer()
        self.tokens = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Celerity Compiler")
        self.setGeometry(100, 100, 1500, 850)
        self.setStyleSheet("background-color: #DFC7A8;")

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        main_widget.setLayout(main_layout)

        # Header
        header = self.create_header()
        main_layout.addWidget(header)

        # Content area with splitters
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Left side (Code Editor + Terminal)
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)
        left_widget.setLayout(left_layout)

        # Code Editor header with label and buttons
        editor_header = QWidget()
        editor_header.setStyleSheet("background: transparent;")
        editor_header_layout = QHBoxLayout()
        editor_header_layout.setContentsMargins(0, 0, 0, 5)
        editor_header_layout.setSpacing(10)
        editor_header.setLayout(editor_header_layout)
        
        editor_label = QLabel("Code Editor")
        editor_label.setStyleSheet("""
            color: #333;
            font-weight: bold;
            font-size: 12pt;
            background: transparent;
        """)
        editor_header_layout.addWidget(editor_label)
        editor_header_layout.addStretch()
        
        self.stop_btn = QPushButton("⬛ Stop")
        self.run_btn = QPushButton("▶ Run")
        
        for btn in [self.stop_btn, self.run_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background: #D2691E;
                    color: white;
                    border: 2px solid #A0522D;
                    padding: 8px 25px;
                    font-weight: bold;
                    font-size: 10pt;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background: #CD853F;
                }
            """)
        
        self.run_btn.clicked.connect(self.run_code)
        self.stop_btn.clicked.connect(self.stop_and_refresh)
        editor_header_layout.addWidget(self.stop_btn)
        editor_header_layout.addWidget(self.run_btn)
        
        left_layout.addWidget(editor_header)

        # Code editor
        self.code_editor = CodeEditor()

        # DEFAULT CODE APPEARS HERE
        self.code_editor.setPlainText(
            'main(){\n'
            '  #Welcome To Celerity Compiler!\n'
            '}\n'
        )
        left_layout.addWidget(self.code_editor, stretch=3)

        # Terminal header with tabs
        terminal_header = QWidget()
        terminal_header.setStyleSheet("background: transparent;")
        terminal_header_layout = QHBoxLayout()
        terminal_header_layout.setContentsMargins(0, 5, 0, 0)
        terminal_header_layout.setSpacing(5)
        terminal_header.setLayout(terminal_header_layout)
        
        # Terminal tabs
        self.terminal_btn = QPushButton("Terminal")
        self.generate_code_btn = QPushButton("Generate Code")
        
        for btn in [self.terminal_btn, self.generate_code_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background: #C8B5A0;
                    color: #333;
                    border: 2px solid #8B7355;  
                    padding: 6px 20px;
                    font-size: 9pt;
                    border-radius: 5px;
                    border-top-left-radius: 5px;
                    border-top-right-radius: 5px;
                }
                QPushButton:hover {
                    background: #D4C4B0;
                }
            """)
        
        # Connect tab button clicks
        self.terminal_btn.clicked.connect(self.show_terminal_view)
        self.generate_code_btn.clicked.connect(self.show_generate_code_view)
        
        terminal_header_layout.addWidget(self.terminal_btn)
        terminal_header_layout.addWidget(self.generate_code_btn)
        terminal_header_layout.addStretch()
        left_layout.addWidget(terminal_header)

        # Terminal
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet("""
            QTextEdit {
                background: #E8DCC8;
                color: #333;
                border: 2px solid #8B7355;
                font-family: Consolas;
                font-size: 9pt;
                padding: 8px;
            }
        """)
        left_layout.addWidget(self.terminal, stretch=2)
        
        # Track current view
        self.current_terminal_view = "terminal"

        content_splitter.addWidget(left_widget)

        # Right side (Analysis results)
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(8)
        right_widget.setLayout(right_layout)

        # Analysis buttons
        analysis_layout = QHBoxLayout()
        analysis_layout.setSpacing(8)
        analysis_layout.setContentsMargins(0, 0, 0, 5)
        
        self.lexical_btn = QPushButton("lexical")
        self.syntax_btn = QPushButton("syntax")
        self.semantic_btn = QPushButton("semantic")
        
        for btn in [self.lexical_btn, self.syntax_btn, self.semantic_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background: #B8A890;
                    color: #333;
                    border: 2px solid #8B7355;
                    padding: 8px 25px;
                    border-radius: 5px;
                    font-weight: normal;
                    font-size: 10pt;
                }
                QPushButton:hover {
                    background: #C8B5A0;
                }
            """)
        
        self.lexical_btn.clicked.connect(self.show_lexical_analysis)
        self.syntax_btn.clicked.connect(self.show_syntax_analysis)
        self.semantic_btn.clicked.connect(self.show_semantic_analysis)
        
        analysis_layout.addWidget(self.lexical_btn)
        analysis_layout.addWidget(self.syntax_btn)
        analysis_layout.addWidget(self.semantic_btn)
        analysis_layout.addStretch()
        right_layout.addLayout(analysis_layout)

        # Results table
        self.results_table = QTableWidget()
        self.results_table.setStyleSheet("""
            QTableWidget {
                background: #E8DCC8;
                border: 2px solid #8B7355;
                gridline-color: #C8B5A0;
            }
            QHeaderView::section {
                background: #C19A6B;
                color: #333;
                padding: 8px;
                border: 1px solid #8B7355;
                font-weight: bold;
                font-size: 10pt;
            }
            QTableWidget::item {
                padding: 5px;
                color: #333;
            }
        """)
        right_layout.addWidget(self.results_table)

        content_splitter.addWidget(right_widget)
        content_splitter.setStretchFactor(0, 2)
        content_splitter.setStretchFactor(1, 1)

        main_layout.addWidget(content_splitter)

    def create_header(self):
        header = QWidget()
        header.setStyleSheet("""
            background: #E8D4B8;
            border: none;
        """)
        header.setFixedHeight(120)

        # Main layout for header
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 30, 20, 30)
        
        # Left side - Logo and Title
        left_side = QWidget()
        left_layout = QHBoxLayout(left_side)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)
        
        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("icon/Celerity.png")
        logo_label.setPixmap(pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setStyleSheet("""
            color: #E63946;
            font-size: 32pt;
            font-weight: bold;
            border: none;                     
        """)
        left_layout.addWidget(logo_label)
        
        # Title
        title_label = QLabel("Celerity")
        title_label.setStyleSheet("""
            color: #E63946;
            font-size: 28pt;
            font-weight: bold;
            font-family: Arial;
            border: none;
        """)
        left_layout.addWidget(title_label)
        
        header_layout.addWidget(left_side)
        header_layout.addStretch()
        
        # Right side - Names in grid
        names_widget = QWidget()
        names_layout = QGridLayout(names_widget)
        names_layout.setContentsMargins(0, 0, 0, 0)
        names_layout.setSpacing(20)
        # Names on the right
        names = ["Amper ", "Enriquez ", "Habana ", "Gorme ", "Tolin ", "Valdez "]
        for i, name in enumerate(names):
            name_label = QLabel(name, header)
            name_label.setStyleSheet("""
                color: #333;
                font-size: 11pt;
                border: none;
            """)
            name_label.setAlignment(Qt.AlignCenter)
            # position names on the right manually
            names_layout.addWidget(name_label, i // 3, i % 3)
        
        header_layout.addWidget(names_widget)

        return header

    def refresh_all(self):
        """Completely refresh terminal and results table"""
        # Disable updates for better performance
        self.terminal.setUpdatesEnabled(False)
        self.results_table.setUpdatesEnabled(False)
        
        # Clear terminal completely
        self.terminal.clear()
        self.terminal.document().clear()
        self.terminal.setHtml("")
        
        # Clear results table completely
        self.results_table.clear()
        self.results_table.setRowCount(0)
        self.results_table.setColumnCount(0)
        
        # Reset tokens
        self.tokens = []
        
        # Re-enable updates
        self.terminal.setUpdatesEnabled(True)
        self.results_table.setUpdatesEnabled(True)

    def stop_and_refresh(self):
        """Stop button - clears everything"""
        self.refresh_all()
        self.terminal.setHtml("<span style='color: #666;'>Terminal cleared. Click 'Run' to execute code.</span>")

    def run_code(self):
        # COMPLETE refresh first
        self.refresh_all()
        
        # Set view to terminal when running
        self.current_terminal_view = "terminal"
        
        # Build output as list for efficiency
        output = []
        output.append("<b>Running code...</b><br>")
        
        # Get code and run lexical analysis
        code = self.code_editor.toPlainText()
        self.tokens, errors = self.lexer.lexeme(code)
        
        if errors:
            output.append("<span style='color: red;'><b>Lexical Errors:</b></span><br>")
            for error in errors:
                output.append(f"<span style='color: red;'>{error}</span><br>")
        else:
            output.append("<span style='color: green;'>✓ Lexical analysis passed</span><br>")
            
            # Run syntax analysis
            try:
                parser = CFG.LL1Parser(CFG.cfg, CFG.parse_table, CFG.follow_set)
                success, parse_errors = parser.parse(self.tokens)
                
                if success:
                    output.append("<span style='color: green;'>✓ Syntax analysis passed</span><br>")
                else:
                    output.append("<span style='color: red;'><b>Syntax Errors:</b></span><br>")
                    for error in parse_errors:
                        output.append(f"<span style='color: red;'>{error}</span><br>")
            except Exception as e:
                output.append(f"<span style='color: red;'>Syntax analysis error: {str(e)}</span><br>")
        
        # Display all output at once
        self.terminal.setHtml("".join(output))
    
    def show_terminal_view(self):
        """Switch to terminal view"""
        self.current_terminal_view = "terminal"
    
    def show_generate_code_view(self):
        """Switch to generate code view"""
        self.current_terminal_view = "generate"
        
        # Clear and show generated code view
        self.terminal.setUpdatesEnabled(False)
        self.terminal.clear()
        self.terminal.document().clear()
        self.terminal.setHtml("")
        self.terminal.setUpdatesEnabled(True)
        
        if self.tokens:
            output = []
            output.append("<b>Generated Code:</b><br>")
            output.append("# Three-address code generation coming soon...")
            self.terminal.setHtml("".join(output))
        else:
            self.terminal.setHtml("<span style='color: #666;'>Please run the code first to generate output.</span>")

    def show_lexical_analysis(self):
        code = self.code_editor.toPlainText()
        self.tokens, errors = self.lexer.lexeme(code)
        
        # Complete table refresh
        self.results_table.setUpdatesEnabled(False)
        self.results_table.clear()
        self.results_table.setRowCount(0)
        self.results_table.setColumnCount(0)
        
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["Lexeme", "Token", "Line", "Column"])
        self.results_table.setRowCount(len(self.tokens))
        
        for i, (lexeme, token, line, column) in enumerate(self.tokens):
            self.results_table.setItem(i, 0, QTableWidgetItem(str(lexeme)))
            self.results_table.setItem(i, 1, QTableWidgetItem(str(token)))
            self.results_table.setItem(i, 2, QTableWidgetItem(str(line)))
            self.results_table.setItem(i, 3, QTableWidgetItem(str(column)))
        
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setUpdatesEnabled(True)

    def show_syntax_analysis(self):
        if not self.tokens:
            self.terminal.clear()
            self.terminal.setHtml("<span style='color: red;'>Please run lexical analysis first!</span>")
            return
        
        # Complete table refresh
        self.results_table.setUpdatesEnabled(False)
        self.results_table.clear()
        self.results_table.setRowCount(0)
        self.results_table.setColumnCount(0)
        
        self.results_table.setColumnCount(1)
        self.results_table.setHorizontalHeaderLabels(["Syntax Analysis"])
        
        try:
            parser = CFG.LL1Parser(CFG.cfg, CFG.parse_table, CFG.follow_set)
            success, errors = parser.parse(self.tokens)
            
            if success:
                self.results_table.setRowCount(1)
                self.results_table.setItem(0, 0, QTableWidgetItem("✓ Syntax analysis passed - No errors found"))
            else:
                self.results_table.setRowCount(len(errors))
                for i, error in enumerate(errors):
                    self.results_table.setItem(i, 0, QTableWidgetItem(error))
        except Exception as e:
            self.results_table.setRowCount(1)
            self.results_table.setItem(0, 0, QTableWidgetItem(f"Error: {str(e)}"))
        
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setUpdatesEnabled(True)

    def show_semantic_analysis(self):
        # Complete table refresh
        self.results_table.setUpdatesEnabled(False)
        self.results_table.clear()
        self.results_table.setRowCount(0)
        self.results_table.setColumnCount(0)
        
        self.results_table.setColumnCount(1)
        self.results_table.setHorizontalHeaderLabels(["Semantic Analysis"])
        self.results_table.setRowCount(1)
        
        item = QTableWidgetItem("Coming soon...")
        item.setForeground(QColor("#666"))
        item.setFont(QFont("Arial", 12, QFont.Bold))
        self.results_table.setItem(0, 0, item)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setUpdatesEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CelerityCompiler()
    window.show()
    sys.exit(app.exec_())
