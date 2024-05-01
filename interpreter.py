import re


def parse(file):
    contents = open(file, 'r').read()
    tokens = lexer(contents)
    return tokens


def lexer(contents):
    digit = "[0-9]"
    letter = "[a-zA-Z]"
    operatorSymbol = "[+\\-*/<>&.@/:=~|$!#%^_\\[\\]{}`'\\?]"

    patterns = {
        'Identifier': f"^{letter}({letter}|{digit}|_)*",
        'Integer': f"{digit}+",
        'Operator': f"^{operatorSymbol}+",
        'String': r'^\"(?:\\.|[^\\"])*\"',
        'Spaces': r"^(\s|\t)+",
        'Comment': "^//.*",
        'Punctuation': "[(),;]"
    }

    compiled_patterns = {key: re.compile(pattern) for key, pattern in patterns.items()}

    tokens = []
    for line in contents.split('\n'):
        while line:
            matched = False
            for token_type, pattern in compiled_patterns.items():
                match = pattern.match(line)
                if match:
                    value = match.group(0)
                    # if token_type != 'Spaces' and token_type != 'Comment':
                    tokens.append((token_type, value))

                    line = line[len(value):].lstrip()
                    matched = True
                    break
            if not matched:
                raise ValueError("Unable to match token at: '{}'".format(line))
    return tokens
