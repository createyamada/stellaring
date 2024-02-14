from fastapi import APIRouter
from service import equationOfMotion
from library import common
import sympy
import numpy as np
from scipy.integrate import odeint
from library import const

router = APIRouter()

@router.get('/')
# def index(speed: int , angle: float , type: int):
def index():

    speed = 90
    angle = 45.0
    position = 0
    type = 1
    theta_rad = np.radians(angle)
    vx = speed * np.cos(theta_rad)
    vy = speed * np.sin(theta_rad)

    print(speed)
    print(angle)
    print(type)

    sol = None
    x = None
    y = None

    # 時間の設定
    total_time = 2 * speed * np.sin(np.radians(angle)) / const.GRAVITATIONAL_ACCELERATION
    num_steps = 100

    if type == 0:
        # 解析解の場合

        # 時間の範囲を設定
        dt = np.linspace(0, total_time, num_steps)

        # 位置の解析解を計算
        x = vx * dt
        y = position + vy * dt - 0.5 * g * dt**2

        return x, y

    else: 
        # 数値解の場合
        # 時間経過
        dt = total_time / num_steps
        if type == 1:
            # オイラー法の場合
            x, y = numerical_solution_euler(None, func_v, vx, vy, dt, num_steps)
        elif type == 2:
            # ルンゲクッタ法の場合
            x, y = numerical_solution_rungekutta(func_p, func_v, vx, vy, dt, num_steps)




    # print(sol)      
    print(x)      
    print(y)   
    # result = {"x":x,""y":y}   
    # return result
    return {"Hello":"World"}


def numerical_solution_euler(calc_p, calc_v, vx, vy, dt, num_steps):

    """
    オイラー法による常微分方程式の数値解法

    Parameters:
    - calc_p:function 時間変化に応じた位置計算
    - calc_v:function 時間変化に応じた速度計算
    - v0:int 初期速度
    - dt: 刻み幅
    - num_steps: 時刻のリスト数

    Returns:
    - result_x: 対応するx数値解のリスト
    - result_y: 対応するy数値解のリスト
    """

    # 初期条件
    t = np.linspace(0, num_steps * dt, num_steps + 1)

    ini = 0

    h = t[1] - t[0]
    x = np.zeros_like(t, dtype=float)
    y = np.zeros_like(t, dtype=float)
    x[0] = ini
    y[0] = ini

    # オイラー法の計算
    for i in range(len(x) - 1):

    # x[1:] = x[:-1] + h * x(t[:-1], x[:-1])
    # y[1:] = y[:-1] + h * y(t[:-1], y[:-1])
        x[i + 1] = x[i] + (calc_v(vx) * t[i])
        y[i + 1] = y[i] + (calc_v(vy,t[i]) * t[i])

    return x, y


def numerical_solution_rungekutta(calc_p, calc_v, vx, vy, dt, num_steps):

    """
    ルンゲクッタ法による常微分方程式の数値解法

    Parameters:
    - calc_p:function 時間変化に応じた位置計算
    - calc_v:function 時間変化に応じた速度計算
    - v0: 初期速度
    - dt: 刻み幅
    - num_steps: 時刻のリスト数

    Returns:
    - result_x: 対応するx数値解のリスト
    - result_y: 対応するy数値解のリスト
    """

    ini = 0
    # 初期条件
    t = np.linspace(0, num_steps * dt, num_steps + 1)
    h = t[1] - t[0]
    x = np.zeros_like(t, dtype=float)
    y = np.zeros_like(t, dtype=float)
    y[0] = ini
    x[0] = ini


    # ルンゲ-クッタ法による更新
    for i in range(len(x) - 1):
        k1_x = calc_v(vx)
        k2_x = calc_p(x[i] + k1_x/2) * t[i]
        k3_x = calc_p(x[i] + k2_x/2) * t[i]
        k4_x = calc_p(x[i] + k3_x) * t[i]

        k1_y = calc_v(vy, t[i])
        k2_y = calc_p(y[i] + k1_y/2) * t[i]
        k3_y = calc_p(y[i] + k2_y/2) * t[i]
        k4_y = calc_p(y[i] + k3_y) * t[i]

        x[i + 1] = x[i] + (k1_x + 2*k2_x + 2*k3_x + k4_x) / 6
        y[i + 1] = y[i] + (k1_y + 2*k2_y + 2*k3_y + k4_y) / 6

    return x, y


def func_v(v, t=None):
    """
    数値計算用速度ベクトル計算

    Parameters:
    - p: 速度ベクトル
    - t: 時間(default=None)

    Returns:
    - return: 速度ベクトル
    """
    if(t):
        result = v - (const.GRAVITATIONAL_ACCELERATION * t)
    else:
        result = v

    return result

def func_p(p):
    """
    数値計算用位置ベクトル計算

    Parameters:
    - v: 位置ベクトル
    - t: 時間

    Returns:
    - return: 位置ベクトル
    """

    return (-const.GRAVITATIONAL_ACCELERATION * p)



