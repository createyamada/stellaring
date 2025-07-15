from fastapi import APIRouter
from pydantic import BaseModel
import numpy as np
from Library import common
from Library import const

router = APIRouter()

class StateScheme(BaseModel):
    k: float
    m: float
    x: float
    phi: float
    speed: float
    step: float
    type: int

@router.get('/')
def index(k: float , m:float , x:float , phi: float , speed:float , step:float , type: int):


    # 初期条件
    num_steps = 100

    # 角周波数
    omega = np.sqrt(k / m)

    # 結果格納用配列
    datas = []

    # 時間配列
    dt = np.arange(0, num_steps, step)  # 0から10までの1000点で等間隔の時間
    # 一般解
    datas = [0] * len(dt)

    # 位置の解析解を計算
    for i in range(len(dt)):
        datas[i] = {
            "y":x * np.cos(omega * dt[i]) + (speed / omega) * np.sin(omega * dt[i]),
            "x":float(dt[i])
        }

    result = {
        "datas" : datas
    } 

    return result