from fastapi import APIRouter
import numpy as np

router = APIRouter()

@router.get('/')
def index(speed: float , angle: float , step:float , type: int):

    # パラメータ
    m = 1.0  # 質量
    k = 1.0  # バネ定数

    # 初期条件
    x0 = 1.0  # 初期位置
    v0 = 0.0  # 初期速度

    # 角周波数
    omega = np.sqrt(k / m)

    # 時間配列
    t = np.linspace(0, 10, 1000)  # 0から10までの1000点で等間隔の時間

    # 一般解
    x = x0 * np.cos(omega * t) + (v0 / omega) * np.sin(omega * t)

    return x