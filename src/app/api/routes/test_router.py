from fastapi import APIRouter
from pydantic import BaseModel, Field
import time
import random

router = APIRouter()


class StateScheme(BaseModel):
    test_num: float


@router.get("/test")
def test_get():
    sleep_time = random.uniform(1, 5)
    time.sleep(sleep_time)
    return {"test_num": "success!",
            "sleep_time": sleep_time}


@router.post("/test")
def test(state: StateScheme):
    state.test_num += 0.1
    return {"test_num": state.test_num}
