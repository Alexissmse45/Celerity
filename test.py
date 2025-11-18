from lexer import Lexer

def test_lexer():
    code = """
    2
    ;
    """
#  bool flag = true;
#         single c = 'a';
#         word s = "hello";
#         if (flag) {
#             out("test");
#         }
#         while (x < 10) {
#             x++;
#         }
    lexer = Lexer()
    tokens, errors = lexer.lexeme(code)

    # Print tokens nicely
    print(f"{'Lexeme':<15} | {'Token':<12} | {'Line':<4} | {'Col':<4}")
    print("-" * 45)
    for token in tokens:
        print(f"{token[0]:<15} | {token[1]:<12} | {token[2]:<4} | {token[3]:<4}")
    print()

    # Print errors in a separate section if any
    if errors:
        print("Errors:")
        print("-" * 45)
        for error in errors:
            print(error)
        print()
    else:
        print("No errors found.\n")


if __name__ == "__main__":
    test_lexer()







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
