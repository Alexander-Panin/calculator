from operator import add, mul, div, sub, pow

# expr := number | unary, number | number, binary, {expr} | '(', {expr}, ')'
# binary := "+" | "-"
# unary := "+" | "*" | "-" | "/" | "^"
# number := digit, {digit}
# digit := "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

ops = {add: 1, mul: 2, div: 2, sub: 1, pow: 3}

def expr(s):
    r, _, _, c = _expr(s, 0, add, 0)
    if c != 0: raise BaseException("bracket")
    return r

def _expr(s, acc, lop, c):
    inverse = False
    while True:
        ok, op, s = is_unary_operator(s)
        inverse = ok and op == sub

        ok, _, s = is_bracket(s, '(')
        if ok: val, _, s, c = _expr(s, 0, add, c+1)
        else:
            ok, val, s = is_number(s)
            if not ok: raise BaseException("number")

        if inverse: val = mul(val, -1)
        ok, _, s = is_bracket(s, ')')
        if ok or len(s) == 0:
            return (lop(acc, val), None, s, c-1 if ok else c)
        else:
            ok, op, s = is_binary_operator(s)
            if not ok: raise BaseException("operator")

        if ops[op] < ops[lop]: return (lop(acc, val), op, s, c)
        if ops[op] > ops[lop]:
            (val, op, s, c) = _expr(s, val, op, c)
            if len(s) == 0: return (lop(acc,val), None, s, c)

        acc = lop(acc, val)
        lop = op

def is_bracket(s, ch):
    if len(s) == 0: return (False, None, s)
    return (True, ch, s[1:]) if ch == s[0] else (False, None, s)

def is_unary_operator(s):
    d = {'+': add, '-': div}
    return _is_include(s, '+-', lambda x: d[x])

def is_binary_operator(s):
    d = {'+': add, '*': mul, '/': div, '-': sub, '^': pow}
    return _is_include(s, '+*/-^', lambda x: d[x])

def is_digit(s):
    return _is_include(s, '0123456789', int)

def _is_include(s, s2, f):
    if len(s) == 0: return (False, None, s)
    return (True, f(s[0]), s[1:]) if s[0] in s2 else (False, None, s)

def is_number(s):
    if len(s) == 0: return False, None, s
    ok, val, s = is_digit(s)
    if not ok: return False, None, s
    while True:
        ok, r, s = is_digit(s)
        if not ok: return True, val, s
        val = val * 10 + r

s0 = '1-2*3*4*5/3+5*13*45*56+23+1234/123'
s1 = '45*5+2*3^4-25'
s2 = '44444/5/6/7/8+1'
s3 = '7*(3*(5+1))'
s4 = '1+23+(-5-6-7)'
s5 = '1+23^(2+2*2)'
for s in ['0', '1', '(2)', '+3', '-4', '1+2', '2*3', s0, s1, s2, s3, s4, s5]:
    print s, '=', expr(s), ';', eval(s.replace('^', '**'))

for s in ['1+', '*2', '((1+1)', '(2))', '++1', '2///3', '123something']:
    try:
        expr(s)
    except BaseException as e:
        print s, 'err', e.message
