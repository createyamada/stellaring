from fastapi import APIRouter
from service import equationOfMotion
from Library import common
import sympy

router = APIRouter()

@router.get('/')
def index():
    v = sympy.Symbol('v')
    theta = sympy.Symbol('theta')
    t = sympy.Symbol('t')
    x = v * sympy.cos(theta)
    y = v * sympy.sin(theta)

    print(sympy.Eq(sympy.Derivative(y, t), sympy.diff(y, t)))
    common.differential(y,1)

                
    return {"Hello":"world"}