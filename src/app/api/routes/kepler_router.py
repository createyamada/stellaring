from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class StateScheme(BaseModel):
    point_x: float
    point_y: float
    velocity_x: float
    velocity_y: float


@router.post('/calc_state')
async def calc_state(prev_state: StateScheme):
    position_1 = prev_state.point_x + 1.2
    point_y = prev_state.point_y
    velocity_x = prev_state.velocity_x
    velocity_y = prev_state.velocity_y
    return {
        "point_x": point_x,
        "point_y": point_y + 3.1,
        "velocity_x": velocity_x,
        "velocity_y": velocity_y
        }
