from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class StateScheme(BaseModel):
    test_num: float


@router.post("/test")
def test(state: StateScheme):
    state.test_num += 0.1
    return {"test_num": state.test_num}
