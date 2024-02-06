import sympy
sympy.init_printing(use_unicode=True)

# 微分する関数
# @param eq 式
# @param int cnt 微分回数
# @return sympy.core.add.Add
def differential(eq , cnt:int):
    x = sympy.Symbol('g')
    print(sympy.diff(eq, x, cnt))
    return sympy.diff(eq, x, cnt)

# 積分する関数
# @param eq 式
# @param int cnt 積分回数
# @return sympy.core.add.Add 
def integral(eq , cnt:int):
    x = sympy.Symbol('x')
    eq = 2 * x ** 2 + 5 * x - 3
    print(type(eq))
    for num in range(cnt):
        eq = sympy.integrate(eq)
        print(eq)
    return eq
    