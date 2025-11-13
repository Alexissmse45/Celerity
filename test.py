from lexer import Lexer

def main():
    
    lexer = Lexer()
    code = "isnot ;"
    tokens, errors = lexer.lexeme(code)

    print(f"{'Lexeme':<20} | {'Token':<15} | {'Token Type':<15} | {'Line':<4} | {'Col':<4}")
    print("-" * 80)
    for lex, token_type, line, col in tokens:
        print(f"{lex:<20} | {lex:<15} | {token_type:<15} | {line:<4} | {col:<4}")

    if errors:
        print("\nErrors:")
        for err in errors:
            print(err)
    print("Running lexer test...")

if __name__ == "__main__":
    main()










# from tryyy import Tokenizer  # Adjust if your filename differs

# def test_tokenizer():
#     code = """
#     int main() {
#         bool flag = true;
#         char c = 'a';
#         string s = "hello";
#         float f = 123.45;
#         if (flag) {
#             parse();
#         }
#         while (x < 10) {
#             x++;
#         }
#         return 0;
#     }
#     """

#     tokenizer = Tokenizer()
#     tokens, errors = tokenizer.tokenize(code)

#     # Print tokens nicely
#     print(f"{'Lexeme':<15} | {'Token':<12} | {'Line':<4} | {'Col':<4}")
#     print("-" * 45)
#     for token in tokens:
#         print(f"{token[0]:<15} | {token[1]:<12} | {token[2]:<4} | {token[3]:<4}")
#     print()

#     # Print errors in a separate section if any
#     if errors:
#         print("Errors:")
#         print("-" * 45)
#         for error in errors:
#             print(error)
#         print()
#     else:
#         print("No errors found.\n")


# if __name__ == "__main__":
#     test_tokenizer()
