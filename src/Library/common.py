import numpy as np


def numerical_solution_euler(f:object, vx:float, vy:float, dt:np.ndarray):
    """
    オイラー法による常微分方程式の数値解法

    Parameters:
    - f:object 速度を更新する力{"x":vxの力,"y":vyの力}
    - vx: x軸初速度
    - vy: y軸初速度
    - dt:array 刻み幅リスト

    Returns:
    - result: x,y軸の位置ベクトルのリスト[{"x":0,"y":0},...]
    """
    # 初期条件
    # 刻み幅
    h = dt[1] - dt[0]
    # 結果格納用配列
    result = [0] * len(dt)
    # 初期位置
    result[0] = {
        "x":0,
        "y":0
    }

    # オイラー法による更新
    for i in range(len(dt) - 1):
        result[i+1] = {
            "x":result[i]["x"] + vx,
            "y":result[i]["y"] + (vy * h)
        }
        # 速度を更新する
        vx -= f["x"] * h
        vy -= f["y"] * h
        if (result[i+1]["y"] < 0):
            break
    return result



def numerical_solution_rungekutta(f:object, vx:float, vy:float, dt:np.ndarray):
    """
    ルンゲクッタ法による常微分方程式の数値解法

    Parameters:
    - f:object 速度を更新する力{"x":vxの力,"y":vyの力}
    - vx: x軸初速度
    - vy: y軸初速度
    - dt:array 刻み幅リスト

    Returns:
    - result: x,y軸の位置ベクトルのリスト[{"x":0,"y":0},...]
    """
    # 初期条件
    # 刻み幅
    h = dt[1] - dt[0]
    # 結果格納用配列
    result = [0] * len(dt)
    # 初期位置
    result[0] = {
        "x":0,
        "y":0
    }
    

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

        result[i+1] = {
            "x":result[i]["x"] + (k1_x + 2 * k2_x + 2 * k3_x + k4_x) / 6,
            "y":result[i]["y"] + (k1_y + 2 * k2_y + 2 * k3_y + k4_y) / 6
        }

        # 速度を更新する
        vx -= f["x"]
        vy -= f["y"] * h
        if (result[i]["y"] < 0):
            break
    return result
