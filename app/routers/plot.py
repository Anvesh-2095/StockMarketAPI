from typing import List, Optional
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, status, Query, Body
from pyexpat import features

from .. import models
from fastapi.responses import JSONResponse

from ..models import PlotRequest
from ..utils import draw_plot, features_list
router = APIRouter(
    prefix="/plot",
)

@router.get("/{name}")
def get_plot(name: str, indicators: PlotRequest,  start_date: Optional[str] = None, end_date: Optional[str] = None):

    try:
        if start_date:
            start_date = datetime.strptime(start_date, "%d-%m-%Y")
        if end_date:
            end_date = datetime.strptime(end_date, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid date format. Use 'DD-MM-YYYY'.")

    if not end_date:
        end_date = datetime.now()
    if not start_date:
        start_date = end_date - timedelta(days=7)

    if (end_date - start_date).days < 7:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="The date range must be at least 7 days.")

    if not indicators:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="At least one indicator must be provided.")

    # res = [draw_plot.get_plot(name, indicator, start_date, end_date) for indicator in indicators.indicators]
    res = []
    for indicator in indicators.indicators:
        if indicator and indicator in features_list.plot_indicators_list:
            res.append(draw_plot.get_plot(name, indicator, start_date, end_date))
    return JSONResponse(content={"images": res})