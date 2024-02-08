from fastapi import APIRouter
from pydantic import BaseModel, Field
import numpy as np

router = APIRouter()
GRAVITATIONAL_CONSTANT = 6.6743 * 10**(-11)


class StateScheme(BaseModel):
    position_1: list[float] = Field(..., min_items=2, max_items=2)
    position_2: list[float] = Field(..., min_items=2, max_items=2)
    velocity_1: list[float] = Field(..., min_items=2, max_items=2)
    velocity_2: list[float] = Field(..., min_items=2, max_items=2)
    mass_1: float
    mass_2: float
    delta_time: float


def calc_gravity(position_1: list[float], position_2: list[float], mass_1: float, mass_2: float) -> list[float]:
    np_position_1 = np.array(position_1)
    np_position_2 = np.array(position_2)
    np_distance_vector = np_position_1 - np_position_2
    distance = np.linalg.norm(np_distance_vector)
    np_gravity_1 = -(GRAVITATIONAL_CONSTANT * mass_1 * mass_2 / distance**3) * np_distance_vector
    np_gravity_2 = - np_gravity_1
    return [
        np_gravity_1.tolist(),
        np_gravity_2.tolist()
    ]


@router.post('/calc_state')
async def calc_state(state: StateScheme):
    gravity = calc_gravity(state.position_1, state.position_2, state.mass_1, state.mass_2)
    np_new_position_1 = np.array(state.position_1) + state.delta_time * np.array(state.velocity_1)
    np_new_position_2 = np.array(state.position_2) + state.delta_time * np.array(state.velocity_2)
    np_new_velocity_1 = np.array(state.velocity_1) + state.delta_time * np.array(gravity[0]) / state.mass_1
    np_new_velocity_2 = np.array(state.velocity_2) + state.delta_time * np.array(gravity[1]) / state.mass_2
    return {
        "position_1": np_new_position_1.tolist(),
        "position_2": np_new_position_2.tolist(),
        "velocity_1": np_new_velocity_1.tolist(),
        "velocity_2": np_new_velocity_2.tolist(),
        }
