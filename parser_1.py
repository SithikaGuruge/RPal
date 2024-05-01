


#   E  -> ’let’ D ’in’ E                          => ’let’
#      -> ’fn’ Vb+ ’.’ E                          => ’lambda’
#      ->  Ew;

def parse_E(tokens):
    if tokens and tokens[0][0] == 'let':
        tokens.pop(0)
        parse_D(tokens)

        if tokens and tokens[0][0] == 'in':
            tokens.pop(0)
            parse_E(tokens)

    elif tokens and tokens[0][0] == 'fn':
        tokens.pop(0)
        while tokens[0][0] == 'Vb':
            parse_Vb(tokens)
        if tokens and tokens[0][0] == '.':
            tokens.pop(0)
            parse_E(tokens)
    else:
        parse_Ew(tokens)


#  Ew -> T ’where’ Dr                            => ’where’
#     -> T;
def parse_Ew(tokens):
    parse_T(tokens)
    if tokens and tokens[0][0] == 'where':
        tokens.pop(0)
        parse_Dr(tokens)


#  T  -> Ta ( ’,’ Ta )+                          => ’tau’
#     -> Ta ;
def parse_T(tokens):
    parse_Ta(tokens)
    while tokens and tokens[0][0] == ',':
        tokens.pop(0)
        parse_Ta(tokens)

# Ta -> Ta ’aug’ Tc                             => ’aug’
#    -> Tc ;


def parse_Ta(tokens):
    parse_Tc(tokens)
    while tokens and tokens[0][0] == 'aug':
        tokens.pop(0)
        parse_Tc(tokens)

# Tc  -> B ’->’ Tc ’|’ Tc                      => '->'
#     -> B ;


def parse_Tc(tokens):
    parse_B(tokens)
    if tokens and tokens[0][0] == '->':
        tokens.pop(0)
        parse_Tc(tokens)
        if tokens and tokens[0][0] == '|':
            tokens.pop(0)
            parse_Tc(tokens)

# B  -> B ’or’ Bt                               => ’or’
#    -> Bt ;


def parse_B(tokens):
    parse_Bt(tokens)
    while tokens and tokens[0][0] == 'or':
        tokens.pop(0)
        parse_Bt(tokens)
# Bt -> Bt ’&’ Bs                               => ’&’
#    -> Bs ;


def parse_Bt(tokens):
    parse_Bs(tokens)
    while tokens and tokens[0][0] == '&':
        tokens.pop(0)
        parse_Bs(tokens)
# Bs -> ’not’ Bp                                => ’not’
#    -> Bp ;


def parse_Bs(tokens):
    if tokens and tokens[0][0] == 'not':
        tokens.pop(0)
        parse_Bp(tokens)

    else:
        parse_Bp(tokens)

# Bp -> A('gr' | '>')A  => 'gr'
#    -> A('ge' | '>=')A => 'ge'
#    -> A('ls' | '<')A  => 'ls'
#    -> A('le' | '<=')A => 'le'
#    -> A'eq'A          => 'eq'
#    -> A'ne'A          => 'ne'
#    -> A ;


def parse_Bp(tokens):
    parse_A(tokens)
    if tokens[0][0] in ['gr', '>']:
        tokens.pop(0)
        parse_A(tokens)
    elif tokens[0][0] in ['ge', '>=']:
        tokens.pop(0)
        parse_A(tokens)
    elif tokens[0][0] in ['ls', '<']:
        tokens.pop(0)
        parse_A(tokens)
    elif tokens[0][0] in ['le', '<=']:
        tokens.pop(0)
        parse_A(tokens)
    elif tokens[0][0] == 'eq':
        tokens.pop(0)
        parse_A(tokens)
    elif tokens[0][0] == 'ne':
        tokens.pop(0)
        parse_A(tokens)

# A  -> A ’+’ At                                => ’+’
#    -> A ’-’ At                                => ’-’
#    -> At ;


def parse_A(tokens):
    if tokens[0][0] == '+':
        tokens.pop(0)
        parse_At(tokens)
    elif tokens[0][0] == '-':
        tokens.pop(0)
        parse_At(tokens)
    else:
        parse_At(tokens)

    while tokens and tokens[0][0] in ['+', '-']:
        if tokens[0][0] == '+':
            tokens.pop(0)
            parse_At(tokens)
        elif tokens[0][0] == '-':
            tokens.pop(0)
            parse_At(tokens)

# At -> At ’*’ Af                               => ’*’
#    -> At ’/’ Af                               => ’/’
#    -> Af ;


def parse_At(tokens):
    parse_Af(tokens)
    while tokens and tokens[0][0] in ['*', '/']:
        if tokens[0][0] == '*':
            tokens.pop(0)
            parse_Af(tokens)
        elif tokens[0][0] == '/':
            tokens.pop(0)
            parse_Af(tokens)

# Af -> Ap ’**’ Af                              => ’**’
#    -> Ap ;


def parse_Af(tokens):
    parse_Ap(tokens)
    while tokens and tokens[0][0] == '**':
        tokens.pop(0)
        parse_Ap(tokens)

#


def parse_Ap(tokens):
    parse_R(tokens)
    while tokens and tokens[0][0] == '@':
        tokens.pop(0)
        if tokens and tokens[0][1] == '<IDENTIFIER>':
            tokens.pop(0)
            print("Ap -> Ap @ <IDENTIFIER> R")
            print("Ap -> R")
        else:
            return SyntaxError
        parse_R(tokens)

# R  -> R Rn
#    -> Rn ;


def parse_R(tokens):
    parse_Rn(tokens)
    while tokens[0][0] in ['true', 'false', 'nil', 'dummy', '('] or tokens[0][1] in ['<IDENTIFIER>', '<INTEGER>', '<STRING>']:
        parse_Rn(tokens)

# Rn -> ’true’
#    -> ’false’
#    -> ’nil’
#    -> ’dummy’
#    -> ’(’ E ’)’
#     -> ’<IDENTIFIER>’
#     -> ’<INTEGER>’
#     -> ’<STRING>’ ;


def parse_Rn(tokens):
    if tokens and tokens[0][0] in ['true', 'false', 'nil', 'dummy', '('] or tokens[0][1] in ['<IDENTIFIER>', '<INTEGER>', '<STRING>']:
        if tokens[0][0] == 'true':
            pass
        elif tokens[0][0] == 'false':
            pass
        elif tokens[0][0] == 'nil':
            pass
        elif tokens[0][0] == 'dummy':
            pass
        elif tokens[0].type in ['<IDENTIFIER>', '<INTEGER>', '<STRING>']:
            pass
            tokens.pop(0)
        elif tokens and tokens[0][0] == '(':
            tokens.pop(0)
            parse_E(tokens)
            if tokens and tokens[0][0] == ')':
                tokens.pop(0)
            else:
                return SyntaxError
        else:
            return SyntaxError

# D-> Da ’within’ D
#   -> Da


def parse_D(tokens):
    parse_Da(tokens)
    while tokens and tokens[0][0] == 'within':
        tokens.pop(0)
        parse_D(tokens)

# Da -> Dr ('and' Da) +
#   -> Dr


def parse_Da(tokens):
    parse_Dr(tokens)
    n = 0
    while tokens and tokens[0][0] == 'and':
        tokens.pop(0)
        parse_Dr(tokens)
        n += 1
    if n > 0:
        build_tree('and', n+1)

# Dr -> 'rec' Db
#   -> Db


def parse_Dr(tokens):
    if tokens and tokens[0][0] == 'rec':
        tokens.pop(0)
        parse_Db(tokens)

    else:
        parse_Db(tokens)

# Db -> Vl ’=’ E
#    -> '<IDENTIFIER>' Vb+ ’=’ E
#    -> ’(’ D ’)’ ;


def parse_Db(tokens):
    if tokens and tokens[0][0] == '(':
        tokens.pop(0)
        parse_D(tokens)
        if tokens and tokens[0][0] == ')':
            tokens.pop(0)
        else:
            return SyntaxError

    elif tokens and tokens[0][1] == '<IDENTIFIER>':

        tokens.pop(0)
        while tokens and tokens[0][0] == 'Vb':
            parse_Vb(tokens)
            if tokens and tokens[0][0] == '=':
                tokens.pop(0)
                parse_E(tokens)

    else:
        parse_Vl(tokens)
        if tokens and tokens[0][0] == '=':
            tokens.pop(0)
            parse_E(tokens)

# Vb -> '<IDENTIFIER>'
#    -> '(' Vl ')' ;
#     -> '(' ')' ;


def parse_Vb(tokens):
    if tokens and tokens[0][1] == '<IDENTIFIER>':
        tokens.pop(0)
        pass
    elif tokens and tokens[0][0] == '(':
        tokens.pop(0)
        if tokens and tokens[0][1] == '<IDENTIFIER>':
            parse_Vl(tokens)
            if tokens and tokens[0][0] == ')':
                tokens.pop(0)
            else:
                return SyntaxError
        if tokens and tokens[0][0] == ')':
            tokens.pop(0)

# Vl -> -> ’<IDENTIFIER>’ list ’,’


def parse_Vl(tokens):
    if tokens and tokens[0][1] == '<IDENTIFIER>':
        tokens.pop(0)
        if tokens and tokens[0][0].type() == 'list':
            tokens.pop(0)
            if tokens and tokens[0][0] == ',':
                tokens.pop(0)
            else:
                return SyntaxError
        else:
            return SyntaxError
    else:
        return SyntaxError
