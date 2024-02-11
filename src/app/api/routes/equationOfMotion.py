from fastapi import APIRouter
from service import equationOfMotion
from Library import common
import sympy
import numpy as np
from scipy.integrate import odeint
from Library import const

router = APIRouter()

@router.get('/')
def index(speed: int , angle: float , type: int):


    print(speed)
    print(angle)
    print(type)
    type = 2

    sol = None
    x = None
    y = None

    # 初速度 (m/s)
    speed = 20.0
    # 放射角度 (度)
    angle = 45.0

    # 時間の設定
    total_time = 2 * speed * np.sin(np.radians(angle)) / const.GRAVITATIONAL_ACCELERATION
    num_steps = 100



    if type == 0:
        # 解析解の場合
        # 初期位置 (水平および垂直方向) は原点
        initial_conditions = [0.0, 0.0]  
        # 時間範囲
        t = np.linspace(0,total_time, num_steps)
        # odeint関数を使用して数値積分を実行
        sol = odeint(analytical_solution, initial_conditions, t, args=(angle, speed)) 
    else: 
        # 数値解の場合
        # 時間経過
        dt = total_time / num_steps
        if type == 1:
            # オイラー法の場合
            x, y = numerical_solution_euler(speed, angle, dt, num_steps)
        elif type == 2:
            # ルンゲクッタ法の場合
            x, y = numerical_solution_rungekutta(speed, angle, dt, num_steps)




    # print(sol)      
    # print(x)      
    # print(y)      
    return {"Hello":sol}

# 放物運動　運動方程式
def analytical_solution(y, t, angle, initial_speed):
    theta = np.radians(angle)  # 角度をラジアンに変換
    v0x = initial_speed * np.cos(theta)  # 水平方向の初速度成分
    v0y = initial_speed * np.sin(theta)  # 垂直方向の初速度成分
    dydt = [v0x, v0y - const.GRAVITATIONAL_ACCELERATION * t]
    return dydt

def numerical_solution_euler(v0, theta, dt, num_steps):
    theta_rad = np.radians(theta)  # 角度をラジアンに変換

    # 初期条件
    t = np.linspace(0, num_steps * dt, num_steps + 1)
    vx = v0 * np.cos(theta_rad)
    vy = v0 * np.sin(theta_rad)

    # オイラー法による更新
    x = vx * t
    y = vy * t - 0.5 * const.GRAVITATIONAL_ACCELERATION * t**2

    return x, y


def numerical_solution_rungekutta(v0, theta, dt, num_steps):
    g = 9.8  # 重力加速度 (m/s^2)
    theta_rad = np.radians(theta)  # 角度をラジアンに変換

    # 初期条件
    t = np.linspace(0, num_steps * dt, num_steps + 1)
    vx = v0 * np.cos(theta_rad)
    vy = v0 * np.sin(theta_rad)

    # ルンゲ-クッタ法による更新
    x = vx * t
    y = vy * t - 0.5 * g * t**2

    return x, y
