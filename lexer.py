# class Token:
#     def __init__(self, type, value, line, column):
#         self.type = type
#         self.value = value
#         self.line = line
#         self.column = column
    
#     def __repr__(self):
#         return f'Token({self.type}, {repr(self.value)}, line {self.line}, col {self.column})'
    
class Lexer: 
    def __init__(self): 
        self.errors = [] 
        self.space = {' '} 
        self.newln = {'\n', '\r'}
        self.whitespace = {' ','\n', '\t'}
        self.semicolon = {';'}
        self.colon = {':'}
        self.comma = {','}
        self.period = {'.'}
        self.zero = {'0'}
        self.number = set("123456789") 
        self.negative = {'~'}
        self.digit = set("0123456789")
        self.alphalow = set("abcdefghijklmnopqrstuvwxyz") 
        self.alphaup = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ") 
        self.alphabet = self.alphalow|self.alphaup
        self.alphadigit = self.alphabet|self.digit 
        self.bool = {'true', 'false'}
        self.oparith = {'+', '-', '*', '/', '%', '**'}
        self.opassign = {'=', '+=', '-=', '*=', '/=', '%=', '**='}
        self.oprelation = {'==', '!=', '<', '<=', '>', '>='}
        self.opunary = {'++', '--'}
        self.oplogical = {'&&', '||', '!'}
        self.delimop = {'+', '-', '*', '/', '%', '!', '&', '|', '<', '>', '=', ' '}
        self.escapeseq = {'\n', '\t'}

        ascii_chars = set("!@#$%^&*()-_=+[{]}\\|;:,<.>/?`~") | self.alphalow | self.alphaup | self.digit

        self.asciiword = ascii_chars - {'"'}   # string: everything except double quote
        self.asciisingle = ascii_chars - {"'"} # char: everything except single quote
        self.asciicom = (ascii_chars | self.whitespace) - {'#', '*'}
        self.delimword = {')', '}', '+'} | self.comma | self.semicolon | self.space | self.colon
        self.delimsingle = {'}', ')'} | self.comma | self.semicolon | self.space | self.colon
        self.delimdigit = {'}', ')', ']'} | self.space | self.delimop | self.semicolon | self.colon | self.comma | self.period
        self.delimiden = {'(', ')', '{', '}', '[', ']'} | self.space | self.delimop | self.semicolon | self.colon | self.comma | self.newln #kulang sa delimiden "{,[" nag add rin ng newln here.
        self.parspace = {'('} | self.space
        self.curspace = {'{', '}'} | self.space | self.newln
        self.semispace = self.semicolon | self.space
        self.delim1 = self.space | self.colon
        self.delim2 = {')'} | self.comma | self.space | self.semicolon
        self.delim3 = {')'} | self.alphadigit | self.semicolon | self.space  #nagdagdag aq whitespace same sa delim4&5
        self.delim4 = {'~', '('} | self.alphadigit | self.space 
        self.delim5 = {'~', '(', '+' , '-'} | self.digit | self.space
        self.delim6 = {'('} | self.alphadigit | self.space
        self.delim7 = {'~', '"', "'", '('} | self.alphadigit | self.space
        self.delim8 = {'~', '"', '(' , '{'} | self.alphadigit | self.space
        self.delim9 = {'(', ')', '!', "'", '"'} | self.alphadigit | self.space
        self.delim10 = {'{', ')', '<', '>', '=', '|', '&', '+', '-', '/', '*', '%', '"'} | self.semicolon | self.space | self.newln | self.colon | self.comma
        self.delim11 = {']'} | self.space | self.digit
        self.delim12 = {'=', '[', ')'} | self.space | self.newln | self.semicolon
        self.delim13 = {'{', "'", '"', '~'} | self.alphadigit | self.space | self.newln

        self.delim14 = {'}'} | self.semicolon | self.comma | self.alphabet | self.space | self.newln    
        self.delim15 = {'}', ')', ']'} | self.space | self.semicolon | self.comma | self.colon    
        self.delim16 = self.asciisingle | self.escapeseq | self.space
        self.delim17 = self.asciisingle | self.escapeseq | self.space
        
        
      
    def fetch_next_char(self):
        if self.position < len(self.source_code):
            char = self.source_code[self.position]
            print(f"Fetching char at pos {self.position}: {repr(char)}")  # debug print
            self.position += 1
            return char

        return None

    def peek(self):
        if self.position < len(self.source_code):
            return self.source_code[self.position]
        return None

    def step_back(self):
        if self.position > 0:
            self.position -= 1
                # For simplicity, we won't update line and column on rewind in this example.

    def lexeme(self, code):
        self.source_code = code 
        tokens = [] 
        self.position = 0 
        state = 0 
        lexeme = "" 
        line = 1 
        column = 0 
        print("Lexing started...") 

        while True: 
            char = self.fetch_next_char() 
            column += 1 

            if char is None:
                # finalize token if needed before breaking
                if lexeme:
                    tokens.append((lexeme, "unknown", line, column))
                break


            match state: 
                case 0: 

                    lexeme = "" 

                    #spaces 
                    if char in self.whitespace: 
                        if char == '\n': 
                            line += 1 
                            column = 0 
                        continue

                    # single-character tokens / galing sa state 0
                    elif char == 'b':
                        state = 1
                        lexeme += char
                    elif char == 'c':
                        state = 6
                        lexeme += char
                    elif char == 'd':
                        state = 12
                        lexeme += char
                    elif char == 'e':
                        state = 21
                        lexeme += char
                    elif char == 'f':
                        state = 29
                        lexeme += char
                    elif char == 'i':
                        state = 46
                        lexeme += char
                    elif char == 'm':
                        state = 57
                        lexeme += char
                    elif char == 'n':
                        state = 66
                        lexeme += char
                    elif char == 'o':
                        state = 70
                        lexeme += char
                    elif char == 'p':
                        state = 74
                        lexeme += char
                    elif char == 'r':
                        state = 79
                        lexeme += char
                    elif char == 's':
                        state = 91
                        lexeme += char
                    elif char == 't':
                        state = 109
                        lexeme += char
                    elif char == 'v':
                        state = 114
                        lexeme += char
                    elif char == 'w':
                        state = 121
                        lexeme += char

                     # operators / punctuators | Reserved Symbols 
                    elif char == '+':
                        state = 131
                        lexeme += char
                    elif char == '-':
                        state = 137
                        lexeme += char
                    elif char == '*':
                        state = 143
                        lexeme += char
                    elif char == '/':
                        state = 151
                        lexeme += char
                    elif char == '%':
                        state = 155
                        lexeme += char
                    elif char == '>':
                        state = 159
                        lexeme += char
                    elif char == '<':
                        state = 163
                        lexeme += char
                    elif char == '!':
                        state = 167
                        lexeme += char
                    elif char == '&':
                        state = 171
                        lexeme += char
                    elif char == '|':
                        state = 174
                        lexeme += char
                    elif char == ',':
                        state = 177
                        lexeme += char
                    elif char == ':':
                        state = 179
                        lexeme += char
                    elif char == ';':
                        state = 181
                        lexeme += char
                                            # elif char == "'":
                                            #     state = 183
                                            #     lexeme += char
                                            # elif char == "'":
                                            #     state = 185
                                            #     lexeme += char
                                            # elif char == '"':
                                            #     state = 187
                                            #     lexeme += char
                                            # elif char == '"':
                                            #     state = 189
                                            #     lexeme += char
                    elif char == '(':
                        state = 183
                        lexeme += char
                    elif char == ')':
                        state = 185
                        lexeme += char
                    elif char == '[':
                        state = 187
                        lexeme += char
                    elif char == ']':
                        state = 189
                        lexeme += char
                    elif char == '{':
                        state = 191
                        lexeme += char
                    elif char == '}':
                        state = 193
                        lexeme += char
                    elif char == '=':
                        state = 195
                        lexeme += char
                    elif char == '.':
                        state = 199
                        lexeme += char
                    elif char == '#':
                        state = 201
                        lexeme += char

                    #num and deci Literals 
                    elif char == '0':
                        state = 203
                        lexeme += char

                    elif char in self.digit and char != '0':
                        state = 206
                        lexeme += char

                    elif char == '~' : #tilde or lambda po yan
                        state = 205
                        lexeme += char

                    #single literals
                    elif char == "'":
                        state = 243
                        lexeme += "'"
                    #word literals
                    elif char == "'":
                        state = 247
                        lexeme += "'"
                    
                    elif char in self.alphabet:
                        state = 251
                        lexeme += char
                    
                    #error handling 
                    else: 
                        self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Character ( {repr(char)} ).") 

                 #keywords
                 # BOOL keyword recognition: states 1-5
                case 1:  # 'b'
                    if char == 'o': 
                        state = 2
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                case 2:  # 'bo'
                    if char == 'o': 
                        state = 3
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0
                case 3:  # 'boo'
                    if char == 'l': 
                        state = 4
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0
                case 4:  # 'bool'
                    if char in self.space or char == '\t':
                        # Move to case 5 to finalize token
                        state = 5
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                case 5:  # Finalize 'bool' token
                    column -= 2
                    tokens.append((lexeme, "bool", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 6:  # 'c'
                    if char == 'o': 
                        state = 7
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 

                case 7:  # 'co'
                    if char == 'n': 
                        state = 8
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                
                case 8:  # 'con'
                    if char == 's': 
                        state = 9
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 

                case 9:  # 'cons'
                    if char == 't': 
                        state = 10
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                    
                case 10:  # 'const'
                    if char in self.space or char == '\t':
                        state = 11
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                case 11:  # Finalize 'const' token
                    column -= 2 
                    tokens.append((lexeme, "const", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 12:  # 'd' deci or do
                    if char == 'e': 
                        state = 13
                        lexeme += char
                    elif char == 'o': 
                        state = 19
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                    
                case 13:  # 'de' decimal or def
                    if char == 'c': 
                        state = 14
                        lexeme += char
                    elif char == 'f' : 
                        state = 17
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                    
                case 14:  # 'dec'
                    if char == 'i': 
                        state = 14
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 15:  # 'deci'
                    if char in self.space or char == '\t':
                        state = 16
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                
                case 16:  # Finalize 'deci' token
                    column -= 2
                    tokens.append((lexeme, "deci", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 17:  # 'def'
                    if char in self.delim1:
                        state = 18
                        if char is not None:
                            self.step_back()    
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                
                case 18:  # Finalize 'def' token
                    column -= 2 
                    tokens.append((lexeme, "def", line, column))
                    if char is not None:
                        self.step_back()    
                    state = 0

                case 19:  # 'do'
                    if char in self.curspace:
                        state = 20
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                
                case 20:  # Finalize 'do' token
                    column -= 2
                    tokens.append((lexeme, "do", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 21:  # 'e'
                    if char == 'l': 
                        state = 22
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 22:  # 'el'
                    if char == 's': 
                        state = 23
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                    
                case 23:  # 'els'
                    if char == 'e': 
                        state = 24
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 

                case 24:  # 'else'
                    if char in self.curspace:
                        state = 25
                        if char is not None:
                            self.step_back()
                    
                    elif char == 'i' :  # to handle 'elseif' keyword
                        state = 26
                        lexeme += char

                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char  
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 25:  # Finalize 'else' token
                    column -= 2
                    tokens.append((lexeme, "else", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 26:  # 'elseif' continuation
                    if char == 'f': 
                        state = 27
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:   
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 27:  # 'elseif'
                    if char in self.parspace:
                        state = 28
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 28:  # Finalize 'elseif' token
                    column -= 2
                    tokens.append((lexeme, "elseif", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 29:  # 'f'
                    if char == 'a': 
                        state = 30
                        lexeme += char
                    elif char == 'o': 
                        state = 35
                        lexeme += char
                    elif char == 'u': 
                        state = 38
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 30:  # 'fa'
                    if char == 'l':
                        state = 31
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 31:  # 'fal'
                    if char == 's':
                        state = 32
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 32:  # 'fals'
                    if char == 'e':
                        state = 33
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 33:  # 'false'
                    if char in self.delim2:
                        state = 34
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 34:  # Finalize 'false' token
                    column -= 2 
                    tokens.append((lexeme, "false", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 35:  # 'fo'
                    if char == 'r': 
                        state = 36
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 36:  # 'for'
                    if char in self.parspace:
                        state = 37
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 37:  # Finalize 'for' token
                    column -= 2 
                    tokens.append((lexeme, "for", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 38:  # 'fu'
                    if char == 'n': 
                        state = 39
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 39:  # 'fun'
                    if char == 'c': 
                        state = 40
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0
                        
                case 40:  # 'func'
                    if char == 't': 
                        state = 41
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 41:  # 'funct'
                    if char == 'i':
                        state = 42
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 42:  # 'functi'
                    if char == 'o':
                        state = 43
                        lexeme += char 
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0
                        
                case 43:  # 'functio'
                    if char == 'n':
                        state = 44
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 44:  # 'function'
                    if char in self.space or char == '\t':
                        state = 45
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 45:  # Finalize 'function' token
                    column -= 2
                    tokens.append((lexeme, "function", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 46: # 'i'
                    if char == 'f': 
                        state = 47
                        lexeme += char

                    elif char =='n' :
                        state = 49  # to handle 'in' keyword
                        lexeme += char

                    elif char == 's': 
                        state = 51  # to handle 'is' keyword
                        lexeme += char

                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 47:  # 'if'
                    if char in self.parspace:
                        state = 48
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 48:  # Finalize 'if' token
                    column -= 2 
                    tokens.append((lexeme, "if", line, column))
                    if char is not None:
                        self.step_back()    
                    state = 0   

                case 49:  # 'in'
                    if char in self.parspace:
                        state = 50
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 50:  # Finalize 'in' token
                    column -= 2
                    tokens.append((lexeme, "in", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 51:  # 'is'
                    if char in self.space or char == '\t':
                        state = 52
                        if char is not None:
                            self.step_back()

                    elif char == 'n':  # to handle 'isnot' keyword
                        state = 56
                        lexeme += char

                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 52:  # Finalize 'is' token
                    column -= 2     
                    tokens.append((lexeme, "is", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 53:  # 'isn'
                    if char == 'o':
                        state = 54
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 54:  # 'isno'
                    if char == 't':
                        state = 55
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 55:  # 'isnot'
                    if char in self.space or char == '\t':
                        state = 52
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 56:  # Finalize 'isnot' token
                    column -= 2
                    tokens.append((lexeme, "isnot", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0   
                
                case 57: #'m'
                    if char == 'a':
                        state = 58
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 58:  # 'ma'
                    if char == 'i':
                        state = 59
                        lexeme += char
                    
                    elif char == 't': # to handle 'match' keyword
                        state = 62
                        lexeme += char

                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 59:  # 'mai'
                    if char == 'n':
                        state = 60
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 60:  # 'main'
                    if char in self.parspace:
                        state = 61
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 61:  # Finalize 'main' token
                    column -= 2 
                    tokens.append((lexeme, "main", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 62:  # 'mat'
                    if char == 'c':
                        state = 63
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 63:  # 'matc'
                    if char == 'h':
                        state = 64
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 64:  # 'match'
                    if char in self.parspace:
                        state = 65
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 65:  # Finalize 'match' token
                    column -= 2
                    tokens.append((lexeme, "match", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 66: #'n'
                    if char == 'u':
                        state = 67
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 67: #'nu'
                    if char == 'm':
                        state = 68
                        lexeme += char
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        if char in self.delimiden:
                            state = 254
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 68: #'num'
                    if char in self.space or char == '\t':
                        state = 69
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        state = 253
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                    
                





                # Identifier (State 251 - 255) first stage sa pag build
                case 251:
                    if char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        lexeme += char
                        state = 253
                    elif char in self.delimiden:
                        state = 252
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                case 252:
                    column -= 2
                    tokens.append((lexeme, "identifier", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                case 253:
                    if char is not None and (char in self.alphabet or char in self.digit or char == '_'):
                        lexeme += char
                    elif len(lexeme) > 25:  # Identifier limit
                            self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' exceeds 25 characters.")
                            state = 0
                    elif char in self.delimiden:
                        state = 254
                        if char is not None:
                            self.step_back()   
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(at Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                case 254:
                    column -= 2
                    tokens.append((lexeme, "identifier", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0


        return tokens, self.errors
  