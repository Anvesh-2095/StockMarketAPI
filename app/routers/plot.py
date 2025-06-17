from typing import List

from fastapi import APIRouter
from .. import models

router = APIRouter(
    prefix="/plot",
)

@router.get("/{name}")
def get_plot(name: str, start_date: str = None, end_date: str = None, indicators: List[str] = None):
    pass