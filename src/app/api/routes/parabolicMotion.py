from fastapi import APIRouter
from pydantic import BaseModel
import numpy as np
from library import common
from library import const

router = APIRouter()

class StateScheme(BaseModel):
    speed: float
    angle: float
    step: float
    type: int

@router.get('/')
def index(speed: float , angle: float , step:float , type: int):
    # 初期条件
    num_steps = 100
    theta_rad = np.radians(angle)
    vx = speed * np.cos(theta_rad)
    vy = speed * np.sin(theta_rad)

    # 結果格納用配列
    datas = []

    #  取得する配列（時間間隔）を作成
    dt = np.arange(0,num_steps,step) 

    # print(type(dt))
    if type == 0:
        # 解析解の場合
        datas = [0] * len(dt)
        position = 0
        # 位置の解析解を計算
        for i in range(len(dt)-1):
            datas[i] = {
                "x":vx * dt[i],
                "y":position + vy * dt[i] - 0.5 * const.GRAVITATIONAL_ACCELERATION * dt[i]**2
            }
            if (datas[i]["y"] < 0):
                break

    else: 
        f = {"x":0,"y":const.GRAVITATIONAL_ACCELERATION}
        # 数値解の場合
        if type == 1:
            # オイラー法の場合
            datas = common.numerical_solution_euler(f, vx, vy, dt)
        elif type == 2:
            # ルンゲクッタ法の場合
            datas = common.numerical_solution_rungekutta(f, vx, vy, dt)

    # 最高到達点計算
    maxHeight = (speed ** 2) * (np.sin(theta_rad) ** 2) / (2 * const.GRAVITATIONAL_ACCELERATION)
    # 水平到達距離
    maxWidth = (speed ** 2) / const.GRAVITATIONAL_ACCELERATION * (2 * np.sin(theta_rad)) * np.cos(theta_rad)

    print(datas)
    result = {
        "datas" : datas,
        "maxHeight" : maxHeight,
        "maxWidth" : maxWidth,
    } 


    return result








