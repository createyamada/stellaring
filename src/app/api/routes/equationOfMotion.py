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

    # 初期条件
    speed = 100
    angle = 45.0
    position = 0
    step = 0.1
    type = 1
    num_steps = 100
    theta_rad = np.radians(angle)
    vx = speed * np.cos(theta_rad)
    vy = speed * np.sin(theta_rad)

    # 結果格納用配列
    result = []

    #  取得する配列（時間間隔）を作成
    dt = np.arange(0,num_steps,step) 

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
        f = {"x":0,"y":const.GRAVITATIONAL_ACCELERATION}
        # 数値解の場合
        if type == 1:
            # オイラー法の場合
            result = numerical_solution_euler(f, vx, vy, dt)
        elif type == 2:
            # ルンゲクッタ法の場合
            result = numerical_solution_rungekutta(f, vx, vy, dt)




    return result


def numerical_solution_euler(f, vx, vy, dt):
    """
    オイラー法による常微分方程式の数値解法

    Parameters:
    - f:array 速度を更新する力[vxの力,vyの力]
    - vx: x軸初速度
    - vy: y軸初速度
    - dt:array 刻み幅リスト

    Returns:
    - result: x,y軸の位置ベクトルのリスト[{"x":0,"y":0},...]
    """
    print(f)
    print(f["x"])
    # 初期条件
    # 刻み幅
    h = dt[1] - dt[0]
    # 初期位置
    # 結果格納用配列
    result = [0] * len(dt)
    result[0] = {
        "x":0,
        "y":0
    }



    # こいつは多分いらない
    x = [0] * len(dt)
    y = [0] * len(dt)
    y[0] = 0
    x[0] = 0

    # オイラー法の計算
    for i in range(len(dt) - 1):
        x[i + 1] = x[i] + vx
        y[i + 1] = y[i] + (vy * h)
        result[i+1] = {
            "x":x[i+1],
            "y":y[i+1]
        }
        # 速度を更新する
        vx = vx
        vy -= const.GRAVITATIONAL_ACCELERATION * h
        if (y[i+1] < 0):
            break
    return result


def numerical_solution_rungekutta(f, vx, vy, dt):

    """
    ルンゲクッタ法による常微分方程式の数値解法

    Parameters:
    - f:array 速度を更新する力[vxの力,vyの力]
    - vx: x軸初速度
    - vy: y軸初速度
    - dt:array 刻み幅リスト

    Returns:
    - result: x,y軸の位置ベクトルのリスト[{"x":0,"y":0},...]
    """
    # 初期条件
    # 刻み幅
    h = dt[1] - dt[0]
    # 初期位置
    # 結果格納用配列
    result = [0] * len(dt)
    result[0] = {
        "x":0,
        "y":0
    }



    # こいつは多分いらない
    x = [0] * len(dt)
    y = [0] * len(dt)
    y[0] = 0
    x[0] = 0
    

    # ルンゲ-クッタ法による更新
    for i in range(len(dt) - 1):
        k1_x = vx
        k2_x = vx + h / 2 * k1_x
        k3_x = vx + h / 2 * k2_x 
        k4_x = vx + h * k3_x

        k1_y = vy
        k2_y = vy + h / 2 * k1_y
        k3_y = vy + h / 2 * k2_y 
        k4_y = vy + h * k3_y

        x[i + 1] = x[i] + (k1_x + 2 * k2_x + 2 * k3_x + k4_x) / 6
        y[i + 1] = y[i] + (k1_y + 2 * k2_y + 2 * k3_y + k4_y) / 6
        result[i+1] = {
            "x":x[i + 1],
            "y":y[i + 1]
        }

        # 速度を更新する
        vx = vx
        vy -= const.GRAVITATIONAL_ACCELERATION * h
        if (y[i+1] < 0 ):
            break
    return result


def test():
    """
    放物運動力

    Parameters:
    - None

    Returns:
    - return:　力[x軸にかかる力,y軸にかかる力] 
    """

    return {"x":0,"y":const.GRAVITATIONAL_ACCELERATION}

