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

    speed = 100
    angle = 45.0
    position = 0
    step = 0.1
    type = 2
    num_steps = 100
    theta_rad = np.radians(angle)
    vx = speed * np.cos(theta_rad)
    vy = speed * np.sin(theta_rad)

    print(speed)
    print(angle)
    print(step)
    print(num_steps)
    print(type)

    sol = None
    x = None
    y = None

    result = []

    #  取得する配列（時間間隔）を作成
    dt = np.arange(0,num_steps,step) 
    print("len(dt)")
    print(len(dt))



    if type == 0:
        # 解析解の場合
        result = [0] * len(dt)
        # 位置の解析解を計算
        for i in range(len(dt)-1):
            print(i)
            result[i] = {
                "x":vx * dt[i],
                "y":position + vy * dt[i] - 0.5 * const.GRAVITATIONAL_ACCELERATION * dt[i]**2
            }
            print(result[i])
            if (result[i]["y"] < 0):
                break

    else: 
        # 数値解の場合
        if type == 1:
            # オイラー法の場合
            result = numerical_solution_euler(func_p, func_v, vx, vy, dt, num_steps)
        elif type == 2:
            # ルンゲクッタ法の場合
            result = numerical_solution_rungekutta(func_p, func_v, vx, vy, dt, num_steps)




    return result


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
    # t = np.linspace(0, num_steps * dt, num_steps + 1)

    ini = 0

    h = dt[1] - dt[0]
    # x = np.zeros_like(dt, dtype=float)
    # y = np.zeros_like(dt, dtype=float)
    x = [0] * len(dt)
    y = [0] * len(dt)

    x[0] = 0
    y[0] = 0



    result = [0] * len(dt)

    result[0] = {
        "x":0,
        "y":0
    }

    # オイラー法の計算
    for i in range(len(dt) - 1):
        x[i + 1] = calc_p(x[i],calc_v(vx),h)
        y[i + 1] = calc_p(y[i],calc_v(vy,dt[i]),h)
        result[i+1] = {
            "x":x[i+1],
            "y":y[i+1]
        }
        if (y[i+1] < 0):
            break
    return result


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
    # t = np.linspace(0, num_steps * dt, num_steps + 1)
    h = dt[1] - dt[0]
    # x = np.zeros_like(dt, dtype=float)
    # y = np.zeros_like(dt, dtype=float)
    x = [0] * len(dt)
    y = [0] * len(dt)
    y[0] = 0
    x[0] = 0
    result = [0] * len(dt)
    result[0] = {
        "x":0,
        "y":0
    }

    print(dt)
    # ルンゲ-クッタ法による更新
    for i in range(len(dt) - 1):
        # print(i)
        k1_x = calc_p(x[i],calc_v(vx),h)
        k2_x = calc_p(x[i] + k1_x/2,calc_v(vx),dt[i+1])
        k3_x = calc_p(x[i] + k2_x/2,calc_v(vx),dt[i+1])
        k4_x = calc_p(x[i] + k3_x,calc_v(vx),dt[i+1])
        print('k1_x')
        print(k1_x)
        print('k2_x')
        print(k2_x)
        print('k3_x')
        print(k3_x)
        print('k4_x')
        print(k4_x)

        k1_y = calc_p(y[i],calc_v(vy,dt[i]),h)
        k2_y = calc_p(y[i] + k1_y/2,calc_v(vy,dt[i]),dt[i+1])
        k3_y = calc_p(y[i] + k2_y/2,calc_v(vy,dt[i]),dt[i+1])
        k4_y = calc_p(y[i] + k3_y,calc_v(vy,dt[i]),dt[i+1])

        x[i + 1] = x[i] + (k1_x + 2 * k2_x + 2 * k3_x + k4_x) / 6
        y[i + 1] = y[i] + (k1_y + 2 * k2_y + 2 * k3_y + k4_y) / 6
        print('y[i+1]')
        print(round(y[i+1],3) )
        result[i+1] = {
            "x":x[i + 1],
            "y":y[i + 1]
        }
        if (y[i+1] < 0 ):
            break
    return result


def func_v(v, t=None):
    """
    数値計算用速度ベクトル計算

    Parameters:
    - p: 速度ベクトル
    - t: 時間(default=None)

    Returns:
    - return: 速度ベクトル
    """
    if t is None:
        return v
    else:
        return v - (const.GRAVITATIONAL_ACCELERATION * t)


    # return result

def func_p(p,v,t):
    """
    数値計算用位置ベクトル計算

    Parameters:
    - v: 位置ベクトル
    - t: 時間

    Returns:
    - return: 位置ベクトル
    """

    # return (-const.GRAVITATIONAL_ACCELERATION * p)
    return p + (v * t)

def func_p_runge(p,t):
    """
    数値計算用位置ベクトル計算

    Parameters:
    - v: 位置ベクトル
    - t: 時間

    Returns:
    - return: 位置ベクトル
    """

    return (-const.GRAVITATIONAL_ACCELERATION * p) * t
    # return p + (v * t)


