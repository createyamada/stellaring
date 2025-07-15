from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import math

app = FastAPI()

# 定数定義
G = 6.67430e-11  # 万有引力定数
M_e = 5.972e24   # 地球質量
M_sun = 1.989e30
M_moon = 7.35e22
P_srp = 4.56e-6  # 太陽放射圧（おおよその平均）
C_r = 1.5         # 反射係数
A = 2.0           # 衛星の有効面積（m^2）

class OrbitRequest(BaseModel):
    latitude: float
    longitude: float
    altitude: float
    angle: float       # 発射仰角（度）
    velocity: float     # 初速度（m/s）
    steps: int
    mass: float = 1000.0  # 衛星質量（kg）

# 地球中心からの位置ベクトルに変換
def geodetic_to_ecef(lat_deg, lon_deg, height_m):
    lat = math.radians(lat_deg)
    lon = math.radians(lon_deg)
    r = 6371000 + height_m
    x = r * math.cos(lat) * math.cos(lon)
    y = r * math.cos(lat) * math.sin(lon)
    z = r * math.sin(lat)
    return np.array([x, y, z])

# Runge-Kuttaで加速度を考慮して1ステップ進める
def compute_acceleration(r, m_sat):
    r_sun = np.array([1.496e11, 0, 0])
    r_moon = np.array([3.84e8, 0, 0])

    a_earth = -G * M_e * r / np.linalg.norm(r)**3
    a_sun = -G * M_sun * (r - r_sun) / np.linalg.norm(r - r_sun)**3
    a_moon = -G * M_moon * (r - r_moon) / np.linalg.norm(r - r_moon)**3

    srp_dir = (r - r_sun) / np.linalg.norm(r - r_sun)
    a_srp = (C_r * P_srp * A / m_sat) * srp_dir

    thrust = np.array([0.5, 0, 0])  # 仮の推進力方向
    a_thrust = thrust / m_sat

    return a_earth + a_sun + a_moon + a_srp + a_thrust

@app.post("/")
def simulate_orbit(req: OrbitRequest):
    # 初期位置・速度
    r0 = geodetic_to_ecef(req.latitude, req.longitude, req.altitude)
    theta_rad = math.radians(req.angle)
    v0 = np.array([0, req.velocity * math.cos(theta_rad), req.velocity * math.sin(theta_rad)])

    r = r0
    v = v0
    h = 1.0
    result = []

    for _ in range(req.steps):
        result.append(r.tolist())

        k1_v = compute_acceleration(r, req.mass)
        k1_r = v

        k2_v = compute_acceleration(r + 0.5 * h * k1_r, req.mass)
        k2_r = v + 0.5 * h * k1_v

        k3_v = compute_acceleration(r + 0.5 * h * k2_r, req.mass)
        k3_r = v + 0.5 * h * k2_v

        k4_v = compute_acceleration(r + h * k3_r, req.mass)
        k4_r = v + h * k3_v

        r = r + (h / 6.0) * (k1_r + 2*k2_r + 2*k3_r + k4_r)
        v = v + (h / 6.0) * (k1_v + 2*k2_v + 2*k3_v + k4_v)

    return {
        "status": "success",
        "message": "3D軌道計算完了",
        "trajectory_ecef": result
    }
