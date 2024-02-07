from fastapi import APIRouter
from pydantic import BaseModel, Field
import numpy as np

router = APIRouter()


class StateScheme(BaseModel):
    position_1: list[float] = Field(..., min_length=2, max_length=2)
    position_2: list[float] = Field(..., min_length=2, max_length=2)
    velocity_1: list[float] = Field(..., min_length=2, max_length=2)
    velocity_2: list[float] = Field(..., min_length=2, max_length=2)
    mass_1: float
    mass_2: float


@router.post('/calc_state')
async def calc_state(prev_state: StateScheme):
    # TOFIX:
    point_x = prev_state.point_x + 1.2
    point_y = prev_state.point_y
    velocity_x = prev_state.velocity_x
    velocity_y = prev_state.velocity_y
    return {
        "point_x": point_x,
        "point_y": point_y + 3.1,
        "velocity_x": velocity_x,
        "velocity_y": velocity_y
        }
